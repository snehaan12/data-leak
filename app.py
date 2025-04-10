import os
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

from utils.extract_text import extract_text
from utils.presidio_scanner import scan_with_presidio
from utils.drive_uploader import upload_to_drive

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <title>DLP Upload</title>
    <h2>Upload File for Sensitive Data Scan</h2>
    <form method=post enctype=multipart/form-data action="/upload">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    content = extract_text(file_path)
    findings = scan_with_presidio(content)

    if findings:
        os.remove(file_path)
        return jsonify({"status": "unsafe", "findings": findings}), 403

    drive_url = upload_to_drive(file_path, filename)
    os.remove(file_path)

    return jsonify({"status": "safe", "message": "File uploaded", "url": drive_url}), 200

if __name__ == '__main__':
    app.run(debug=True)
