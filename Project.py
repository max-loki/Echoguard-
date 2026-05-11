import librosa
import numpy as np
import joblib
import os


def load_model():
    model_path = 'echoguard_model.joblib'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def extract_features(y, sr):
    mfcc_var = np.var(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20))
    flatness = np.mean(librosa.feature.spectral_flatness(y=y))
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    return np.array([[mfcc_var, flatness, centroid]])


def improved_detection_logic(y, sr):
    model = load_model()
    if model is None:
        return False, 0
    features = extract_features(y, sr)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    is_fake = prediction == 1
    confidence = int(max(probability) * 100)
    return is_fake, confidence