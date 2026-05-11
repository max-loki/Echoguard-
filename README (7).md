# EchoGuard — Real-Time Deepfake Audio Detector

> Defending against synthetic voices before they cause real damage.

EchoGuard is an AI-powered security tool that detects deepfake and voice-cloned audio in real-time. It analyzes acoustic patterns imperceptible to the human ear, providing a critical defensive layer as voice synthesis technology grows more sophisticated.

---

## Overview

EchoGuard distinguishes genuine human speech from AI-generated audio through a multi-stage signal processing and machine learning pipeline — delivering results immediately on uploaded audio.

**Key Capabilities:**
- **Real-Time Detection** — Processes WAV/MP3 files and returns classification results instantly.
- **Spectral Feature Extraction** — Extracts MFCC variance, spectral flatness, and spectral centroid as the audio fingerprint.
- **Ensemble Classification** — Random Forest model trained on balanced real/synthetic audio samples.
- **Forensic UI** — Streamlit-based frontend with authenticity scores and confidence reporting.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Frontend | `Streamlit` |
| Audio Processing | `Librosa` |
| Machine Learning | `Scikit-learn` (Random Forest) |
| Model Persistence | `Joblib` |
| Data Handling | `NumPy` |

---

## Project Structure

```
EchoGuard/
├── data/
│   ├── real/               # Genuine human audio samples (.wav / .mp3)
│   └── fake/               # Synthetic / voice-cloned audio samples
├── Project.py              # Core logic: model loading, feature extraction, detection
├── train.py                # Model training pipeline
├── frontend.py             # Streamlit forensic UI
├── test.py                 # Model integrity check
├── echoguard_model.joblib  # Saved Random Forest weights (generated after training)
└── requirements.txt
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EchoGuard.git
cd EchoGuard
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Training the Model

Place your audio files in the `data/` directory:

```
data/
├── real/    # Label 0 — authentic human speech
└── fake/    # Label 1 — AI-generated / cloned audio
```

Then run:

```bash
python train.py
```

This will:
- Extract 3 spectral features from each file (first 5 seconds used per sample)
- Train a Random Forest classifier with 100 estimators
- Print test accuracy to the console
- Save the model as `echoguard_model.joblib`

**Example output:**

```
Starting EchoGuard Training Protocol...
Loading Genuine Audio...
Loading Synthetic Audio...
Data loaded! Training on 1200 samples...
Model Trained! Test Accuracy: 94.17%
Model saved successfully as 'echoguard_model.joblib'
```

---

## Running the App

```bash
streamlit run frontend.py
```

Open your browser at `http://localhost:8501`, upload a WAV or MP3 file, and click **Initiate Forensic Scan**.

The app will display:
- **Authenticity Score** — Probability the audio is genuine
- **AI Probability** — Likelihood the audio is synthetically generated
- A final verdict: `AUTHENTIC` or `SYNTHETIC` with confidence percentage

---

## How It Works

```
Raw Audio  ->  Preprocessing  ->  Feature Extraction  ->  Classification  ->  Verdict
```

**Preprocessing**
Audio is loaded via Librosa, normalized, and trimmed to the first 5 seconds for consistent analysis.

**Feature Extraction (`Project.py`)**

Three spectral features are extracted per sample:

| Feature | Description |
|---|---|
| MFCC Variance | Variance across 20 Mel-Frequency Cepstral Coefficients — captures timbral inconsistencies common in synthetic audio |
| Spectral Flatness | Measures how noise-like a signal is — synthetic voices often show abnormal flatness patterns |
| Spectral Centroid | Weighted mean frequency — reveals unnatural brightness artifacts in cloned voices |

**Classification**
A `RandomForestClassifier` (100 estimators, balanced class weights) evaluates the 3-feature vector and returns both a binary prediction and a confidence probability.

> **Why Random Forest?**
> Handles high-dimensional audio features well, resistant to overfitting, and consistently outperforms single decision trees on real-world noisy audio data.

---

## Verify Model Integrity

```bash
python test.py
```

Expected output:

```
Model loaded successfully!
```

---

## Requirements

```
streamlit
librosa
numpy
scikit-learn
joblib
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

*Built to keep voices honest.*
