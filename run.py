from Foodimg2Ing import app
import os

if __name__ == '__main__':
    # Ensure the upload folder exists before the app starts
    upload_path = os.path.join('Foodimg2Ing', 'static', 'images')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"Created Artisan directory: {upload_path}")

    # Run the server
    # Port 5000 is standard, but you can change it if needed
    app.run(host='127.0.0.1', port=5000, debug=True)