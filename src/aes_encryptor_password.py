import argparse
import os
import sys
import getpass
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from yt_dlp import YoutubeDL
from base64 import b64encode, b64decode

def derive_key_from_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=16)

def download_video(youtube_url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print(f"[+] Video downloaded to: {output_path}")

def encrypt_file(file_path, password, output_file=None):
    salt = get_random_bytes(16)
    key = derive_key_from_password(password, salt)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(file_path, 'rb') as f:
        data = f.read()

    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    enc_file_path = output_file if output_file else file_path + ".enc"

    with open(enc_file_path, 'wb') as f:
        f.write(salt + iv + ciphertext)

    print(f"[+] File encrypted: {enc_file_path}")
    print(f"[+] Use the same password to decrypt this file.")

def decrypt_file(enc_file_path, password, output_file=None):
    with open(enc_file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()

    key = derive_key_from_password(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    dec_file_path = output_file if output_file else enc_file_path.replace(".enc", ".dec")
    with open(dec_file_path, 'wb') as f:
        f.write(plaintext)

    print(f"[+] File decrypted: {dec_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt videos using password-based AES encryption.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encrypt", help="YouTube video URL or local file to encrypt")
    group.add_argument("--decrypt", help="Encrypted file to decrypt")
    parser.add_argument("--output", help="Optional output file name")

    args = parser.parse_args()
    password = getpass.getpass(prompt="🔐 Enter password: ")

    if args.encrypt:
        if args.encrypt.startswith("http"):
            temp_video = "downloaded_video.mp4"
            download_video(args.encrypt, temp_video)
            encrypt_file(temp_video, password, args.output)
            os.remove(temp_video)
        else:
            encrypt_file(args.encrypt, password, args.output)

    elif args.decrypt:
        decrypt_file(args.decrypt, password, args.output)

if __name__ == "__main__":
    main()
