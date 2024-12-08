
---

# **Background Removal API Documentation**

## **1. Project Overview**

This project provides a simple API for removing the background from an image. The API accepts a public image URL and optionally coordinates (bounding box) to specify the area from which the background should be removed. The processed image with the background removed is returned via a public URL.

### **Features:**
- Accepts a public image URL.
- Optionally accepts a bounding box for cropping.
- Removes the background from the specified image area.
- Returns the processed image via a unique URL.

---

## **2. API Endpoints**

### **2.1. `/process-image`**

#### **Method:**
- **POST**

#### **Request Body:**
The API accepts a JSON body with two fields:
- `image_url` (required): The URL of the image from which the background will be removed.
- `bounding_box` (optional): A dictionary containing coordinates to crop the image before removing the background. If not provided, the entire image will be processed.

**Example Request Body:**
```json
{
  "image_url": "https://example.com/image.jpg",
  "bounding_box": {
    "x_min": 100,
    "y_min": 150,
    "x_max": 500,
    "y_max": 600
  }
}
```

#### **Request Parameters:**
- **image_url**: A string containing the URL of the image.
- **bounding_box** (optional):
  - **x_min**: The X-coordinate of the top-left corner of the bounding box.
  - **y_min**: The Y-coordinate of the top-left corner of the bounding box.
  - **x_max**: The X-coordinate of the bottom-right corner of the bounding box.
  - **y_max**: The Y-coordinate of the bottom-right corner of the bounding box.

#### **Response Body:**
The API will respond with the original image URL and the URL for the processed image.

**Example Response Body:**
```json
{
  "original_image_url": "https://example.com/image.jpg",
  "processed_image_url": "http://127.0.0.1:5000/static/processed_images/unique-uuid.png"
}
```

#### **Error Responses:**
If there is an error processing the request, the API will return an error message along with an HTTP status code.

- **400 Bad Request**: Missing `image_url` or invalid `bounding_box`.
- **500 Internal Server Error**: Unexpected errors during image processing.

**Example Error Response:**
```json
{
  "error": "Missing image_url"
}
```

---

## **3. Setting Up the Project**

### **3.1. Prerequisites**

Before setting up the project, ensure you have the following:
- **Python 3.6+** installed on your machine.
- **Virtual environment** (recommended to isolate dependencies).
- **Git** for version control (if cloning from GitHub).

### **3.2. Clone the Repository**
If you haven't already, clone the repository from GitHub:
```bash
git clone https://github.com/yourusername/bg-remover-api.git
cd bg-remover-api
```

### **3.3. Install Dependencies**

It is recommended to use a **virtual environment** to install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
```

Next, install the necessary dependencies using `pip`:
```bash
pip install -r requirements.txt
```

**`requirements.txt`** should include the following dependencies:
```text
Flask==2.1.0
requests==2.26.0
Pillow==8.4.0
rembg==2.0.0
waitress==3.0.2
```

---

## **4. Running the Project Locally**

### **4.1. Run with Flask (Development Mode)**

To run the API locally for development purposes, you can use Flask's built-in server:
```bash
python run.py
```
The server will be available at `http://127.0.0.1:5000/`.

### **4.2. Run with Waitress or Gunicorn (Production Mode)**

For production deployment, you can use a WSGI server like **Waitress** or **Gunicorn**. Here is how to run the application with **Waitress**:

Install Waitress (if not already installed):
```bash
pip install waitress
```

Run the server:
```bash
python run.py
```
Or, for Gunicorn:
```bash
gunicorn -w 4 run:app
```

This will serve the app with 4 worker processes.

---

## **5. Folder Structure**

The folder structure of the project is as follows:

```
bg-remover-api/
│
├── app/
│   ├── __init__.py        # Initializes the Flask app
│   ├── routes.py          # API route definitions
│   └── static/
│       └── processed_images/  # Folder where processed images are saved
│
├── run.py                 # Entry point to run the Flask app
├── requirements.txt       # List of required Python packages
├── README.md              # This file
└── .gitignore             # Git ignore file
```

- **`app/static/processed_images/`**: Directory where processed images are saved temporarily for access via public URLs.
- **`run.py`**: The main entry point to start the Flask server.

---

## **6. Error Handling**

The API includes basic error handling. Possible errors include:

- **400 Bad Request**: Occurs if `image_url` is missing or the bounding box coordinates are invalid.
- **500 Internal Server Error**: Occurs if there's an unexpected error during the image processing (e.g., if `rembg` fails).

**Error Example:**
```json
{
  "error": "Invalid bounding box coordinates"
}
```

---

## **7. Deployment Instructions**

For deploying the API to a production server, you can use services like **Heroku**, **AWS**, **DigitalOcean**, or **PythonAnywhere**. 

