import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators  


load_dotenv()


QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  
FILL_COLOR = os.getenv('FILL_COLOR', 'black')  
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, path, fill_color='red', back_color='white'):
    if not is_valid_url(data):
        return  

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default='https://github.com/rk94407')
    args = parser.parse_args()

    
    setup_logging()
    
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"github_qr{timestamp}.png"

    
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename
    
    
    create_directory(Path.cwd() / QR_DIRECTORY)
    
    
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()