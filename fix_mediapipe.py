# fix_mediapipe.py
import subprocess
import sys
import os

def fix_mediapipe_installation():
    print("🔧 Fixing MediaPipe Installation...")
    print("=" * 50)
    
    # Step 1: Uninstall problematic packages
    print("1. Removing current installations...")
    packages_to_remove = ["numpy", "mediapipe"]
    
    for package in packages_to_remove:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            print(f"   ✅ Uninstalled {package}")
        except subprocess.CalledProcessError:
            print(f"   ℹ️  {package} not installed or couldn't be uninstalled")
    
    # Step 2: Install compatible versions
    print("\n2. Installing compatible versions...")
    compatible_packages = [
        "numpy<1.24",  # Version compatible with MediaPipe
        "mediapipe",   # Latest MediaPipe
        "opencv-python",
        "protobuf<4.0"  # Some versions have compatibility issues
    ]
    
    for package in compatible_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
    
    # Step 3: Test installation
    print("\n3. Testing installation...")
    try:
        import numpy as np
        import mediapipe as mp
        print(f"   ✅ NumPy version: {np.__version__}")
        print(f"   ✅ MediaPipe version: {mp.__version__}")
        print("   🎉 MediaPipe is now working correctly!")
        
        # Test pose detection
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        print("   ✅ Pose detection initialized successfully")
        pose.close()
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if fix_mediapipe_installation():
        print("\n🎉 Fix completed successfully!")
        print("You can now run the MediaPipe-enabled UI:")
        print("streamlit run working_mediapipe_ui.py")
    else:
        print("\n❌ Fix failed. Please try the manual steps:")
        print("1. pip uninstall numpy mediapipe -y")
        print('2. pip install "numpy<1.24" mediapipe')
        print("3. Restart your application")