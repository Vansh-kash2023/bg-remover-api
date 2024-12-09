from app import create_app
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()

# Create the Flask app instance
app = create_app()

# Only run the app with Flask's built-in server if this script is run directly
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Use for local development
