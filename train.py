import os
import librosa
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("🚀 Starting EchoGuard Training Protocol...")

def extract_features(file_path):
    """Extracts the exact 3 features used in our deployment logic."""
    try:
        # We load only the first 5 seconds to make training much faster
        y, sr = librosa.load(file_path, duration=5) 
        
        mfcc_var = np.var(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20))
        flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        return [mfcc_var, flatness, centroid]
    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")
        return None

# 1. Load Data
features = []
labels = []

# Process Real Audio (Label = 0)
print("Loading Genuine Audio...")
for root, dirs, files in os.walk('data/real'):
    for filename in files:
        if filename.endswith(('.wav', '.mp3')):
            feat = extract_features(os.path.join(root, filename))
            if feat:
                features.append(feat)
                labels.append(0)

# Process Fake Audio (Label = 1)
print("Loading Synthetic Audio...")
for root, dirs, files in os.walk('data/fake'):
    for filename in files:
        if filename.endswith(('.wav', '.mp3')):
            feat = extract_features(os.path.join(root, filename))
            if feat:
                features.append(feat)
                labels.append(1)

# 2. Train the Random Forest
print(f"Data loaded! Training on {len(features)} samples...")
X = np.array(features)
y = np.array(labels)

# Split into training and testing sets to see how well it learned
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 3. Test and Save
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model Trained! Test Accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, 'echoguard_model.joblib')
print("💾 Model saved successfully as 'echoguard_model.joblib'")