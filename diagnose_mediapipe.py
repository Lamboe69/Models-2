# diagnose_mediapipe.py
import sys
import numpy as np
import subprocess
import importlib

def diagnose_environment():
    print("🔍 Diagnosing MediaPipe Environment...")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # Check numpy version
    print(f"📊 NumPy Version: {np.__version__}")
    
    # Check if numpy has dtypes attribute
    print(f"🔧 NumPy has 'dtypes': {hasattr(np, 'dtypes')}")
    
    # Check available numpy attributes
    numpy_attrs = [attr for attr in dir(np) if not attr.startswith('_')]
    print(f"📋 NumPy attributes (first 20): {numpy_attrs[:20]}")
    
    # Try to import mediapipe step by step
    print("\n🧪 Testing MediaPipe Import...")
    try:
        import mediapipe as mp
        print("✅ mediapipe imported successfully")
        print(f"📦 MediaPipe Version: {mp.__version__}")
    except Exception as e:
        print(f"❌ MediaPipe import failed: {e}")
        return False
    
    # Test specific MediaPipe components
    print("\n🔧 Testing MediaPipe Components...")
    try:
        from mediapipe.python import solutions
        print("✅ mediapipe.solutions imported")
    except Exception as e:
        print(f"❌ solutions import failed: {e}")
    
    try:
        mp_pose = mp.solutions.pose
        print("✅ mediapipe.solutions.pose imported")
    except Exception as e:
        print(f"❌ pose import failed: {e}")
    
    return True

if __name__ == "__main__":
    diagnose_environment()