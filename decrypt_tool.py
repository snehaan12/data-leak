import os
from cryptography.fernet import Fernet

UPLOADS_DIR = "uploads"
KEYS_DIR = "keys"
OUTPUT_DIR = "recovered"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def decrypt_file(filename):
    enc_path = os.path.join(UPLOADS_DIR, filename)
    key_path = os.path.join(KEYS_DIR, filename.replace(".enc", ".key"))
    output_path = os.path.join(OUTPUT_DIR, filename.replace(".enc", ""))

    if not os.path.exists(enc_path):
        print(f"❌ Encrypted file not found: {enc_path}")
        return

    if not os.path.exists(key_path):
        print(f"❌ Key file not found: {key_path}")
        return

    with open(key_path, "rb") as kf:
        key = kf.read()

    cipher = Fernet(key)
    with open(enc_path, "rb") as ef:
        encrypted_data = ef.read()

    decrypted = cipher.decrypt(encrypted_data)

    with open(output_path, "wb") as out:
        out.write(decrypted)

    print(f"✅ Decrypted → {output_path}")

if __name__ == "__main__":
    print("🔍 Scanning /uploads for encrypted files...\n")
    for file in os.listdir(UPLOADS_DIR):
        if file.endswith(".enc"):
            decrypt_file(file)
