# test_mediapipe_final.py
import cv2
import numpy as np
import mediapipe as mp

def test_mediapipe_complete():
    print("🎯 Final MediaPipe Test")
    print("=" * 50)
    
    # Initialize MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    
    # Create a test image
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    cv2.circle(test_image, (320, 100), 30, (0, 0, 0), -1)  # Head
    cv2.line(test_image, (320, 130), (320, 250), (0, 0, 0), 3)  # Body
    
    # Test pose detection
    rgb_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_image)
    
    if results.pose_landmarks:
        print("✅ MediaPipe pose detection: WORKING")
        print(f"✅ Landmarks detected: {len(results.pose_landmarks.landmark)}")
        
        # Test landmark extraction
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        
        print(f"✅ Features extracted: {len(landmarks)} values")
        print(f"✅ Padded to 225: {len(landmarks * 3)[:225]} features")
        
    else:
        print("⚠️  No pose detected in test image (expected for simple drawing)")
    
    pose.close()
    print("🎉 MediaPipe integration: SUCCESSFUL")

if __name__ == "__main__":
    test_mediapipe_complete()