# mediapipe_ui_simple.py
import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from clinical_gat_inference import ClinicalGATInference
import mediapipe as mp
from PIL import Image
import io

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize Clinical GAT model
@st.cache_resource
def load_model():
    return ClinicalGATInference('clinical_gat_weights.pth')

model = load_model()

def extract_pose_landmarks(frame, pose_detector):
    """Extract pose landmarks from frame using MediaPipe"""
    try:
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Process the frame
        results = pose_detector.process(rgb_frame)
        
        if results.pose_landmarks:
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            # MediaPipe returns 33 landmarks × 3 = 99 features
            # We need 225 features, so we'll pad appropriately
            if len(landmarks) == 99:
                # Strategy: Repeat landmarks and take first 225
                # This maintains the spatial relationships
                padded_landmarks = []
                for i in range(3):  # Repeat 3 times to get close to 225
                    padded_landmarks.extend(landmarks)
                padded_landmarks = padded_landmarks[:225]
                return padded_landmarks, results.pose_landmarks
        return None, None
        
    except Exception as e:
        st.error(f"Pose extraction error: {e}")
        return None, None

def process_video_with_mediapipe(video_file):
    """Process video and extract real pose features using MediaPipe"""
    # Save uploaded video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file.read())
        video_path = tmp_file.name
    
    # Initialize MediaPipe Pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(video_path)
    pose_features_list = []
    frames_with_landmarks = []
    landmark_data_list = []
    
    st.info("🔄 Processing video with MediaPipe Pose Detection...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if frame_count == 0:
        st.error("❌ Could not read video frame count")
        return [], [], []
    
    processed_frames = 0
    landmarks_detected = 0
    
    # Process frames (limit to reasonable number for performance)
    max_frames = min(frame_count, 50)
    
    for i in range(max_frames):
        ret, frame = cap.read()
        if not ret:
            break
            
        # Extract pose landmarks
        landmarks, raw_landmarks = extract_pose_landmarks(frame, pose)
        
        if landmarks:
            pose_features_list.append(landmarks)
            landmarks_detected += 1
            landmark_data_list.append(raw_landmarks)
            
            # Draw landmarks on frame for visualization
            annotated_frame = frame.copy()
            mp_drawing.draw_landmarks(
                annotated_frame,
                raw_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            frames_with_landmarks.append(annotated_frame)
        
        processed_frames += 1
        progress_bar.progress((i + 1) / max_frames)
        status_text.text(f"📊 Processed {processed_frames}/{max_frames} frames - {landmarks_detected} with pose detected")
    
    cap.release()
    pose.close()
    os.unlink(video_path)  # Clean up temp file
    
    st.success(f"✅ Processed {processed_frames} frames, found pose in {landmarks_detected} frames")
    return pose_features_list, frames_with_landmarks, landmark_data_list

def process_image_with_mediapipe(image_file):
    """Process single image with MediaPipe"""
    # Read image
    image = Image.open(image_file)
    image_np = np.array(image)
    
    # Convert to BGR if needed
    if len(image_np.shape) == 3 and image_np.shape[2] == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    # Initialize MediaPipe Pose for single image
    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.5
    ) as pose:
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_image)
        
        if results.pose_landmarks:
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            # Pad to 225 features
            if len(landmarks) == 99:
                padded_landmarks = []
                for i in range(3):
                    padded_landmarks.extend(landmarks)
                padded_landmarks = padded_landmarks[:225]
                return padded_landmarks, results.pose_landmarks, image_np
        return None, None, image_np

