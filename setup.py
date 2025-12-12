import os
import requests

# MIRROR LINKS (Tested & Working)
FILES = {
    "colorization_deploy_v2.prototxt": "https://raw.githubusercontent.com/richzhang/colorization/caffe/models/colorization_deploy_v2.prototxt",
    "colorization_release_v2.caffemodel": "https://huggingface.co/spaces/BilalSardar/Black-N-White-To-Color/resolve/main/colorization_release_v2.caffemodel",
    "pts_in_hull.npy": "https://raw.githubusercontent.com/richzhang/colorization/caffe/resources/pts_in_hull.npy"
}

# Target: backend/models
SAVE_DIR = os.path.join("backend", "models")
os.makedirs(SAVE_DIR, exist_ok=True)

print(f"🚀 Starting download to {SAVE_DIR}...")

for filename, url in FILES.items():
    filepath = os.path.join(SAVE_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Done: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n🎉 Files ready!")