import os
from cryptography.fernet import Fernet
from utils.extract_text import extract_text
from utils.presidio_scanner import scan_with_presidio
from utils.drive_uploader import upload_to_drive

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Optional: save keys for admin testing only
KEYS_FOLDER = "keys"
os.makedirs(KEYS_FOLDER, exist_ok=True)

def encrypt_file(file_path: str, filename: str) -> tuple[str, str]:
    key = Fernet.generate_key()

    # Optionally store for admin offline recovery
    key_path = os.path.join(KEYS_FOLDER, filename + ".key")
    with open(key_path, "wb") as f:
        f.write(key)

    cipher = Fernet(key)
    with open(file_path, "rb") as f:
        raw = f.read()
    encrypted = cipher.encrypt(raw)

    encrypted_path = file_path + ".enc"
    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    return encrypted_path  # no key_path returned

def handle_file(file_bytes, filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    content = extract_text(file_path)
    findings = scan_with_presidio(content)

    if findings:
        encrypted_path = encrypt_file(file_path, filename)

        with open(file_path, "w") as f:
            f.write("This file contains sensitive data and has been encrypted.")

        drive_url = upload_to_drive(encrypted_path, filename + ".enc")
        os.remove(file_path)
        os.remove(encrypted_path)

        return {
            "status": "unsafe",
            "message": "Sensitive info found. Encrypted file uploaded.",
            "url": drive_url,
            "findings": findings
        }

    drive_url = upload_to_drive(file_path, filename)
    os.remove(file_path)

    return {
        "status": "safe",
        "message": "No sensitive info found. File uploaded.",
        "url": drive_url
    }
