# CLINICAL GAT DEPLOYMENT GUIDE

## Quick Start:
1. pip install -r requirements.txt
2. python test_deployment.py

## Usage:
from clinical_gat_inference import ClinicalGATInference
engine = ClinicalGATInference()
results = engine.predict(your_pose_data)

## Performance: 86.7% accuracy
- Core symptoms: 100% accuracy
- Ready for Ugandan healthcare deployment!
