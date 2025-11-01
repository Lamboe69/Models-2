import streamlit as st
import numpy as np
from clinical_gat_inference import ClinicalGATInference

@st.cache_resource
def load_model():
    return ClinicalGATInference('clinical_gat_weights.pth')

model = load_model()

st.title("🏥 Quick Clinical GAT Tester")
st.write("Test your model instantly with different input methods")

# Method 1: Instant test
if st.button("🎯 Instant Random Test"):
    pose = np.random.randn(225) * 0.1
    results = model.predict(pose)
    
    st.success("✅ Test completed!")
    for symptom, data in results.items():
        st.write(f"**{symptom}:** {data['prediction']} ({data['confidence']:.1%})")

# Method 2: Gesture simulation
st.subheader("🎭 Simulate Specific Gestures")
gesture = st.selectbox("Choose gesture:", ["Fever", "Cough", "Pain", "Diarrhea", "Random"])

if st.button("🔍 Analyze This Gesture"):
    # Simple simulation based on gesture type
    if gesture == "Fever":
        pose = np.random.randn(225) * 0.3 + 0.2
    elif gesture == "Cough":
        pose = np.random.randn(225) * 0.4 + 0.1
    elif gesture == "Pain":
        pose = np.random.randn(225) * 0.5 + 0.3
    elif gesture == "Diarrhea":
        pose = np.random.randn(225) * 0.2 + 0.4
    else:
        pose = np.random.randn(225) * 0.1
    
    results = model.predict(pose)
    
    st.write(f"**Results for {gesture} gesture:**")
    for symptom, data in results.items():
        icon = "🆘" if data['prediction'] == 'Yes' else "✅"
        st.write(f"{icon} {symptom}: {data['prediction']} ({data['confidence']:.1%})")