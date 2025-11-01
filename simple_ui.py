import streamlit as st
import numpy as np
import cv2
import tempfile
import os
from clinical_gat_inference import ClinicalGATInference
from PIL import Image
import io

# Initialize Clinical GAT model
@st.cache_resource
def load_model():
    return ClinicalGATInference('clinical_gat_weights.pth')

model = load_model()

def generate_sample_pose(gesture_type="random"):
    """Generate sample pose data for testing"""
    if gesture_type == "fever":
        # Simulate fever gesture pattern
        return np.random.randn(225) * 0.5 + 0.3
    elif gesture_type == "cough":
        # Simulate cough gesture pattern  
        return np.random.randn(225) * 0.4 + 0.2
    elif gesture_type == "pain":
        # Simulate pain gesture pattern
        return np.random.randn(225) * 0.6 + 0.4
    else:
        # Random gesture
        return np.random.randn(225) * 0.1

def main():
    st.set_page_config(
        page_title="Clinical GAT - USL Testing",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Clinical GAT - Ugandan Sign Language Testing")
    st.markdown("""
    Test your **86.7% accurate** Clinical GAT model with different input methods.
    This simulates pose data extraction from sign language videos.
    """)
    
    # Sidebar
    st.sidebar.header("🔧 Testing Options")
    test_mode = st.sidebar.selectbox(
        "Choose Testing Method",
        ["Manual Input", "Sample Gestures", "Video Upload (Basic)", "Real-time Simulation"]
    )
    
    st.sidebar.info("""
    **Model Performance:**
    - Overall Accuracy: 86.7%
    - Core Symptoms: 100%
    - Input: 225 pose features
    - Output: 8 clinical categories
    """)
    
    # Main content
    if test_mode == "Manual Input":
        st.header("📝 Manual Pose Data Input")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter 225 Pose Features")
            pose_input = st.text_area(
                "Comma-separated values:",
                value=", ".join([f"{x:.4f}" for x in np.random.randn(225) * 0.1]),
                height=150,
                help="Enter 225 numbers representing pose landmarks (x,y,z coordinates for 75 points)"
            )
            
            if st.button("🚀 Predict from Manual Input", type="primary"):
                try:
                    # Parse input
                    features = [float(x.strip()) for x in pose_input.split(",") if x.strip()]
                    
                    if len(features) != 225:
                        st.error(f"❌ Expected 225 features, got {len(features)}")
                    else:
                        with st.spinner("Processing..."):
                            results = model.predict(features)
                        
                        display_results(results)
                        
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            st.subheader("Quick Actions")
            if st.button("🎲 Generate Random Pose"):
                random_pose = np.random.randn(225) * 0.1
                st.session_state.random_pose = ", ".join([f"{x:.4f}" for x in random_pose])
                st.rerun()
            
            if st.button("📋 Copy Sample Format"):
                sample = np.random.randn(225) * 0.1
                st.code(", ".join([f"{x:.4f}" for x in sample]))
    
    elif test_mode == "Sample Gestures":
        st.header("🎭 Test with Sample Gestures")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Choose Gesture Type")
            gesture_type = st.selectbox(
                "Select gesture to simulate:",
                ["random", "fever", "cough", "pain"]
            )
            
            if st.button("🎬 Simulate Gesture", type="primary"):
                with st.spinner("Generating pose data..."):
                    # Generate pose data based on gesture type
                    pose_features = generate_sample_pose(gesture_type)
                    results = model.predict(pose_features)
                
                st.session_state.gesture_results = results
                st.session_state.gesture_type = gesture_type
            
        with col2:
            if 'gesture_results' in st.session_state:
                st.subheader(f"Results for {st.session_state.gesture_type.title()} Gesture")
                display_results(st.session_state.gesture_results)
                
                # Show the generated pose data
                with st.expander("📊 View Generated Pose Data"):
                    pose_features = generate_sample_pose(st.session_state.gesture_type)
                    st.write("First 30 features (of 225):")
                    st.code(", ".join([f"{x:.4f}" for x in pose_features[:30]]))
    
    elif test_mode == "Video Upload (Basic)":
        st.header("🎥 Basic Video Testing")
        st.info("""
        **Note:** This is a basic simulation. In a full implementation, 
        we would use MediaPipe to extract actual pose landmarks from video.
        """)
        
        uploaded_file = st.file_uploader(
            "Upload a sign language video", 
            type=['mp4', 'avi', 'mov'],
            help="For demonstration, we'll simulate pose extraction"
        )
        
        if uploaded_file is not None:
            st.video(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🎯 Process Video (Simulated)", type="primary"):
                    with st.spinner("Simulating video processing..."):
                        # Simulate processing multiple frames
                        frame_results = []
                        for i in range(5):  # Simulate 5 frames
                            pose_features = generate_sample_pose("random")
                            results = model.predict(pose_features)
                            frame_results.append(results)
                        
                        st.session_state.video_results = frame_results
            
            with col2:
                if st.button("🔍 Analyze Specific Gesture"):
                    gesture = st.selectbox("Gesture to analyze:", ["fever", "cough", "diarrhea", "pain"])
                    pose_features = generate_sample_pose(gesture)
                    results = model.predict(pose_features)
                    st.session_state.specific_gesture = results
        
        if 'video_results' in st.session_state:
            st.subheader("🎞️ Simulated Frame Analysis")
            
            frame_to_view = st.slider("Select Frame", 0, len(st.session_state.video_results)-1, 0)
            results = st.session_state.video_results[frame_to_view]
            
            st.write(f"**Frame {frame_to_view + 1} Results:**")
            display_results(results)
    
    elif test_mode == "Real-time Simulation":
        st.header("⏱️ Real-time Gesture Simulation")
        
        st.info("Simulate real-time sign language gesture recognition")
        
        if st.button("🎬 Start Real-time Simulation", type="primary"):
            # Simulate real-time processing
            placeholder = st.empty()
            
            for i in range(10):  # Simulate 10 time steps
                with placeholder.container():
                    # Generate different gesture patterns
                    if i < 3:
                        gesture = "fever"
                    elif i < 6:
                        gesture = "cough" 
                    else:
                        gesture = "random"
                    
                    pose_features = generate_sample_pose(gesture)
                    results = model.predict(pose_features)
                    
                    st.write(f"**Time Step {i + 1}** (Simulating: {gesture} gesture)")
                    display_results(results)
                    
                    # Add small delay for realism
                    import time
                    time.sleep(1)
            
            st.success("✅ Real-time simulation completed!")

def display_results(results):
    """Display prediction results in a nice format"""
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    symptoms = list(results.keys())
    mid_point = len(symptoms) // 2
    
    with col1:
        for symptom in symptoms[:mid_point]:
            data = results[symptom]
            prediction = data['prediction']
            confidence = data['confidence']
            
            # Color code based on prediction and confidence
            if prediction == 'Yes':
                if confidence > 0.7:
                    icon = "🆘"
                    color = "red"
                else:
                    icon = "⚠️" 
                    color = "orange"
            else:
                if confidence > 0.7:
                    icon = "✅"
                    color = "green"
                else:
                    icon = "⚪"
                    color = "gray"
            
            st.markdown(
                f"{icon} **{symptom.title()}:** {prediction} "
                f"<span style='color: {color}; font-weight: bold;'>({confidence:.1%})</span>",
                unsafe_allow_html=True
            )
    
    with col2:
        for symptom in symptoms[mid_point:]:
            data = results[symptom]
            prediction = data['prediction']
            confidence = data['confidence']
            
            if prediction == 'Yes':
                if confidence > 0.7:
                    icon = "🆘"
                    color = "red"
                else:
                    icon = "⚠️"
                    color = "orange"
            else:
                if confidence > 0.7:
                    icon = "✅"
                    color = "green"
                else:
                    icon = "⚪"
                    color = "gray"
            
            st.markdown(
                f"{icon} **{symptom.title()}:** {prediction} "
                f"<span style='color: {color}; font-weight: bold;'>({confidence:.1%})</span>",
                unsafe_allow_html=True
            )
    
    # Summary
    st.markdown("---")
    yes_count = sum(1 for r in results.values() if r['prediction'] == 'Yes')
    high_confidence = sum(1 for r in results.values() if r['confidence'] > 0.7)
    
    st.write(f"**Summary:** {yes_count} symptoms detected, {high_confidence} high-confidence predictions")

if __name__ == "__main__":
    main()