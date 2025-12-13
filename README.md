# ✨ PixelRevive AI

**PixelRevive** is a computer vision application that restores and colorizes historical black & white photos using Deep Learning.

### 🌐 [View Live Demo](https://pixelreviveai.vercel.app/)

> **⚠️ Infrastructure Note:** The live demo is hosted on a free-tier instance (512MB RAM). Due to the high memory requirements of the CNN model (~450MB), the server may experience "Out of Memory" timeouts under load. **For the best experience, please run the project locally.**

---

## 📸 Demo (Running Locally)
<img width="1920" height="1080" alt="Screenshot (230)" src="https://github.com/user-attachments/assets/d7649053-e6d0-485e-a5d5-d01ac77e792f" />

*Screenshot of the application successfully colorizing an image in a local environment.*

## 🧠 How It Works
The app uses the **Zhang et al. (ECCV 2016)** architecture, a Convolutional Neural Network (CNN) trained on over 1 million images.
1.  **L-Channel Extraction:** The image is converted to the LAB color space.
2.  **Feature Hallucination:** The model analyzes the Lightness (L) channel to predict the A and B (Color) channels.
3.  **Reconstruction:** The predicted colors are merged back with the original sharp L-channel to preserve edge details.

## 🛠️ Tech Stack
* **Frontend:** Next.js 14 (React), Tailwind CSS.
* **Backend:** FastAPI (Python), OpenCV DNN Module.
* **Model:** Caffe (Colorization Release v2).

## 📦 Run Locally (Recommended)
1.  **Clone the repo**
    ```bash
    git clone [https://github.com/Zakaria-ElAlami/PixelRevive-AI.git](https://github.com/Zakaria-ElAlami/PixelRevive-AI.git)
    ```
2.  **Setup Backend** (Auto-downloads the 129MB Model)
    ```bash
    cd backend
    pip install -r requirements.txt
    python setup.py
    uvicorn main:app --reload
    ```
3.  **Setup Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---
**Developed by Zakaria El Alami**
