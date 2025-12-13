from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os
import requests

app = FastAPI()

# --- BULLETPROOF CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins (Safest for portfolio)
    allow_credentials=True,
    allow_methods=["*"],  # Allow ALL methods (POST, GET, OPTIONS)
    allow_headers=["*"],  # Allow ALL headers
)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
PROTOTXT = os.path.join(MODEL_DIR, "colorization_deploy_v2.prototxt")
MODEL_WEIGHTS = os.path.join(MODEL_DIR, "colorization_release_v2.caffemodel")
POINTS = os.path.join(MODEL_DIR, "pts_in_hull.npy")

# --- SELF-HEALING DOWNLOADER ---
def check_and_download_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    FILES = {
        "colorization_deploy_v2.prototxt": "https://raw.githubusercontent.com/richzhang/colorization/caffe/models/colorization_deploy_v2.prototxt",
        "colorization_release_v2.caffemodel": "https://huggingface.co/spaces/BilalSardar/Black-N-White-To-Color/resolve/main/colorization_release_v2.caffemodel",
        "pts_in_hull.npy": "https://raw.githubusercontent.com/richzhang/colorization/caffe/resources/pts_in_hull.npy"
    }

    for filename, url in FILES.items():
        filepath = os.path.join(MODEL_DIR, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            print(f"📉 Downloading missing file: {filename}...")
            try:
                r = requests.get(url, stream=True)
                r.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Downloaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to download {filename}: {e}")

# Run Check
print("🔍 Checking AI Models...")
check_and_download_models()

# Load Brain
print("🧠 Loading Neural Network...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL_WEIGHTS)
pts = np.load(POINTS)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
print("🚀 AI Ready!")

@app.get("/")
def home():
    return {"status": "PixelRevive Backend Live"}

@app.post("/colorize")
async def colorize(file: UploadFile = File(...)):
    # Read Image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process
    h, w = img.shape[:2]
    if h > 800 or w > 800:
        scale = 800 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        h, w = img.shape[:2]

    img_float = img.astype(np.float32) / 255.0
    img_lab = cv2.cvtColor(img_float, cv2.COLOR_BGR2Lab)
    img_l = img_lab[:, :, 0]
    input_l = cv2.resize(img_l, (224, 224))
    input_l -= 50.0 
    
    net.setInput(cv2.dnn.blobFromImage(input_l))
    result_ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    result_ab_resized = cv2.resize(result_ab, (w, h))
    result_lab = np.concatenate((img_l[:, :, np.newaxis], result_ab_resized), axis=2)
    result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_Lab2BGR)
    result_bgr = np.clip(result_bgr * 255, 0, 255).astype("uint8")

    _, encoded_img = cv2.imencode('.png', result_bgr)
    return Response(content=encoded_img.tobytes(), media_type="image/png")