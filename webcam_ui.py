# webcam_ui.py
import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from clinical_gat_inference import ClinicalGATInference
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import threading
import queue

# Initialize model
@st.cache_resource
def load_model():
    return ClinicalGATInference('clinical_gat_weights.pth')

model = load_model()

# Simple pose simulation (replace with MediaPipe when fixed)
def simulate_pose_extraction(frame):
    """Simulate pose extraction - replace with actual MediaPipe later"""
    # For now, generate random pose data based on frame characteristics
    frame_variance = np.var(frame) / 1000  # Use frame variance as gesture indicator
    pose_data = np.random.randn(225) * (0.1 + frame_variance)
    return pose_data

def main():
    st.set_page_config(
        page_title="Clinical GAT - Live Testing",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 Clinical GAT - Live Sign Language Testing")
    st.markdown("""
    **Test real-time Ugandan Sign Language translation using your webcam**
    """)
    
    # Testing options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🖥️ Webcam Testing")
        
        # Webcam input
        st.info("""
        **Instructions:**
        1. Allow camera access when prompted
        2. Perform Ugandan Sign Language gestures
        3. View real-time clinical predictions
        """)
        
        # Simple webcam capture
        picture = st.camera_input("Take a picture of sign language gesture")
        
        if picture:
            # Convert to OpenCV format
            bytes_data = picture.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Simulate pose extraction
            with st.spinner("Extracting pose features..."):
                pose_features = simulate_pose_extraction(cv2_img)
                results = model.predict(pose_features)
            
            # Display results
            st.subheader("🎯 Clinical Assessment")
            display_live_results(results)
            
            # Show the captured image
            st.image(picture, caption="Captured Gesture", use_column_width=True)
    
    with col2:
        st.header("📊 Quick Tests")
        
        # Pre-defined gesture tests
        st.subheader("Common Symptoms")
        
        symptoms = ["Fever", "Cough", "Headache", "Stomach Pain", "Fatigue"]
        
        for symptom in symptoms:
            if st.button(f"🔍 Test {symptom}"):
                # Generate appropriate pose simulation
                if symptom == "Fever":
                    pose = np.random.randn(225) * 0.3 + 0.4
                elif symptom == "Cough":
                    pose = np.random.randn(225) * 0.4 + 0.3
                elif symptom == "Headache":
                    pose = np.random.randn(225) * 0.5 + 0.2
                elif symptom == "Stomach Pain":
                    pose = np.random.randn(225) * 0.2 + 0.5
                else:
                    pose = np.random.randn(225) * 0.1
                
                results = model.predict(pose)
                st.session_state.quick_results = results
                st.session_state.quick_symptom = symptom
        
        if 'quick_results' in st.session_state:
            st.subheader(f"Results for {st.session_state.quick_symptom}")
            display_live_results(st.session_state.quick_results)

def display_live_results(results):
    """Display results for live testing"""
    # Create emergency alert for critical symptoms
    critical_symptoms = ['fever', 'cough', 'hemoptysis']
    has_critical = any(results[s]['prediction'] == 'Yes' for s in critical_symptoms)
    
    if has_critical:
        st.error("🚨 CRITICAL SYMPTOMS DETECTED - URGENT CARE NEEDED")
    
    # Display results in columns
    col1, col2 = st.columns(2)
    
    symptoms = list(results.keys())
    mid = len(symptoms) // 2
    
    with col1:
        for symptom in symptoms[:mid]:
            data = results[symptom]
            display_symptom_result(symptom, data)
    
    with col2:
        for symptom in symptoms[mid:]:
            data = results[symptom]
            display_symptom_result(symptom, data)
    
    # Summary statistics
    yes_count = sum(1 for r in results.values() if r['prediction'] == 'Yes')
    total_confidence = np.mean([r['confidence'] for r in results.values()])
    
    st.metric("Symptoms Detected", yes_count)
    st.metric("Average Confidence", f"{total_confidence:.1%}")

def display_symptom_result(symptom, data):
    """Display individual symptom result"""
    prediction = data['prediction']
    confidence = data['confidence']
    
    if prediction == 'Yes':
        if confidence > 0.7:
            icon = "🔴"
            color = "red"
        else:
            icon = "🟡"
            color = "orange"
    else:
        if confidence > 0.7:
            icon = "🟢"
            color = "green"
        else:
            icon = "⚪"
            color = "gray"
    
    st.markdown(
        f"{icon} **{symptom.title()}:** {prediction} "
        f"<span style='color: {color}'>({confidence:.1%})</span>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()