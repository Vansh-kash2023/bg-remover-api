from flask import Blueprint, request, jsonify
import requests
from io import BytesIO
from PIL import Image
from rembg import remove
import os
import uuid
from datetime import datetime

main = Blueprint('main', __name__)

# Path to save processed images
OUTPUT_DIR = 'app/static/processed_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@main.route('/')
def home():
    return "Welcome to the Flask API!"

@main.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Parse JSON input
        data = request.json
        image_url = data.get('image_url')
        bounding_box = data.get('bounding_box', None)  # Bounding box is now optional

        if not image_url:
            return jsonify({"error": "Missing image_url"}), 400

        # Download the image
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400
        
        # Open the image from the downloaded content
        image = Image.open(BytesIO(response.content))

        if bounding_box:
            # Validate bounding box format
            x_min, y_min = bounding_box['x_min'], bounding_box['y_min']
            x_max, y_max = bounding_box['x_max'], bounding_box['y_max']
            if any(coord < 0 for coord in [x_min, y_min, x_max, y_max]) or x_min >= x_max or y_min >= y_max:
                return jsonify({"error": "Invalid bounding box coordinates"}), 400

            # Crop the image to the bounding box
            image = image.crop((x_min, y_min, x_max, y_max))

        # Remove the background
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        transparent_image_bytes = remove(image_bytes.getvalue())

        # Generate a unique filename for the processed image
        unique_filename = f"{str(uuid.uuid4())}.png"
        processed_image_path = os.path.join(OUTPUT_DIR, unique_filename)

        # Save the processed image
        with open(processed_image_path, "wb") as f:
            f.write(transparent_image_bytes)

        # Construct the public URL of the processed image
        processed_image_url = f"http://127.0.0.1:5000/static/processed_images/{unique_filename}"
        
        return jsonify({
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