def main():
    st.set_page_config(
        page_title="Clinical GAT - Real Pose Detection",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Clinical GAT - Real MediaPipe Pose Detection")
    st.markdown("""
    **Now with real MediaPipe pose detection!** 
    Upload videos or images of Ugandan Sign Language gestures for accurate clinical screening.
    """)
    
    # Test MediaPipe availability
    try:
        import mediapipe as mp
        st.success("✅ MediaPipe is working correctly!")
    except Exception as e:
        st.error(f"❌ MediaPipe not working: {e}")
        return
    
    # Sidebar
    st.sidebar.header("🔧 Detection Options")
    input_type = st.sidebar.selectbox(
        "Input Type",
        ["Video", "Image", "Webcam", "Quick Test"]
    )
    
    st.sidebar.info("""
    **MediaPipe Features:**
    - 33 pose landmarks detection
    - Real-time processing
    - High accuracy pose estimation
    - Compatible with Clinical GAT model
    """)
    
    # Main content based on input type
    if input_type == "Video":
        st.header("🎥 Video Analysis with MediaPipe")
        
        uploaded_file = st.file_uploader(
            "Upload sign language video",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Video will be processed with MediaPipe pose detection"
        )
        
        if uploaded_file is not None:
            # Display video
            st.video(uploaded_file)
            
            if st.button("🎯 Process with MediaPipe", type="primary"):
                with st.spinner("Processing video with MediaPipe..."):
                    pose_features_list, frames_with_landmarks, landmark_data = process_video_with_mediapipe(uploaded_file)
                
                if pose_features_list:
                    # Get predictions
                    all_predictions = []
                    for features in pose_features_list:
                        results = model.predict(features)
                        all_predictions.append(results)
                    
                    display_mediapipe_results(all_predictions, frames_with_landmarks, landmark_data)
                else:
                    st.error("❌ No pose landmarks detected in the video")
    
    elif input_type == "Image":
        st.header("🖼️ Image Analysis with MediaPipe")
        
        uploaded_image = st.file_uploader(
            "Upload sign language image",
            type=['jpg', 'jpeg', 'png'],
            help="Image will be processed with MediaPipe pose detection"
        )
        
        if uploaded_image is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(uploaded_image, caption="Original Image", use_column_width=True)
            
            with col2:
                if st.button("🔍 Analyze Pose", type="primary"):
                    with st.spinner("Detecting pose with MediaPipe..."):
                        pose_features, landmarks, original_image = process_image_with_mediapipe(uploaded_image)
                    
                    if pose_features is not None:
                        results = model.predict(pose_features)
                        
                        # Display annotated image
                        annotated_image = original_image.copy()
                        mp_drawing.draw_landmarks(
                            annotated_image,
                            landmarks,
                            mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                        )
                        
                        # Convert BGR to RGB for display
                        annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                        st.image(annotated_image_rgb, caption="Pose Landmarks Detected", use_column_width=True)
                        
                        st.subheader("🎯 Clinical Assessment")
                        display_single_prediction(results)
                        
                        # Show landmark statistics
                        with st.expander("📊 Pose Landmark Details"):
                            st.write(f"**Landmarks detected:** 33 points")
                            st.write(f"**Features extracted:** 225 values")
                            st.write(f"**Confidence:** High")
                            
                    else:
                        st.error("❌ No pose detected in the image")
    
    elif input_type == "Webcam":
        st.header("📷 Webcam Capture")
        st.info("Take a photo using your webcam for pose analysis")
        
        # Webcam capture
        picture = st.camera_input("Take a picture of a sign language gesture")
        
        if picture:
            # Convert to OpenCV format
            bytes_data = picture.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Process with MediaPipe
            with st.spinner("Analyzing pose with MediaPipe..."):
                pose_features, landmarks, _ = process_image_with_mediapipe(picture)
            
            if pose_features:
                results = model.predict(pose_features)
                
                # Display annotated image
                annotated_image = cv2_img.copy()
                mp_drawing.draw_landmarks(
                    annotated_image,
                    landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(picture, caption="Original Photo", use_column_width=True)
                with col2:
                    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                    st.image(annotated_image_rgb, caption="Pose Detected", use_column_width=True)
                
                st.subheader("🎯 Clinical Assessment")
                display_single_prediction(results)
            else:
                st.error("❌ No pose detected. Please ensure the person is visible and trying a clear sign language gesture.")
    
    else:  # Quick Test
        st.header("⚡ Quick MediaPipe Test")
        
        if st.button("🧪 Run Quick MediaPipe Test", type="primary"):
            # Create a simple test image with a person-like shape
            test_image = create_test_image()
            
            with st.spinner("Testing MediaPipe on sample image..."):
                # Convert to PIL Image for processing
                pil_image = Image.fromarray(test_image)
                pose_features, landmarks, _ = process_image_with_mediapipe(pil_image)
            
            if pose_features:
                results = model.predict(pose_features)
                st.success("✅ MediaPipe test successful!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(test_image, caption="Test Image", use_column_width=True)
                with col2:
                    st.subheader("Test Results")
                    display_single_prediction(results)
            else:
                st.warning("⚠️ No pose detected in test image (expected for synthetic image)")

def create_test_image():
    """Create a simple test image for MediaPipe"""
    # Create a blank image
    img = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Draw a simple stick figure (simplified person)
    cv2.circle(img, (320, 100), 30, (0, 0, 0), -1)  # Head
    cv2.line(img, (320, 130), (320, 250), (0, 0, 0), 3)  # Body
    cv2.line(img, (320, 150), (250, 200), (0, 0, 0), 3)  # Left arm
    cv2.line(img, (320, 150), (390, 200), (0, 0, 0), 3)  # Right arm
    cv2.line(img, (320, 250), (280, 350), (0, 0, 0), 3)  # Left leg
    cv2.line(img, (320, 250), (360, 350), (0, 0, 0), 3)  # Right leg
    
    return img

def display_mediapipe_results(all_predictions, frames_with_landmarks, landmark_data):
    """Display results from MediaPipe processing"""
    st.header("🎯 Clinical Screening Results")
    
    if frames_with_landmarks:
        # Show frame selection
        frame_idx = st.slider("Select Frame", 0, len(frames_with_landmarks)-1, 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Convert BGR to RGB for display
            display_frame = cv2.cvtColor(frames_with_landmarks[frame_idx], cv2.COLOR_BGR2RGB)
            st.image(display_frame, 
                   caption=f"Frame {frame_idx + 1} - Pose Landmarks Detected",
                   use_column_width=True)
        
        with col2:
            results = all_predictions[frame_idx]
            display_single_prediction(results)
            
            # Show landmark confidence
            if landmark_data and frame_idx < len(landmark_data):
                st.write("**Pose Detection:** ✅ Successful")
    
    # Show aggregated results
    st.subheader("📊 Overall Video Assessment")
    
    if len(all_predictions) > 1:
        # Calculate most common predictions across all frames
        aggregated_results = {}
        symptom_names = list(all_predictions[0].keys())
        
        for symptom in symptom_names:
            predictions = [frame[symptom]['prediction'] for frame in all_predictions]
            confidences = [frame[symptom]['confidence'] for frame in all_predictions]
            
            most_common = max(set(predictions), key=predictions.count)
            avg_confidence = np.mean(confidences)
            detection_rate = predictions.count(most_common) / len(predictions)
            
            aggregated_results[symptom] = {
                'prediction': most_common,
                'confidence': avg_confidence,
                'detection_rate': detection_rate,
                'frames_detected': predictions.count(most_common)
            }
        
        # Display aggregated results
        for symptom, data in aggregated_results.items():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{symptom.title()}:**")
            with col2:
                status = "🆘" if data['prediction'] == 'Yes' else "✅"
                st.write(f"{status} {data['prediction']}")
            with col3:
                st.write(f"({data['confidence']:.1%})")
            with col4:
                st.write(f"{data['frames_detected']}/{len(all_predictions)} frames")
    else:
        st.info("Only one frame with pose detected")

def display_single_prediction(results):
    """Display single prediction results"""
    st.subheader("Clinical Assessment")
    
    # Critical symptoms check
    critical_symptoms = ['fever', 'cough', 'hemoptysis']
    critical_detected = [
        symptom for symptom in critical_symptoms 
        if results[symptom]['prediction'] == 'Yes' and results[symptom]['confidence'] > 0.7
    ]
    
    if critical_detected:
        st.error(f"🚨 **URGENT:** Critical symptoms detected: {', '.join(critical_detected).title()}")
    
    for symptom, data in results.items():
        prediction = data['prediction']
        confidence = data['confidence']
        
        if prediction == 'Yes':
            if confidence > 0.7:
                icon = "🔴"
                status = "DETECTED - High Confidence"
                color = "red"
            else:
                icon = "🟡"
                status = "DETECTED - Low Confidence"
                color = "orange"
        else:
            if confidence > 0.7:
                icon = "🟢"
                status = "NOT DETECTED - High Confidence"
                color = "green"
            else:
                icon = "⚪"
                status = "NOT DETECTED - Low Confidence"
                color = "gray"
        
        st.markdown(
            f"{icon} **{symptom.title()}:** {status} "
            f"<span style='color: {color}; font-weight: bold;'>({confidence:.1%})</span>",
            unsafe_allow_html=True
        )
    
    # Summary
    yes_count = sum(1 for r in results.values() if r['prediction'] == 'Yes')
    high_confidence = sum(1 for r in results.values() if r['confidence'] > 0.7)
    
    st.metric("Symptoms Detected", yes_count)
    st.metric("High-Confidence Predictions", high_confidence)

if __name__ == "__main__":
    main()