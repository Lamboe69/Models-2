# Test if MediaPipe works
import cv2
import mediapipe as mp
import numpy as np

print("🧪 Testing MediaPipe installation...")

# Test pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Create a dummy image
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# Test processing
results = pose.process(test_image)
print(f"✅ MediaPipe working: {results.pose_landmarks is not None}")

pose.close()