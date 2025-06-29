import argparse
from PIL import Image
import os

def embed_file_in_image(image_path, file_to_hide, output_image):
    with open(file_to_hide, 'rb') as f:
        hidden_data = f.read()

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Ensure image can hold the data
    max_bytes = img.width * img.height * 3 // 8
    if len(hidden_data) > max_bytes:
        raise ValueError("Data too large to hide in this image.")

    # Convert data to bits
    binary_data = ''.join(format(byte, '08b') for byte in hidden_data) + '1111111111111110'  # EOF marker
    data_index = 0
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_data):
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_image)
    print(f"[+] File embedded into image: {output_image}")

def extract_file_from_image(stego_image, output_file):
    img = Image.open(stego_image)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary_data = ''
    for pixel in img.getdata():
        for color in pixel:
            binary_data += str(color & 1)

    # Extract bytes until EOF marker
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    file_data = bytearray()
    for byte in all_bytes:
        if byte == '11111110':  # EOF
            break
        file_data.append(int(byte, 2))

    with open(output_file, 'wb') as f:
        f.write(file_data)

    print(f"[+] File extracted and saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Hide and extract a file inside a PNG image.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hide_parser = subparsers.add_parser("hide")
    hide_parser.add_argument("--image", required=True, help="Path to cover PNG image")
    hide_parser.add_argument("--file", required=True, help="File to hide inside image")
    hide_parser.add_argument("--output", required=True, help="Output image with hidden file")

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("--image", required=True, help="Stego image")
    extract_parser.add_argument("--output", required=True, help="Output file to save extracted data")

    args = parser.parse_args()

    if args.command == "hide":
        embed_file_in_image(args.image, args.file, args.output)
    elif args.command == "extract":
        extract_file_from_image(args.image, args.output)

if __name__ == "__main__":
    main()
