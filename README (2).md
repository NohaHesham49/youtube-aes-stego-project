# 🔐 AES Video Encryptor + Steganography Project

This project demonstrates how to:
1. 🔒 Encrypt a YouTube video using AES encryption with a password
2. 🖼️ Hide the encrypted video inside a PNG image using steganography

## 📁 Project Structure

```
project-folder/
├── aes_encryptor_password.py
├── steg_hide_file_in_image.py
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

Install the required packages using:

```
pip install -r requirements.txt
```

Or individually:

```
pip install pycryptodome yt-dlp pillow
```

---

## ✨ Features

### 🔐 AES Encryption with Password

Encrypt a YouTube video:

```bash
python aes_encryptor_password.py --encrypt "https://youtube.com/shorts/..." --output video.enc
```

Decrypt it:

```bash
python aes_encryptor_password.py --decrypt video.enc --output video.mp4
```

> The password is requested at runtime. The key is derived securely using PBKDF2.

---

### 🖼️ Steganography – Hide Encrypted File Inside Image

**Embed encrypted file into a PNG image:**

```bash
python steg_hide_file_in_image.py hide --image cover_4k.png --file video.enc --output secret.png
```

**Extract the encrypted file back:**

```bash
python steg_hide_file_in_image.py extract --image secret.png --output recovered.enc
```

> Make sure to use a large PNG image (e.g., 4K resolution) for big encrypted files.

---

## 🎓 Use Case

This project was created as part of a cybersecurity training application focused on:
- Cryptography
- Penetration Testing
- Practical offensive/defensive skills

