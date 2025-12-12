from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# --- LOAD MODELS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
PROTOTXT = os.path.join(MODEL_DIR, "colorization_deploy_v2.prototxt")
MODEL_WEIGHTS = os.path.join(MODEL_DIR, "colorization_release_v2.caffemodel")
POINTS = os.path.join(MODEL_DIR, "pts_in_hull.npy")

print("Loading AI Brain...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL_WEIGHTS)
pts = np.load(POINTS)

# Add the cluster centers to the model (Essential for color)
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
print("✅ AI Brain Ready!")

@app.post("/colorize")
async def colorize(file: UploadFile = File(...)):
    # 1. Read Image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Scale image to avoid memory errors on large files
    h, w = img.shape[:2]
    if h > 800 or w > 800:
        scale = 800 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        h, w = img.shape[:2]

    # 2. Convert to LAB color space
    # L = Lightness (0-100), A/B = Colors
    img_float = img.astype(np.float32) / 255.0
    img_lab = cv2.cvtColor(img_float, cv2.COLOR_BGR2Lab)
    img_l = img_lab[:, :, 0] # Extract L channel

    # 3. Prepare L channel for the AI (Subtract 50 to center data)
    input_l = cv2.resize(img_l, (224, 224))
    input_l -= 50.0 
    
    # 4. Run AI Inference
    net.setInput(cv2.dnn.blobFromImage(input_l))
    result_ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # 5. Resize prediction back to original size
    result_ab_resized = cv2.resize(result_ab, (w, h))

    # 6. Combine original L with predicted AB
    # We use the original L channel to keep sharpness
    result_lab = np.concatenate((img_l[:, :, np.newaxis], result_ab_resized), axis=2)
    
    # 7. Convert back to RGB
    result_bgr = cv2.cvtColor(result_lab, cv2.COLOR_Lab2BGR)
    result_bgr = np.clip(result_bgr * 255, 0, 255).astype("uint8")

    # Return
    _, encoded_img = cv2.imencode('.png', result_bgr)
    return Response(content=encoded_img.tobytes(), media_type="image/png")