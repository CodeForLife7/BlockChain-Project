# ORIGN — AI-Powered NFT Art Originality Checker

> A "Digital Customs Office" for NFTs. Upload any artwork — our AI scans it, compares it against known works, and issues a blockchain-sealed Proof of Originality certificate.

![ORIGN Banner](https://img.shields.io/badge/ORIGN-v3.0-5dffb6?style=for-the-badge&labelColor=060608)
![AI Powered](https://img.shields.io/badge/AI-Claude%20Sonnet-5d9fff?style=for-the-badge&labelColor=060608)
![License](https://img.shields.io/badge/License-MIT-ffd45d?style=for-the-badge&labelColor=060608)

---

## Features

- **AI Analysis** — Real Claude AI writes a personalized originality report for every scan
- **Feature Extraction** — Extracts colors, brightness, saturation, edge density, warmth via Canvas API
- **SHA-256 Fingerprinting** — Unique cryptographic hash for every artwork
- **Similarity Matching** — Cosine similarity on color vectors (like ORB/SIFT in OpenCV)
- **Blockchain Certificate** — Simulated on-chain Proof of Originality with block number + timestamp
- **Compare Tool** — Side-by-side visual diffing of any two artworks
- **Scan History** — Full audit log of all scans
- **10-Artwork Database** — Pre-loaded with known originals and high-risk clones

---

## Live Demo

Open `index.html` in any browser — no install needed.

Or deploy instantly with GitHub Pages:

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → main branch → / (root)**
3. Your app is live at `https://YOUR_USERNAME.github.io/orign-nft`

---

## How It Works

```
Upload Artwork
      ↓
Feature Extraction (Canvas API)
  → Color vectors, brightness, saturation, edge density
      ↓
SHA-256 Fingerprint (CryptoJS)
      ↓
Database Comparison (Cosine Similarity)
  → Checks against 10 known artworks
      ↓
Originality Score (0–100%)
  → 70%+ = Original  |  40–70% = Suspicious  |  <40% = Duplicate
      ↓
Claude AI Analysis (Anthropic API)
  → Personalized written report streamed live
      ↓
Blockchain Certificate (Simulated)
  → Block number + TX hash + timestamp sealed
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS (zero dependencies) |
| Image Analysis | Canvas API (feature extraction) |
| Hashing | CryptoJS SHA-256 |
| AI Analysis | Anthropic Claude Sonnet API |
| Fonts | Bebas Neue + DM Sans + Space Mono (Google Fonts) |
| Blockchain | Simulated (extensible to Ethereum/Solidity) |

---

## Extending to Production

### Real Image Comparison (Python Backend)
```python
import cv2
import numpy as np

def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    similarity = len(matches) / max(len(kp1), len(kp2)) * 100
    return round(similarity, 2)
```

### Real Blockchain (Solidity Smart Contract)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OriginalityRegistry {
    struct Certificate {
        bytes32 imageHash;
        uint8   originalityScore;
        address creator;
        uint256 timestamp;
        bool    approved;
    }

    mapping(bytes32 => Certificate) public certificates;

    event CertificateIssued(bytes32 indexed imageHash, address creator, uint8 score);

    function issueCertificate(bytes32 imageHash, uint8 score) external {
        require(score >= 70, "Score too low to mint");
        require(certificates[imageHash].timestamp == 0, "Already registered");
        certificates[imageHash] = Certificate(imageHash, score, msg.sender, block.timestamp, true);
        emit CertificateIssued(imageHash, msg.sender, score);
    }

    function verifyCertificate(bytes32 imageHash) external view returns (bool) {
        return certificates[imageHash].approved;
    }
}
```

---

## Project Structure

```
orign-nft/
├── index.html        ← Full app (single file, runs in browser)
├── README.md         ← This file
├── LICENSE           ← MIT License
└── backend/          ← (Optional) Python backend for real ORB matching
    ├── app.py
    └── requirements.txt
```

---

## Competition Pitch

> "Every year, millions of dollars of stolen digital art gets minted as NFTs. ORIGN is the world's first AI-powered Digital Customs Office — before you mint, we verify. In 6 seconds, our system extracts visual fingerprints, cross-references a copyright database, gets a live AI verdict, and seals a Proof of Originality on the blockchain. No lawyers. No delays. Just trust."

---

## License

MIT — free to use, extend, and deploy.

---

*Built with Claude AI · ORIGN v3.0*
