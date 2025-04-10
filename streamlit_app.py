import streamlit as st
from scan_engine import handle_file
from cryptography.fernet import Fernet

st.set_page_config(page_title="Cloud DLP", layout="centered")

st.title("🔐 Cloud-Based Data Leak Detector")
st.markdown("Upload `.txt`, `.pdf`, `.docx` files to scan for sensitive data.")

uploaded_file = st.file_uploader("Upload a File", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Scanning for sensitive info..."):
        result = handle_file(uploaded_file.read(), uploaded_file.name)

    if result["status"] == "unsafe":
        st.error(result["message"])
        for item in result["findings"]:
            st.markdown(f"- **{item['entity_type']}** → `{item['text']}`")
        st.markdown(f"[📎 Download Encrypted File]({result['url']})", unsafe_allow_html=True)
    else:
        st.success(result["message"])
        st.markdown(f"[✅ View File in Drive]({result['url']})", unsafe_allow_html=True)

st.divider()
st.subheader("🔐 Admin Decryption Panel")

enc_file = st.file_uploader("Upload Encrypted File (.enc)", type=["enc"], key="admin_enc")
key_file = st.file_uploader("Upload Key File (.key)", type=["key"], key="admin_key")

if enc_file and key_file:
    try:
        key = key_file.read()
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(enc_file.read())

        output_filename = enc_file.name.replace(".enc", "")

        st.download_button(
            label="🔓 Download Decrypted File",
            data=decrypted_data,
            file_name=output_filename,
            mime="application/octet-stream"
        )
        st.success("✅ Decryption successful!")
    except Exception as e:
        st.error(f"❌ Decryption failed: {e}")
