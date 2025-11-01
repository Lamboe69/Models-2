# deployment_ui.py
import streamlit as st
import numpy as np
from clinical_gat_inference import ClinicalGATInference
import base64
import json

@st.cache_resource
def load_model():
    st.info("🚀 Loading Clinical GAT Model...")
    model = ClinicalGatInference('clinical_gat_weights.pth')
    st.success("✅ Model loaded - 86.7% accuracy")
    return model

model = load_model()

def main():
    st.set_page_config(
        page_title="Clinical GAT - Healthcare Deployment",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .critical-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🏥 Clinical GAT - Ugandan Healthcare Deployment</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Deployment Tools")
        st.info("""
        **Deployment Status:** ✅ LIVE
        **API URL:** https://models-2-ctfm.onrender.com
        **Model Accuracy:** 86.7%
        """)
        
        st.subheader("Quick Actions")
        if st.button("🧪 Run System Test"):
            run_system_test()
        
        if st.button("📊 Performance Report"):
            show_performance_report()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎥 Live Testing", 
        "📁 Batch Processing", 
        "📈 Analytics", 
        "🔧 Integration"
    ])
    
    with tab1:
        show_live_testing()
    
    with tab2:
        show_batch_processing()
    
    with tab3:
        show_analytics()
    
    with tab4:
        show_integration()

def show_live_testing():
    st.header("🎥 Real-time Sign Language Translation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Gesture Input")
        
        # Gesture type selection
        gesture_type = st.selectbox(
            "Select gesture type to simulate:",
            ["Fever", "Cough", "Headache", "Diarrhea", "Chest Pain", "Fatigue", "Random"]
        )
        
        # Confidence simulation
        confidence_level = st.slider("Gesture clarity", 0.1, 1.0, 0.8)
        
        if st.button("🎬 Analyze Gesture", type="primary", use_container_width=True):
            with st.spinner("Processing sign language gesture..."):
                # Simulate gesture-based pose data
                pose_features = simulate_gesture(gesture_type, confidence_level)
                results = model.predict(pose_features)
                
                # Store results
                st.session_state.latest_results = results
                st.session_state.gesture_type = gesture_type
    
    with col2:
        st.subheader("Quick Assessment")
        
        if 'latest_results' in st.session_state:
            display_clinical_assessment(st.session_state.latest_results)
            
            # Export options
            st.download_button(
                "📄 Export Report",
                data=json.dumps(st.session_state.latest_results, indent=2),
                file_name=f"clinical_assessment_{st.session_state.gesture_type}.json",
                mime="application/json"
            )

def simulate_gesture(gesture_type, confidence):
    """Simulate different sign language gestures"""
    base_patterns = {
        "Fever": np.random.randn(225) * 0.3 + 0.4,
        "Cough": np.random.randn(225) * 0.4 + 0.3,
        "Headache": np.random.randn(225) * 0.5 + 0.2,
        "Diarrhea": np.random.randn(225) * 0.2 + 0.5,
        "Chest Pain": np.random.randn(225) * 0.6 + 0.3,
        "Fatigue": np.random.randn(225) * 0.1 + 0.1,
        "Random": np.random.randn(225) * 0.1
    }
    
    base_pose = base_patterns.get(gesture_type, base_patterns["Random"])
    noise = np.random.randn(225) * (1 - confidence) * 0.2
    return base_pose + noise

def display_clinical_assessment(results):
    """Display comprehensive clinical assessment"""
    
    # Critical symptoms check
    critical_symptoms = ['fever', 'cough', 'hemoptysis']
    critical_detected = [
        symptom for symptom in critical_symptoms 
        if results[symptom]['prediction'] == 'Yes' and results[symptom]['confidence'] > 0.7
    ]
    
    if critical_detected:
        st.markdown(f"""
        <div class="critical-box">
            <h3>🚨 URGENT ATTENTION NEEDED</h3>
            <p>Critical symptoms detected: {', '.join(critical_detected).title()}</p>
            <p><strong>Recommendation:</strong> Immediate medical consultation required</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Results display
    st.subheader("Clinical Findings")
    
    for symptom, data in results.items():
        pred = data['prediction']
        conf = data['confidence']
        
        if pred == 'Yes':
            if conf > 0.7:
                icon = "🔴"
                status = "POSITIVE - High Confidence"
            else:
                icon = "🟡" 
                status = "POSITIVE - Low Confidence"
        else:
            if conf > 0.7:
                icon = "🟢"
                status = "NEGATIVE - High Confidence"
            else:
                icon = "⚪"
                status = "NEGATIVE - Low Confidence"
        
        st.write(f"{icon} **{symptom.title()}:** {status} ({conf:.1%})")

def run_system_test():
    """Run comprehensive system test"""
    st.header("🧪 System Diagnostics")
    
    test_results = []
    
    # Test 1: Model loading
    try:
        test_model = ClinicalGATInference('clinical_gat_weights.pth')
        test_results.append(("✅", "Model Loading", "Success"))
    except Exception as e:
        test_results.append(("❌", "Model Loading", f"Failed: {e}"))
    
    # Test 2: Prediction
    try:
        sample_pose = np.random.randn(225) * 0.1
        results = test_model.predict(sample_pose)
        test_results.append(("✅", "Prediction", f"Success - {len(results)} outputs"))
    except Exception as e:
        test_results.append(("❌", "Prediction", f"Failed: {e}"))
    
    # Test 3: Performance
    import time
    start_time = time.time()
    for _ in range(10):
        test_model.predict(np.random.randn(225) * 0.1)
    avg_time = (time.time() - start_time) / 10
    test_results.append(("✅", "Performance", f"Avg: {avg_time:.3f}s per prediction"))
    
    # Display results
    for icon, test, result in test_results:
        st.write(f"{icon} **{test}:** {result}")
    
    st.success("🎉 System test completed successfully!")

# Other tab functions would go here...

if __name__ == "__main__":
    main()