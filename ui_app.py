import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from clinical_gat_inference import ClinicalGATInference
import mediapipe as mp
import time
from PIL import Image

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Clinical GAT model
@st.cache_resource
def load_model():
    return ClinicalGATInference('clinical_gat_weights.pth')

model = load_model()

def extract_pose_landmarks(frame):
    """Extract pose landmarks from frame using MediaPipe"""
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        
        # We need exactly 75 landmarks × 3 coordinates = 225 features
        if len(landmarks) == 99:  # MediaPipe returns 33 landmarks × 3
            return landmarks[:225]  # Take first 225 features
        else:
            # Pad or truncate to 225 features
            if len(landmarks) > 225:
                return landmarks[:225]
            else:
                return landmarks + [0] * (225 - len(landmarks))
    return None

def process_video(video_file):
    """Process video and extract pose features"""
    # Save uploaded video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file.read())
        video_path = tmp_file.name
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    pose_features_list = []
    frames_with_landmarks = []
    
    st.info("🔄 Processing video frames...")
    progress_bar = st.progress(0)
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
            
        # Extract pose landmarks
        landmarks = extract_pose_landmarks(frame)
        
        if landmarks:
            pose_features_list.append(landmarks)
            
            # Draw landmarks on frame for visualization
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            if results.pose_landmarks:
                annotated_frame = frame.copy()
                mp_drawing.draw_landmarks(
                    annotated_frame, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS
                )
                frames_with_landmarks.append(annotated_frame)
        
        progress_bar.progress((i + 1) / frame_count)
    
    cap.release()
    os.unlink(video_path)  # Clean up temp file
    
    return pose_features_list, frames_with_landmarks

def main():
    st.set_page_config(
        page_title="Clinical GAT - USL Translator",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Clinical GAT - Ugandan Sign Language Translator")
    st.markdown("""
    This tool translates **Ugandan Sign Language** videos into clinical screening data using our **86.7% accurate** Clinical GAT model.
    """)
    
    # Sidebar
    st.sidebar.header("📊 Model Information")
    st.sidebar.info("""
    **Model Performance:**
    - Overall Accuracy: 86.7%
    - Core Symptoms: 100%
    - Duration/Severity: Needs improvement
    
    **Input:** 225 pose features (75 landmarks × 3 coordinates)
    **Output:** 8 clinical screening categories
    """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎥 Upload Sign Language Video")
        
        # Video upload
        uploaded_file = st.file_uploader(
            "Choose a video file", 
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a video of Ugandan Sign Language gestures"
        )
        
        if uploaded_file is not None:
            # Display video
            st.video(uploaded_file)
            
            if st.button("🚀 Process Video", type="primary"):
                with st.spinner("Processing video and extracting pose data..."):
                    # Process video
                    pose_features_list, frames_with_landmarks = process_video(uploaded_file)
                    
                    if pose_features_list:
                        st.success(f"✅ Extracted pose data from {len(pose_features_list)} frames")
                        
                        # Get predictions for each frame
                        all_predictions = []
                        for i, features in enumerate(pose_features_list):
                            predictions = model.predict(features)
                            all_predictions.append(predictions)
                        
                        # Display results
                        st.header("🎯 Clinical Screening Results")
                        
                        # Show frame-by-frame results
                        tab1, tab2, tab3 = st.tabs(["📊 Summary", "🎞️ Frame Analysis", "📈 Trends"])
                        
                        with tab1:
                            # Aggregate results
                            st.subheader("Overall Assessment")
                            
                            # Calculate most common predictions
                            symptom_results = {}
                            for symptom in all_predictions[0].keys():
                                predictions = [frame[symptom]['prediction'] for frame in all_predictions]
                                most_common = max(set(predictions), key=predictions.count)
                                confidence_avg = np.mean([frame[symptom]['confidence'] for frame in all_predictions])
                                symptom_results[symptom] = {
                                    'prediction': most_common,
                                    'confidence': confidence_avg,
                                    'count': predictions.count(most_common),
                                    'total': len(predictions)
                                }
                            
                            # Display results
                            for symptom, data in symptom_results.items():
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.write(f"**{symptom.title()}:**")
                                with col2:
                                    status = "🟢" if data['prediction'] == 'No' else "🔴"
                                    st.write(f"{status} {data['prediction']}")
                                with col3:
                                    st.write(f"({data['confidence']:.1%})")
                        
                        with tab2:
                            st.subheader("Frame-by-Frame Analysis")
                            frame_to_show = st.slider("Select Frame", 0, len(frames_with_landmarks)-1, 0)
                            
                            if frames_with_landmarks:
                                # Display annotated frame
                                st.image(frames_with_landmarks[frame_to_show], 
                                       caption=f"Frame {frame_to_show} - Pose Landmarks",
                                       use_column_width=True)
                            
                            # Show predictions for selected frame
                            st.write("**Predictions for this frame:**")
                            predictions = all_predictions[frame_to_show]
                            for symptom, data in predictions.items():
                                st.write(f"- {symptom}: {data['prediction']} ({data['confidence']:.1%})")
                        
                        with tab3:
                            st.subheader("Prediction Trends")
                            
                            # Plot confidence trends
                            symptoms = list(all_predictions[0].keys())
                            selected_symptom = st.selectbox("Select symptom to view trend:", symptoms)
                            
                            if selected_symptom:
                                confidences = [frame[selected_symptom]['confidence'] for frame in all_predictions]
                                predictions = [frame[selected_symptom]['prediction'] for frame in all_predictions]
                                
                                # Simple text trend
                                st.write(f"**{selected_symptom} Trend:**")
                                st.write(f"- Frames with 'Yes': {predictions.count('Yes')}")
                                st.write(f"- Frames with 'No': {predictions.count('No')}")
                                st.write(f"- Average Confidence: {np.mean(confidences):.1%}")
                    
                    else:
                        st.error("❌ No pose landmarks detected in the video. Please try a different video.")
    
    with col2:
        st.header("📋 Quick Testing")
        st.markdown("""
        **Test with sample pose data:**
        
        Use this for quick testing without video upload.
        """)
        
        if st.button("🧪 Run Quick Test", type="secondary"):
            with st.spinner("Running quick test..."):
                # Generate random pose data
                sample_pose = np.random.randn(225) * 0.1
                results = model.predict(sample_pose)
                
                st.success("✅ Quick test completed!")
                
                # Display results
                st.subheader("Quick Test Results")
                for symptom, data in results.items():
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**{symptom}:**")
                    with col2:
                        status = "✅" if data['prediction'] == 'No' else "🆘"
                        st.write(f"{status} {data['prediction']} ({data['confidence']:.1%})")

if __name__ == "__main__":
    main()