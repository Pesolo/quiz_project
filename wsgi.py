from app import create_app

print("Starting application initialization...")
try:
    flask_app = create_app()
    app = flask_app  # This explicit assignment helps Gunicorn find the 'app' variable
    print("Application initialized successfully!")
except Exception as e:
    print(f"Error initializing application: {str(e)}")
    raise

if __name__ == '__main__':
    app.run()