from flask import Blueprint, request, jsonify, url_for
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from rembg import remove
import os
import uuid
from datetime import datetime

main = Blueprint('main', __name__)

# Output directory for processed images (used in local development)
OUTPUT_DIR = 'app/static/processed_images'

# Ensure the output directory exists only if it's a local environment
if not os.getenv("ENV", "development") == "production":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

@main.route('/')
def home():
    return "Welcome to the Flask API for Background Removal!"

@main.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Parse JSON input
        data = request.json
        image_url = data.get('image_url')
        bounding_box = data.get('bounding_box', None)  # Bounding box is optional

        if not image_url:
            return jsonify({"error": "Missing 'image_url' in the request body."}), 400
        if not image_url.startswith(('http://', 'https://')):
            return jsonify({"error": "Invalid URL provided for 'image_url'."}), 400

        # Stream image download to reduce memory overhead
        try:
            with requests.get(image_url, stream=True, timeout=10) as response:
                if response.status_code != 200:
                    return jsonify({"error": "Failed to fetch the image from the provided URL."}), 400
                
                response.raw.decode_content = True  # Ensure content is decoded
                image = Image.open(BytesIO(response.content))
        except requests.RequestException as e:
            return jsonify({"error": f"Failed to fetch the image: {str(e)}"}), 400
        except UnidentifiedImageError:
            return jsonify({"error": "The provided image could not be opened or is not supported."}), 400

        # Optional: Crop the image if bounding_box is provided
        if bounding_box:
            try:
                x_min, y_min = bounding_box['x_min'], bounding_box['y_min']
                x_max, y_max = bounding_box['x_max'], bounding_box['y_max']

                if any(coord < 0 for coord in [x_min, y_min, x_max, y_max]) or x_min >= x_max or y_min >= y_max:
                    return jsonify({"error": "Invalid bounding box coordinates."}), 400

                image = image.crop((x_min, y_min, x_max, y_max))
            except KeyError:
                return jsonify({"error": "Bounding box must contain 'x_min', 'y_min', 'x_max', and 'y_max' keys."}), 400

        # Remove the background
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Perform background removal
        transparent_image_bytes = remove(image_bytes.getvalue())
        if not transparent_image_bytes:
            return jsonify({"error": "Background removal failed."}), 500

        # Save the processed image
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.png"
        processed_image_url = None

        if os.getenv("ENV", "development") == "production":
            # In production, return in-memory URL or use cloud storage
            processed_image_url = "data:image/png;base64," + transparent_image_bytes.encode("base64")
        else:
            # For local development, save to disk and generate public URL
            processed_image_path = os.path.join(OUTPUT_DIR, unique_filename)
            with open(processed_image_path, "wb") as f:
                f.write(transparent_image_bytes)
            processed_image_url = url_for('static', filename=f'processed_images/{unique_filename}', _external=True)

        return jsonify({
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
