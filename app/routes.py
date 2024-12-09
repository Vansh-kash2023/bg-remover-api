from flask import Blueprint, request, jsonify, current_app, url_for
import requests
from io import BytesIO
from PIL import Image
from rembg import remove
import os
import uuid
from datetime import datetime

main = Blueprint('main', __name__)

# Ensure the output directory exists
os.makedirs('app/static/processed_images', exist_ok=True)

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

        # Download the image
        response = requests.get(image_url)
        print(f"Response status: {response.status_code}")  # Debugging line
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch the image from the provided URL."}), 400
        
        # Verify that the image content is not empty
        if not response.content:
            return jsonify({"error": "Empty image data received."}), 400

        # Open the image
        image = Image.open(BytesIO(response.content))

        # Optional: Crop the image if bounding_box is provided
        if bounding_box:
            try:
                x_min, y_min = bounding_box['x_min'], bounding_box['y_min']
                x_max, y_max = bounding_box['x_max'], bounding_box['y_max']

                if any(coord < 0 for coord in [x_min, y_min, x_max, y_max]) or x_min >= x_max or y_min >= y_max:
                    return jsonify({"error": "Invalid bounding box coordinates."}), 400

                # Crop the image
                image = image.crop((x_min, y_min, x_max, y_max))
            except KeyError:
                return jsonify({"error": "Bounding box must contain 'x_min', 'y_min', 'x_max', and 'y_max' keys."}), 400

        # Remove the background
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        transparent_image_bytes = remove(image_bytes.getvalue())

        # Check if background removal produced valid data
        if not transparent_image_bytes:
            return jsonify({"error": "Background removal failed or returned empty data."}), 400

        # Ensure the output directory exists
        output_dir = current_app.config.get('STATIC_FOLDER', 'app/static/processed_images')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate a unique filename for the processed image
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.png"
        processed_image_path = os.path.join(output_dir, unique_filename)

        # Check the processed image path
        print(f"Processed image path: {processed_image_path}")  # Debugging line

        # Save the processed image
        with open(processed_image_path, "wb") as f:
            f.write(transparent_image_bytes)

        # Generate the processed image's public URL using url_for
        processed_image_url = url_for('static', filename=f'processed_images/{unique_filename}', _external=True)

        return jsonify({
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        })

    except Exception as e:
        # Capture unexpected errors and provide feedback
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
