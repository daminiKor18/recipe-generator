import os
import gdown

# 1. DEFINE THE DOWNLOADER
def download_assets():
    # UPDATED with your verified matching IDs
    assets = {
        'modelbest.ckpt': '1SeNx5cxnjYW-03w8YLrymgzxC3-3tHBC',
        'ingr_vocab.pkl': '1lBTrokWH1AHq9bMFxuykozhnZ7WohYBN',
        'instr_vocab.pkl': '1C9EwqVzJlKWLzw3VO959bF9SaaT-dp4f'
    }
    
    data_dir = os.path.join('Foodimg2Ing', 'data')
    os.makedirs(data_dir, exist_ok=True)

    for filename, file_id in assets.items():
        output_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(output_path):
            print(f"🚀 Neural Engine: Downloading {filename}...")
            url = f'https://drive.google.com/uc?id={file_id}'
            try:
                gdown.download(url, output_path, quiet=False)
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")
        else:
            print(f"✅ Neural Engine: {filename} verified.")

# 2. RUN THE DOWNLOADER IMMEDIATELY (Before importing app)
download_assets()

# 3. NOW IMPORT THE APP
from Foodimg2Ing import app

if __name__ == '__main__':
    # Ensure the upload folder exists
    upload_path = os.path.join('Foodimg2Ing', 'static', 'images')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"🎨 Created Artisan directory: {upload_path}")

    # Run the server
    # Note: On Render, use host='0.0.0.0' and port=int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=5000, debug=True)