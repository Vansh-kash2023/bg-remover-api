from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# For production use this
# from app import create_app
# from waitress import serve

# app = create_app()

# if __name__ == "__main__":
#     # Use Waitress to serve the app
#     serve(app, host="0.0.0.0", port=5000)
