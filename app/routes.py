from flask import Blueprint, request, jsonify, url_for, render_template
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from rembg import remove
import os
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

OUTPUT_DIR = 'app/static/processed_images'
TEMP_DIR = 'app/static/temp_images'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/process-image', methods=['POST'])
def process_image():
    try:
        data = request.json
        image_url = data.get('image_url')
        if not image_url:
            return jsonify({"error": "Missing 'image_url' in the request body."}), 400

        unique_temp_filename = f"{uuid.uuid4().hex}.tmp"
        temp_image_path = os.path.join(TEMP_DIR, unique_temp_filename)
        with requests.get(image_url, stream=True, timeout=60) as response:
            if response.status_code != 200:
                return jsonify({"error": "Failed to fetch the image from the provided URL."}), 400
            
            with open(temp_image_path, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    temp_file.write(chunk)

        try:
            with Image.open(temp_image_path) as image:
                image_bytes = BytesIO()
                image.save(image_bytes, format="PNG")
                image_bytes.seek(0)
                transparent_image_bytes = remove(image_bytes.getvalue())
        except UnidentifiedImageError:
            os.remove(temp_image_path)
            return jsonify({"error": "Invalid image format."}), 400

        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.png"
        processed_image_path = os.path.join(OUTPUT_DIR, unique_filename)
        with open(processed_image_path, "wb") as f:
            f.write(transparent_image_bytes)

        os.remove(temp_image_path)

        processed_image_url = url_for('static', filename=f'processed_images/{unique_filename}', _external=True)
        return jsonify({
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        })

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image: {e}")
        return jsonify({"error": "Failed to download the image."}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
