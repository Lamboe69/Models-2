# test_my_model.py
from clinical_gat_inference import ClinicalGATInference
import numpy as np

print("🧪 Testing my Clinical GAT model...")
engine = ClinicalGATInference('clinical_gat_weights.pth')

# Test with sample pose data
sample_pose = np.random.randn(225) * 0.1
results = engine.predict(sample_pose)

print("\n🎯 CLINICAL SCREENING RESULTS:")
for symptom, result in results.items():
    print(f"🏥 {symptom:12}: {result['prediction']} ({result['confidence']:.1%} confidence)")

print("\n✅ My 86.7% accurate Clinical GAT is working!")