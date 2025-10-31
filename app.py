from flask import Flask, request, jsonify
from clinical_gat_inference import ClinicalGATInference
import numpy as np
import os

app = Flask(__name__)

# Initialize model
print("🚀 Loading Clinical GAT Model...")
engine = ClinicalGATInference('clinical_gat_weights.pth')
print("✅ Model loaded successfully!")

@app.route('/')
def home():
    return jsonify({
        "message": "Clinical GAT API - Ugandan Sign Language Healthcare",
        "status": "healthy",
        "accuracy": "86.7%",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "model": "Clinical GAT 86.7%"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        if not data or 'pose_features' not in data:
            return jsonify({"error": "No pose_features provided"}), 400
        
        pose_features = np.array(data['pose_features'])
        
        # Validate input
        if len(pose_features.shape) != 1:
            return jsonify({"error": "pose_features must be 1D array"}), 400
        
        # Get predictions
        results = engine.predict(pose_features)
        
        return jsonify({
            "status": "success",
            "predictions": results,
            "model_accuracy": "86.7%"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    try:
        data = request.json
        
        if not data or 'pose_list' not in data:
            return jsonify({"error": "No pose_list provided"}), 400
        
        pose_list = [np.array(pose) for pose in data['pose_list']]
        results = [engine.predict(pose) for pose in pose_list]
        
        return jsonify({
            "status": "success",
            "predictions": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)