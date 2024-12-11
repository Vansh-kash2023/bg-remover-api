# **Background Removal API Documentation**

## **1. Project Overview**

This project provides a simple API for removing the background from an image. The API accepts a public image URL, processes the image to remove its background, and provides the processed image via a unique URL.

### **Features:**
- Accepts a public image URL.
- Removes the background from the image.
- Returns the processed image via a unique URL.

---

## **2. API Endpoints**

### **2.1. `/process-image`**

#### **Method:** `POST`

#### **Request Body:**

- **image_url** (required): The URL of the image to process.

**Example Request Body:**

```json
{
  "image_url": "public_image_url",
  "bounding_box": {
    "x_min": "integer",
    "y_min": "integer",
    "x_max": "integer",
    "y_max": "integer"
  }
}
```

#### **Response Body:**

The API responds with the original image URL and the URL for the processed image.

**Example Response Body:**

```json
{
  "original_image_url": "https://example.com/image.jpg",
  "processed_image_url": "https://your-deployment-url/static/processed_images/unique-uuid.png"
}
```

#### **Error Responses:**

- **400 Bad Request**: Missing or invalid `image_url`.
- **500 Internal Server Error**: Unexpected errors during image processing.

**Example Error Response:**

```json
{
  "error": "Invalid image_url"
}
```

---

## **3. Setting Up the Project**

### **3.1. Prerequisites**

- Python 3.6+ installed.
- Virtual environment (recommended).
- Git (if cloning the repository).

### **3.2. Clone the Repository**

```bash
git clone https://github.com/yourusername/bg-remover-api.git
cd bg-remover-api
```

### **3.3. Install Dependencies**

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## **4. Running the Project Locally**

### **4.1. Run the Server**

Run the Flask application locally:

```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000/`.

---

## **5. Folder Structure**

The project directory is structured as follows:

```
bg-remover-api/
│
├── app/
│   ├── __init__.py                # Initializes the Flask app
│   ├── routes.py                  # API route definitions
│   ├── static/
│   │   ├── processed_images/      # Folder where processed images are saved
│   │   └── css/
│   │       └── home.css           # CSS for the home page
│   └── templates/
│       └── home.html              # HTML file for the home page
│
├── config.py                      # Configuration settings (e.g., upload folder paths)
├── Procfile                       # Instructions for deployment on Railway
├── run.py                         # Entry point for running the Flask app
├── requirements.txt               # List of required Python packages
├── README.md                      # Project documentation (this file)
└── .gitignore                     # Files and folders to be ignored by Git

```

- **`app/static/processed_images/`**: Directory where processed images are saved temporarily for access via public URLs.
- **`config.py`**: Centralized configuration for settings like `UPLOAD_FOLDER`.
- **`Procfile`**: Specifies the process to run the application in production (e.g., for Railway deployment).

---

## **6. Deployment Instructions**

### **6.1. Deploying on Railway**

1. **Install the Railway CLI:**
   Follow the official guide to set up the Railway CLI: [Railway CLI Documentation](https://docs.railway.app/cli/).

2. **Initialize the Project:**

   ```bash
   railway init
   ```

3. **Deploy the Project:**

   ```bash
   railway up
   ```

4. **Environment Variables:**
   Set the required environment variables (e.g., `PORT`) in the Railway Dashboard.

5. **Access Your API:**
   Railway will provide a public URL for your API upon successful deployment.

---

## **7. Tools and Libraries**

### **1. Flask**

- **Description**: Flask is a lightweight and flexible web framework for Python, commonly used for building APIs and web applications.
- **Usage**: Facilitates the creation of API endpoints, request handling, and serving static files.

### **2. rembg**

- **Description**: `rembg` is a Python package leveraging machine learning models for background removal from images.
- **Usage**: Core functionality for removing backgrounds from uploaded images.

### **3. Pillow**

- **Description**: A Python imaging library for opening, manipulating, and saving image files.
- **Usage**: Processes image files (e.g., resizing, cropping) and ensures compatibility with the `rembg` library.

### **4. requests**

- **Description**: An HTTP library for Python to make web requests.
- **Usage**: Fetches images from provided URLs before processing.

### **5. Gunicorn**

- **Description**: A Python WSGI HTTP server for UNIX, designed for serving web applications in production.
- **Usage**: Handles multiple concurrent requests when the API is deployed.

### **6. Waitress**

- **Description**: A production-quality WSGI server for Python applications.
- **Usage**: Alternative to Gunicorn for serving the Flask app in production.

### **7. uuid**

- **Description**: Python’s `uuid` module generates universally unique identifiers.
- **Usage**: Generates unique filenames for processed images to prevent overwriting.

### **8. JSON**

- **Description**: Lightweight data-interchange format widely used for APIs.
- **Usage**: Input (image URL) and output (processed image URLs) are formatted as JSON.

### **9. os**

- **Description**: Python module for interacting with the operating system.
- **Usage**: Manages file paths, creates necessary directories, and interacts with static file storage.

### **10. Railway**

- **Description**: A deployment platform that simplifies hosting applications with minimal configuration.
- **Usage**: Hosts the API with automated deployment and scaling features.

---

## **8. Conclusion**

This API provides a reliable and scalable solution for background removal from images. It is easy to set up locally and deploy in production environments such as Railway for seamless user access.

---
