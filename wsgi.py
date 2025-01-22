from app import create_app

print("Creating app...")
try:
    app = create_app()
    print("App created successfully!")
except Exception as e:
    print(f"Error creating app: {str(e)}")
    raise

if __name__ == '__main__':
    app.run()
    