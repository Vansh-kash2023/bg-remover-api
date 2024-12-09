import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    # Use the port provided by Render (via the PORT environment variable) or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  # For local and Render deployment
