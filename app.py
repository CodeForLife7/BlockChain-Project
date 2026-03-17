from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import hashlib
import base64
import os

app = Flask(__name__)
CORS(app)

DB_FOLDER = "database_images"
os.makedirs(DB_FOLDER, exist_ok=True)

def decode_image(b64_string):
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]
    img_bytes = base64.b64decode(b64_string)
    nparr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def compute_hash(img_bytes):
    return hashlib.sha256(img_bytes).hexdigest().upper()

def orb_similarity(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=500)
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)
    if des1 is None or des2 is None:
        return 0.0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    good = [m for m in matches if m.distance < 50]
    similarity = len(good) / max(len(kp1), len(kp2), 1) * 100
    return round(min(similarity * 3, 100), 2)

def color_histogram_similarity(img1, img2):
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0,256,0,256,0,256])
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0,256,0,256,0,256])
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return round(max(score, 0) * 100, 2)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    uploaded_img = decode_image(data["image"])
    img_bytes = base64.b64decode(data["image"].split(",")[1] if "," in data["image"] else data["image"])
    img_hash = compute_hash(img_bytes)

    results = []
    for fname in os.listdir(DB_FOLDER):
        if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
            continue
        db_img = cv2.imread(os.path.join(DB_FOLDER, fname))
        if db_img is None:
            continue
        orb_score = orb_similarity(uploaded_img, db_img)
        color_score = color_histogram_similarity(uploaded_img, db_img)
        combined = round(orb_score * 0.6 + color_score * 0.4, 2)
        results.append({"name": fname, "orb": orb_score, "color": color_score, "similarity": combined})

    results.sort(key=lambda x: x["similarity"], reverse=True)
    top_sim = results[0]["similarity"] if results else 0
    originality_score = round(max(5, min(99, 100 - top_sim)))

    return jsonify({
        "hash": img_hash,
        "originality_score": originality_score,
        "top_similarity": top_sim,
        "matches": results[:5],
        "verdict": "ORIGINAL" if originality_score > 70 else "SUSPICIOUS" if originality_score > 40 else "DUPLICATE"
    })

@app.route("/register", methods=["POST"])
def register():
    """Add an image to the known database"""
    data = request.json
    if not data or "image" not in data or "name" not in data:
        return jsonify({"error": "Missing image or name"}), 400
    img = decode_image(data["image"])
    path = os.path.join(DB_FOLDER, f"{data['name']}.png")
    cv2.imwrite(path, img)
    return jsonify({"success": True, "registered": data["name"]})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "db_size": len(os.listdir(DB_FOLDER))})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