### **7.1. Deploying on Heroku**

Here is a general guide for deploying to **Heroku**:

1. **Install the Heroku CLI**: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login to Heroku**: `heroku login`
3. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
4. **Create a new Heroku app**:
   ```bash
   heroku create
   ```
5. **Deploy to Heroku**:
   ```bash
   git push heroku master
   ```
6. **Scale your app** (Optional):
   ```bash
   heroku ps:scale web=1
   ```

Heroku will automatically set up everything for you, including provisioning a web dyno.

### **7.2. Configure Static Files (Heroku Specific)**

If using **Heroku**, ensure static files (processed images) are stored properly:
```python
# Ensure static files are served correctly
app.config['UPLOAD_FOLDER'] = 'app/static/processed_images'
```

---

## **8. Tools, Frameworks, and Libraries**

### **1. Flask**
- **Description**: Flask is a lightweight and flexible web framework for Python that is commonly used to build APIs and web applications. It provides essential features for routing HTTP requests, handling user inputs, and serving static files.
- **Why it's used**: Flask is used for creating the API endpoints in this project. It provides a simple way to set up the backend for the background removal functionality. Flask’s flexibility allows you to easily add routes and extend the functionality without unnecessary overhead.

### **2. rembg**
- **Description**: `rembg` is a Python package that utilizes machine learning models to remove the background from images. It provides a simple API to remove backgrounds from images with high accuracy.
- **Why it's used**: `rembg` is the core tool used to process images and remove backgrounds. The package provides an easy-to-use API for background removal, making it ideal for this project.

### **3. Pillow**
- **Description**: Pillow is a powerful Python imaging library that allows you to open, manipulate, and save many different image file formats.
- **Why it's used**: Pillow is used to handle image processing tasks such as opening the image from the URL, cropping based on bounding box coordinates, and saving images. It is essential for working with image files in this API.

### **4. requests**
- **Description**: `requests` is a Python HTTP library for making requests to external APIs or websites. It is often used to fetch data from URLs or interact with web services.
- **Why it's used**: `requests` is used to download the image from the provided URL in the API. It ensures that the image is fetched and processed before background removal.

### **5. Gunicorn (Optional for Production)**
- **Description**: Gunicorn is a Python WSGI HTTP server for UNIX. It is a pre-fork worker model server, which is efficient for handling multiple requests at the same time in production environments.
- **Why it's used**: Gunicorn is used for deploying the Flask application in production. It can handle multiple requests simultaneously, making it more scalable and efficient compared to Flask's built-in server.

### **6. Waitress (Optional for Production)**
- **Description**: Waitress is a production-quality WSGI server for Python web applications. It is known for its performance and ease of use in production environments.
- **Why it's used**: Waitress is an alternative to Gunicorn. It can be used to serve the Flask application in production and is lightweight, making it a good choice for smaller projects or simpler deployments.

### **7. uuid**
- **Description**: The `uuid` module in Python generates universally unique identifiers (UUIDs). It is used to create unique file names or identifiers.
- **Why it's used**: UUID is used to create unique filenames for processed images to ensure that multiple users can upload and get processed images without overwriting each other's files. The unique identifier prevents filename conflicts.

### **8. JSON**
- **Description**: JSON (JavaScript Object Notation) is a lightweight data interchange format. It is easy to read and write, and it is used to transmit data between a server and a client.
- **Why it's used**: The API exchanges data with clients in JSON format. Both the input (e.g., image URL and bounding box) and the output (e.g., URLs of the original and processed images) are sent and received as JSON.

### **9. os**
- **Description**: The `os` module in Python provides a way to interact with the operating system. It includes functions for file handling, directory manipulation, and environment variable access.
- **Why it's used**: The `os` module is used to create directories (e.g., the `processed_images` folder), check file existence, and manage file paths in the application.

---

### **Why These Tools Were Chosen:**
- **Ease of Setup**: Flask is simple and quick to set up, making it ideal for small to medium-sized applications like this one.
- **Efficient Image Processing**: `rembg` provides a powerful, ready-to-use machine learning model for background removal. The combination of `rembg` and Pillow ensures that images are handled correctly and efficiently.
- **Scalability**: Gunicorn and Waitress help make the API scalable by enabling it to handle multiple requests simultaneously. They are production-grade servers that can handle the demands of real-world applications.
- **Flexibility**: The tools and libraries chosen provide flexibility in terms of error handling, scalability, and adding new features. For example, you could extend the API to support different image formats or allow additional image processing options.

---

## **9. Conclusion**

This API provides a simple yet powerful solution for background removal from images. It handles requests efficiently and can be easily deployed to production environments for scalable use.
