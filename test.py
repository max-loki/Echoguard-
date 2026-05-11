import joblib
# Try loading the model to ensure it's not corrupted
model = joblib.load('model.pkl')
print("Model loaded successfully!")