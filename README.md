# 🔐 Cloud-Based Data Leak Detector

This app detects sensitive data in uploaded files (like emails, Aadhaar, bank numbers) and encrypts them before uploading to Google Drive. Built using Python, Streamlit, and Presidio.

---

## 🚀 Features

- Upload `.txt`, `.pdf`, `.docx` files
- Automatically scan for sensitive data (PII)
- Encrypt unsafe files using Fernet
- Upload encrypted/safe files to Google Drive
- Decrypt tool for admins

---

## 🛠️ Tech Stack

- Python 3
- Streamlit
- Microsoft Presidio
- Google Drive API
- Cryptography (Fernet)

---

## 📦 Setup Locally

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd data_leak_detector
pip install -r requirements.txt
