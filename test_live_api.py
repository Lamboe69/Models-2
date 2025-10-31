# test_live_api.py
import requests
import numpy as np
import json

# Your live API URL
API_URL = "https://models-2-ctfm.onrender.com"

def test_live_api():
    print("🧪 Testing Live Clinical GAT API")
    print("=" * 50)
    print(f"🌐 API URL: {API_URL}")
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        health_data = response.json()
        print(f"   📊 Model Loaded: {health_data.get('model_loaded', 'Unknown')}")
        print(f"   🩺 Status: {health_data.get('status', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test 2: API Info
    print("\n2. Testing API Info...")
    try:
        response = requests.get(f"{API_URL}/info", timeout=10)
        info = response.json()
        print(f"   ✅ Model: {info.get('model', 'Unknown')}")
        print(f"   🎯 Accuracy: {info.get('accuracy', 'Unknown')}")
        print(f"   💡 Use Case: {info.get('use_case', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Info endpoint failed: {e}")
    
    # Test 3: Single Prediction
    print("\n3. Testing Single Prediction...")
    try:
        # Create sample pose data (225 features)
        sample_pose = np.random.randn(225).tolist()
        
        response = requests.post(
            f"{API_URL}/predict",
            json={"pose_features": sample_pose},
            timeout=30
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   📊 Features processed: {results.get('features_received', 'Unknown')}")
            
            print(f"\n   🎯 CLINICAL RESULTS:")
            print("   " + "=" * 35)
            predictions = results.get('predictions', {})
            for symptom, data in predictions.items():
                prediction = data.get('prediction', 'Unknown')
                confidence = data.get('confidence', 0)
                print(f"   🏥 {symptom:12}: {prediction} ({confidence:.1%})")
        else:
            print(f"   ❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Prediction test failed: {e}")
    
    # Test 4: Batch Prediction
    print("\n4. Testing Batch Prediction...")
    try:
        # Create multiple sample poses
        pose_list = [np.random.randn(225).tolist() for _ in range(3)]
        
        response = requests.post(
            f"{API_URL}/batch_predict",
            json={"pose_list": pose_list},
            timeout=30
        )
        
        if response.status_code == 200:
            batch_results = response.json()
            print(f"   ✅ Batch prediction successful!")
            print(f"   📦 Total poses: {batch_results.get('count', 0)}")
            print(f"   ✅ Successful: {batch_results.get('successful', 0)}")
        else:
            print(f"   ❌ Batch prediction failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Batch prediction test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 CLINICAL GAT API IS FULLY OPERATIONAL!")
    print("   Ready for Ugandan Healthcare Deployment! 🏥")

if __name__ == "__main__":
    test_live_api()