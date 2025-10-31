import requests
import numpy as np

API_URL = "https://models-2-ctfm.onrender.com"

# Your pose data from MediaPipe/OpenPose
pose_features = np.random.randn(225).tolist()  # Replace with real data

response = requests.post(
    f"{API_URL}/predict",
    json={"pose_features": pose_features}
)

if response.status_code == 200:
    results = response.json()
    print("Clinical Screening Results:")
    for symptom, data in results['predictions'].items():
        print(f"{symptom}: {data['prediction']} ({data['confidence']:.1%})")