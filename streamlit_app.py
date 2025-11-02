import streamlit as st
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime
import time
import threading
from streamlit.components.v1 import html

# Page config
st.set_page_config(
    page_title="🏥 MediSign - USL Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main App
st.title("🏥 MediSign - USL Healthcare Assistant")
st.markdown("### Medical Sign Language Interface")

# Simple status display
st.info("🤟 Ready for USL communication")

# Initialize session state for analytics
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        'session_start': time.time(),
        'total_sessions': 1,
        'successful_translations': 0,
        'emergency_escalations': 0,
        'patient_to_clinician': 0,
        'clinician_to_patient': 0,
        'current_latency': np.random.randint(150, 250),
        'current_fps': np.random.randint(25, 35),
        'current_memory': np.random.randint(120, 180),
        'clinical_assessments': 0,
        'triage_scores': [],
        'processing_times': [],
        'api_calls': 0,
        'offline_fallbacks': 0,
        'language_usage': {'USL': 0, 'ASL': 0, 'BSL': 0}
    }

# Initialize other session states
if 'live_camera_active' not in st.session_state:
    st.session_state.live_camera_active = False
if 'screening_results' not in st.session_state:
    st.session_state.screening_results = []
if 'system_status' not in st.session_state:
    st.session_state.system_status = "🟢 All Systems Online"

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎥 Live Camera", "🔍 Clinical Screening", "📋 FHIR Results", "📊 Analytics"])

with tab1:
    st.subheader("🎥 Live Camera Feed & USL Recognition")
    
    # Camera controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**📹 Camera Status**")
        if st.session_state.live_camera_active:
            st.success("🟢 Camera Active - Processing USL")
        else:
            st.info("⚪ Camera Standby")
    
    with col2:
        if st.button("🎬 Start Camera", use_container_width=True):
            st.session_state.live_camera_active = True
            st.rerun()
    
    with col3:
        if st.button("⏹️ Stop Camera", use_container_width=True):
            st.session_state.live_camera_active = False
            st.rerun()
    
    # Camera feed placeholder
    camera_placeholder = st.empty()
    
    if st.session_state.live_camera_active:
        with camera_placeholder.container():
            st.markdown("""
            <div style="
                width: 100%; 
                height: 400px; 
                background: linear-gradient(45deg, #1e3c72, #2a5298);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
                border: 2px solid #4CAF50;
            ">
                📹 Live Camera Feed - USL Recognition Active
            </div>
            """, unsafe_allow_html=True)
    else:
        with camera_placeholder.container():
            st.markdown("""
            <div style="
                width: 100%; 
                height: 400px; 
                background: #f0f2f6;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #666;
                font-size: 18px;
                border: 2px dashed #ccc;
            ">
                📷 Camera Feed Inactive
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("🔍 Clinical Screening & Assessment")
    
    # Screening controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Patient Information**")
        patient_id = st.text_input("Patient ID", "PAT-2024-001")
        patient_name = st.text_input("Patient Name", "John Doe")
        
    with col2:
        st.markdown("**🏥 Clinical Context**")
        screening_type = st.selectbox("Screening Type", 
            ["General Assessment", "Emergency Triage", "Routine Checkup", "Specialist Consultation"])
        urgency_level = st.select_slider("Urgency Level", 
            options=["Low", "Medium", "High", "Critical"], value="Medium")
    
    # Start screening
    if st.button("🔍 Start Clinical Screening", use_container_width=True):
        # Simulate screening process
        with st.spinner("Processing clinical assessment..."):
            time.sleep(2)
            
            # Generate mock results
            screening_result = {
                'patient_id': patient_id,
                'patient_name': patient_name,
                'screening_type': screening_type,
                'urgency_level': urgency_level,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'symptoms': ['Chest pain', 'Shortness of breath'],
                'triage_score': np.random.randint(5, 15),
                'recommendations': ['Immediate cardiac evaluation', 'Monitor vital signs']
            }
            
            st.session_state.screening_results.append(screening_result)
            st.session_state.analytics['clinical_assessments'] += 1
            st.session_state.analytics['triage_scores'].append(screening_result['triage_score'])
            
        st.success("✅ Clinical screening completed!")
        st.rerun()
    
    # Display recent results
    if st.session_state.screening_results:
        st.markdown("**📊 Recent Screening Results**")
        latest_result = st.session_state.screening_results[-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Triage Score", f"{latest_result['triage_score']}/20")
        with col2:
            st.metric("Urgency Level", latest_result['urgency_level'])
        with col3:
            st.metric("Symptoms Detected", len(latest_result['symptoms']))

with tab3:
    st.subheader("📋 FHIR-Structured Clinical Results")
    
    if st.session_state.screening_results:
        latest_result = st.session_state.screening_results[-1]
        
        # FHIR Resource Display
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🏥 Clinical Assessment Summary**")
            
            # Patient info
            st.markdown(f"**Patient:** {latest_result['patient_name']} (ID: {latest_result['patient_id']})")
            st.markdown(f"**Assessment Type:** {latest_result['screening_type']}")
            st.markdown(f"**Timestamp:** {latest_result['timestamp']}")
            
            # Clinical findings
            st.markdown("**🔍 Clinical Findings:**")
            for symptom in latest_result['symptoms']:
                st.markdown(f"• {symptom}")
            
            # Recommendations
            st.markdown("**💡 Clinical Recommendations:**")
            for rec in latest_result['recommendations']:
                st.markdown(f"• {rec}")
        
        with col2:
            st.markdown("**⚡ Quick Actions**")
            
            if st.button("🚨 Emergency Alert", use_container_width=True):
                st.error("🚨 Emergency alert sent")
                
            if st.button("📞 Contact Physician", use_container_width=True):
                st.success("📞 Physician contacted")
                
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("📄 Report generated")
        
        st.divider()
        
        # FHIR Resource Summary
        st.markdown("### 📋 FHIR Resource Summary")
        
        fhir_data = pd.DataFrame({
            'Field': ['Resource Type', 'Resource ID', 'Patient ID', 'Status', 'Category', 'System', 'Timestamp'],
            'Value': [
                'Observation',
                f"OBS-{latest_result['patient_id']}-001",
                latest_result['patient_id'],
                'final',
                'Clinical Screening',
                'MediSign Healthcare Assistant',
                latest_result['timestamp']
            ]
        })
        
        st.dataframe(fhir_data, use_container_width=True, hide_index=True)
        
        # Action buttons row
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Export FHIR JSON", use_container_width=True):
                st.success("📤 FHIR JSON exported")
        with col2:
            if st.button("📧 Send to EHR", use_container_width=True):
                st.success("📧 Sent to EHR system")
        with col3:
            if st.button("🖨️ Print Report", use_container_width=True):
                st.success("🖨️ Report printed")
        
    else:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8fafc; border-radius: 12px; border: 2px dashed #cbd5e1;">
            <div style="font-size: 3em; margin-bottom: 1rem;">📋</div>
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 1rem; color: #475569;">No Clinical Data Available</div>
            <div style="color: #64748b; margin-bottom: 2rem;">Process USL input to generate clinical assessment and FHIR-structured results</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("📊 System Performance & Analytics")
    
    # Performance Metrics Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚡ Performance Metrics**")
        
        # Live performance data
        perf_data = pd.DataFrame({
            'Metric': ['Latency (ms)', 'Accuracy (%)', 'FPS', 'Memory (MB)'],
            'Current': [
                st.session_state.analytics['current_latency'],
                86.7,
                st.session_state.analytics['current_fps'],
                st.session_state.analytics['current_memory']
            ],
            'Target': [300, 90, 30, 200]
        })
        
        st.dataframe(perf_data, use_container_width=True)
        st.bar_chart(perf_data.set_index('Metric')[['Current', 'Target']])
    
    with col2:
        st.markdown("**🔄 Session Statistics**")
        
        # Live session stats
        duration_min = (time.time() - st.session_state.analytics['session_start']) / 60
        session_data = pd.DataFrame({
            'Statistic': ['Total Sessions', 'Successful Translations', 'Emergency Escalations', 'Session Duration (min)'],
            'Count': [
                st.session_state.analytics['total_sessions'],
                st.session_state.analytics['successful_translations'],
                st.session_state.analytics['emergency_escalations'],
                f"{duration_min:.1f}"
            ]
        })
        
        st.dataframe(session_data, use_container_width=True)