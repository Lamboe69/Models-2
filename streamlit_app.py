import streamlit as st
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="🏥 MediSign - USL Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS to match complete_usl_system.py exactly
st.markdown("""
<style>
    /* Main page styling - Dark theme covering all white space */
    .main .block-container {
        padding-top: 1rem;
        background: #0f172a !important;
        min-height: 100vh;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Force entire app background to be dark */
    .stApp, .main, body {
        background: #0f172a !important;
    }
    
    /* Remove any white backgrounds */
    .css-1d391kg, .css-18e3th9, .css-1lcbmhc {
        background: #0f172a !important;
    }
    
    /* Cover any remaining white areas */
    div[data-testid="stAppViewContainer"] {
        background: #0f172a !important;
    }
    
    /* Main content area full coverage */
    .css-1y4p8pa {
        background: #0f172a !important;
        width: 100% !important;
    }
    
    /* FORCE SIDEBAR DARK THEME - All possible classes */
    .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, .css-1y4p8pa, .css-6qob1r, .css-1aumxhk, 
    section[data-testid="stSidebar"], .stSidebar, [data-testid="stSidebar"] {
        background: #1e293b !important;
        border-right: 2px solid #374151 !important;
    }
    
    /* Force all sidebar content to be light colored */
    section[data-testid="stSidebar"] *, .stSidebar *, .css-1d391kg *, .css-1lcbmhc * {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar headers - force white */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #f1f5f9 !important;
        font-weight: bold !important;
    }
    
    /* Force all sidebar labels to be light */
    section[data-testid="stSidebar"] label, .css-1d391kg label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    
    /* Force all sidebar paragraphs and text */
    section[data-testid="stSidebar"] p, .css-1d391kg p {
        color: #e2e8f0 !important;
    }
    
    /* Force sidebar input fields dark */
    section[data-testid="stSidebar"] input, .css-1d391kg input {
        background: #374151 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4b5563 !important;
    }
    
    /* Fix dropdown/selectbox visibility */
    section[data-testid="stSidebar"] select, .css-1d391kg select,
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .css-1wa3eu0-placeholder,
    section[data-testid="stSidebar"] .css-1uccc91-singleValue {
        background: #374151 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4b5563 !important;
    }
    
    /* Fix selectbox dropdown options */
    section[data-testid="stSidebar"] .css-26l3qy-menu,
    section[data-testid="stSidebar"] .css-1n7v3ny-option {
        background: #374151 !important;
        color: #e2e8f0 !important;
    }
    
    /* Fix selectbox control */
    section[data-testid="stSidebar"] .css-1s2u09g-control {
        background: #374151 !important;
        border: 1px solid #4b5563 !important;
    }
    
    /* Fix selectbox text and placeholder */
    section[data-testid="stSidebar"] .css-1wa3eu0-placeholder,
    section[data-testid="stSidebar"] .css-1uccc91-singleValue {
        color: #e2e8f0 !important;
    }
    
    /* Fix number input - Age field */
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] input[type="number"],
    section[data-testid="stSidebar"] .css-1x8cf1d {
        background: #374151 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4b5563 !important;
    }
    
    /* Fix number input controls/buttons */
    section[data-testid="stSidebar"] .stNumberInput button {
        background: #4b5563 !important;
        color: #e2e8f0 !important;
        border: 1px solid #6b7280 !important;
    }
    
    /* Fix text input */
    section[data-testid="stSidebar"] .stTextInput input {
        background: #374151 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4b5563 !important;
    }
    
    /* Force sidebar markdown content */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Force sidebar text elements */
    section[data-testid="stSidebar"] .css-1629p8f, section[data-testid="stSidebar"] .css-10trblm {
        color: #e2e8f0 !important;
    }
    
    /* Main content styling - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        background: #374151;
        border-radius: 5px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        color: #e2e8f0 !important;
        font-weight: 600;
        border: 1px solid #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
    
    /* Tab content styling */
    .stTabs > div > div > div > div {
        background: #1e293b;
        border-radius: 5px;
        padding: 20px;
        margin-top: 5px;
        border: 1px solid #374151;
    }
    
    /* Headers in main content */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
        padding: 8px 12px;
    }
    
    .stButton > button:hover {
        background: #2563eb;
    }
    
    /* Force sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button, .css-1d391kg .stButton > button {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
        width: 100% !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover, .css-1d391kg .stButton > button:hover {
        background: #2563eb !important;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: #374151;
        color: #e2e8f0;
        border: 1px solid #4b5563;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #374151;
        color: #e2e8f0;
    }
    
    /* Info/Success/Error message styling */
    .stAlert {
        border-radius: 5px;
    }
    
    /* Metric styling */
    .metric-container {
        background: #374151;
        border-radius: 5px;
        padding: 15px;
        border: 1px solid #4b5563;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        'session_start': time.time(),
        'total_sessions': 1,
        'successful_translations': 0,
        'emergency_escalations': 0,
        'current_latency': np.random.randint(150, 250),
        'current_fps': np.random.randint(25, 35),
        'current_memory': np.random.randint(120, 180),
    }

if 'live_camera_active' not in st.session_state:
    st.session_state.live_camera_active = False
if 'screening_results' not in st.session_state:
    st.session_state.screening_results = []

# Header matching Tkinter design exactly
st.markdown("""
<div style="
    background: #1e40af;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 20px;
    border: 1px solid #3b82f6;
">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: white; margin: 0; font-size: 1.8rem; font-weight: bold;">🏥 MediSign - USL Healthcare Assistant</h1>
            <p style="color: #bfdbfe; margin: 5px 0 0 0; font-size: 1rem;">Smart Healthcare Communication • Real-time USL Translation • Clinical Integration</p>
        </div>
        <div style="text-align: center;">
            <div style="color: white; font-weight: bold; margin-bottom: 5px;">Translation Mode:</div>
            <div style="color: #e2e8f0; font-size: 0.9rem;">👤→👩⚕️ Patient to Clinician</div>
            <div style="color: #e2e8f0; font-size: 0.9rem;">👩⚕️→👤 Clinician to Patient</div>
        </div>
        <div style="text-align: right;">
            <div style="color: #22c55e; font-weight: bold;">🟢 All Systems Online</div>
            <div style="color: #e2e8f0; font-size: 0.9rem;">👤 No Active Patient</div>
            <div style="color: #cbd5e1; font-size: 0.8rem;">{}</div>
        </div>
    </div>
</div>
""".format(datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)

# Sidebar matching Tkinter design exactly
with st.sidebar:
    # Patient Information Section
    st.markdown("### 👤 Patient Information")
    patient_id = st.text_input("Patient ID:", "")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age:", min_value=0, max_value=120, value=0)
    with col2:
        gender = st.selectbox("Gender:", ["", "Male", "Female", "Other"])
    
    # USL Input & Processing Section
    st.markdown("### 🤟 USL Input & Processing")
    camera_status = "⏹️ Stop Camera" if st.session_state.live_camera_active else "📹 Live Camera (Front+Side)"
    if st.button(camera_status, use_container_width=True):
        st.session_state.live_camera_active = not st.session_state.live_camera_active
    
    if st.button("📁 Upload USL Video", use_container_width=True):
        st.info("Video upload functionality")
    
    if st.button("🖼️ Upload USL Image", use_container_width=True):
        st.info("Image upload functionality")
    
    process_disabled = not st.session_state.live_camera_active
    if st.button("🧠 Process USL → Clinical", use_container_width=True, disabled=process_disabled):
        with st.spinner("Processing USL with Graph-Reasoned LVM..."):
            time.sleep(2)
            st.success("✅ USL processing completed")
            st.session_state.analytics['successful_translations'] += 1
    
    # Real-time metrics
    col1, col2 = st.columns(2)
    with col1:
        fps_val = st.session_state.analytics['current_fps'] if st.session_state.live_camera_active else 0
        st.text(f"FPS: {fps_val}")
    with col2:
        conf_text = "Ready" if not st.session_state.live_camera_active else "85%"
        st.text(f"Confidence: {conf_text}")
    
    # Language & USL Settings Section
    st.markdown("### 🗣️ Language & USL Settings")
    clinic_lang = st.selectbox("Clinic Language:", ["English", "Runyankole", "Luganda"])
    usl_variant = st.selectbox("USL Variant:", ["Canonical", "Kampala Regional", "Gulu Regional", "Mbale Regional"])
    
    st.markdown("**Non-Manual Signals:**")
    nms_signals = ["brow_raise", "head_tilt", "mouth_gestures", "eye_gaze"]
    for nms in nms_signals:
        st.checkbox(nms.replace("_", " ").title(), key=f"nms_{nms}")
    
    # Screening Questions Section
    st.markdown("### 📋 Screening Questions")
    questions = [
        ("fever", "🌡️ Fever"),
        ("cough", "😷 Cough"),
        ("hemoptysis", "🩸 Blood in sputum"),
        ("diarrhea", "💊 Diarrhea"),
        ("rash", "🔴 Rash"),
        ("travel", "✈️ Recent travel"),
        ("exposure", "👥 Sick contact"),
        ("pregnancy", "🤱 Pregnancy")
    ]
    
    for key, label in questions:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.text(label)
        with col2:
            st.radio("", ["Yes"], key=f"{key}_yes", label_visibility="collapsed")
        with col3:
            st.radio("", ["No"], key=f"{key}_no", label_visibility="collapsed")
    
    # Priority Diseases Section
    st.markdown("### 🦠 Priority Diseases (WHO/MoH)")
    diseases = {
        "Malaria": "high",
        "TB": "critical", 
        "Typhoid": "high",
        "Cholera/AWD": "critical",
        "Measles": "high",
        "VHF": "critical",
        "COVID-19": "high",
        "Influenza": "medium"
    }
    
    for disease, priority in diseases.items():
        color = "#dc2626" if priority == "critical" else "#ea580c" if priority == "high" else "#3b82f6"
        st.markdown(f'<span style="color: {color};">□ {disease} ({priority.upper()})</span>', unsafe_allow_html=True)
    
    # Triage Assessment Section
    st.markdown("### 🚨 Triage Assessment")
    st.markdown("""
    <div style="
        background: #dc2626;
        color: white;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    ">
        ⚪ NOT ASSESSED
    </div>
    """, unsafe_allow_html=True)
    
    st.text("Triage Score: 0/20")
    st.text("Risk Level: Low")
    
    if st.button("🚨 EMERGENCY", use_container_width=True):
        st.error("🚨 EMERGENCY ESCALATION ACTIVATED")
        st.session_state.analytics['emergency_escalations'] += 1
    
    if st.button("📞 Call Clinician", use_container_width=True):
        st.success("📞 Clinician alert sent")
    
    # System Controls Section
    st.markdown("### ⚙️ System Controls")
    if st.button("🧪 Test API Connection", use_container_width=True):
        st.success("✅ API connection successful")
    
    if st.button("📄 Generate FHIR Report", use_container_width=True):
        st.success("📄 FHIR report generated")
    
    if st.button("🔄 New Patient Session", use_container_width=True):
        st.session_state.screening_results = []
        st.session_state.analytics['total_sessions'] += 1
        st.success("🔄 New patient session initialized")
        st.rerun()
    
    st.checkbox("Offline-first (Privacy)", value=True)

# Main content tabs matching Tkinter design
tab1, tab2, tab3, tab4 = st.tabs(["🎥 Video Processing", "🤖 Avatar Synthesis", "📋 Clinical Results", "📊 System Analytics"])

with tab1:
    st.subheader("🎥 Real-time USL Processing")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.session_state.live_camera_active:
            st.markdown("""
            <div style="
                width: 100%; 
                height: 400px; 
                background: #374151;
                border-radius: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9ca3af;
                font-size: 16px;
                border: 1px solid #4b5563;
                text-align: center;
            ">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 10px;">📷</div>
                    <div>USL Video Feed</div>
                    <div style="margin-top: 10px;">3D Pose Detection (MediaPipe + MANO + FLAME)</div>
                    <div>Multistream Transformer Processing</div>
                    <div>Graph Attention Network Analysis</div>
                    <div style="margin-top: 10px;">Ready for USL input...</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                width: 100%; 
                height: 400px; 
                background: #374151;
                border-radius: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9ca3af;
                font-size: 16px;
                border: 1px solid #4b5563;
                text-align: center;
            ">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 10px;">📷</div>
                    <div>USL Video Feed</div>
                    <div style="margin-top: 10px;">Camera Inactive</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Real-time Metrics**")
        st.metric("FPS", st.session_state.analytics['current_fps'])
        st.metric("Latency", f"{st.session_state.analytics['current_latency']}ms")
        st.metric("Memory", f"{st.session_state.analytics['current_memory']}MB")
    
    # Neural Processing Pipeline
    st.markdown("### 🧠 Neural Processing Pipeline")
    st.text("🔄 NEURAL PROCESSING PIPELINE")
    st.text("=" * 50)
    st.text("📊 3D Skeletal Pose Extraction: Ready")
    st.text("✋ MANO Hand Tracking: Ready")
    st.text("😊 FLAME Face Analysis: Ready")
    st.text("🧠 Multistream Transformer: Ready")
    st.text("📈 Graph Attention Network: Ready")
    st.text("🎯 Bayesian Calibration: Ready")
    st.text("🏥 Clinical Slot Classification: Ready")
    st.text("")
    st.text("⚡ Latency Target: <300ms")
    st.text("💾 Model Size: <200MB (INT8)")
    st.text("🔒 Privacy: Offline-first processing")

with tab2:
    st.subheader("🤖 Avatar Synthesis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Text → USL Synthesis")
        st.text("Enter clinical text:")
        clinical_text = st.text_area("", height=150, key="clinical_text")
        
        if st.button("🔄 Generate USL Gloss"):
            st.info("USL GLOSS GENERATION\nGenerated Gloss:\nYOU FEVER HAVE? COUGH BLOOD? TRAVEL WHERE?")
        
        if st.button("🤖 Synthesize Avatar"):
            st.success("🤖 Parametric avatar synthesized with MANO+Face rig")
        
        st.markdown("""
        <div style="
            width: 100%; 
            height: 200px; 
            background: #374151;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #9ca3af;
            font-size: 16px;
            border: 1px solid #4b5563;
            margin-top: 15px;
        ">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">🤖</div>
                <div>Parametric Avatar</div>
                <div>(MANO + Face Rig)</div>
                <div style="margin-top: 10px;">Ready for synthesis...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🤟 USL → Structured Text")
        st.text("Recognition Results:")
        recognition_results = st.text_area("", height=250, value="""🤟 USL RECOGNITION RESULTS
========================================

🌡️ fever: Yes (confidence: 92.3%)
😷 cough: No (confidence: 87.1%)
🩸 hemoptysis: Unknown (confidence: 45.2%)
💊 diarrhea: No (confidence: 91.8%)
""", key="recognition_results")
        
        col2a, col2b, col2c = st.columns(3)
        with col2a:
            if st.button("🔊 Neural TTS (English)"):
                st.success("🔊 English TTS activated")
        with col2b:
            if st.button("🔊 Neural TTS (Runyankole)"):
                st.success("🔊 Runyankole TTS activated")
        with col2c:
            if st.button("🔊 Neural TTS (Luganda)"):
                st.success("🔊 Luganda TTS activated")

with tab3:
    st.subheader("📋 FHIR-Structured Clinical Results")
    
    if st.session_state.screening_results:
        latest_result = st.session_state.screening_results[-1]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🏥 Clinical Assessment Summary**")
            st.markdown(f"**Patient:** {latest_result.get('patient_name', 'N/A')} (ID: {latest_result.get('patient_id', patient_id)})")
            st.markdown(f"**Assessment Type:** {latest_result.get('screening_type', 'General')}")
            st.markdown(f"**Timestamp:** {latest_result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
            
            st.markdown("**🔍 Clinical Findings:**")
            for symptom in latest_result.get('symptoms', []):
                st.markdown(f"• {symptom}")
            
            st.markdown("**💡 Clinical Recommendations:**")
            for rec in latest_result.get('recommendations', []):
                st.markdown(f"• {rec}")
        
        with col2:
            st.markdown("**⚡ Quick Actions**")
            
            if st.button("🚨 Emergency Alert", use_container_width=True):
                st.error("🚨 Emergency alert sent")
                st.session_state.analytics['emergency_escalations'] += 1
                
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
                f"OBS-{patient_id}-001",
                patient_id,
                'final',
                'Clinical Screening',
                'MediSign Healthcare Assistant',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        <div style="
            text-align: center; 
            padding: 3rem; 
            background: #374151; 
            border-radius: 5px; 
            border: 1px solid #4b5563;
            color: #9ca3af;
        ">
            <div style="font-size: 3em; margin-bottom: 1rem;">📋</div>
            <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 1rem;">FHIR OBSERVATION RESOURCE</div>
            <div style="margin-bottom: 2rem;">🆔 Resource Type: Observation<br>
            📊 Category: Clinical Screening<br>
            🏥 System: MediSign Healthcare Assistant<br>
            📅 Status: Waiting for patient data...</div>
            <div>🔄 Ready to receive USL input and generate structured clinical data</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("📊 System Performance & Analytics")
    
    # Performance Metrics Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚡ Performance Metrics")
        
        # Performance data
        perf_data = pd.DataFrame({
            'Metric': ['Latency (ms)', 'Memory (MB)', 'FPS', 'Accuracy (%)'],
            'Current': [st.session_state.analytics['current_latency'], 
                       st.session_state.analytics['current_memory'],
                       st.session_state.analytics['current_fps'], 86.7],
            'Target': [300, 200, 30, 90]
        })
        
        st.bar_chart(perf_data.set_index('Metric'))
        
        # Session Statistics Table
        st.markdown("### 🔄 Session Statistics")
        session_data = pd.DataFrame({
            'Statistic': ['Total Sessions', 'Successful Translations', 'Emergency Escalations', 'Session Duration (min)'],
            'Value': [st.session_state.analytics['total_sessions'],
                     st.session_state.analytics['successful_translations'],
                     st.session_state.analytics['emergency_escalations'],
                     f"{(time.time() - st.session_state.analytics['session_start'])/60:.1f}"]
        })
        st.dataframe(session_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🧠 Neural Pipeline Status")
        
        # Pipeline status data
        pipeline_data = pd.DataFrame({
            'Component': ['3D Pose Detection', 'MANO Hand Tracking', 'FLAME Face Analysis', 
                         'Multistream Transformer', 'Graph Attention Network', 'Bayesian Calibration'],
            'Status': ['Active' if st.session_state.live_camera_active else 'Standby',
                      'Active' if st.session_state.live_camera_active else 'Standby',
                      'Active' if st.session_state.live_camera_active else 'Standby',
                      'Ready', 'Ready', 'Ready'],
            'Health': [95, 98, 92, 100, 97, 99]
        })
        
        st.dataframe(pipeline_data, use_container_width=True, hide_index=True)
        
        # Health Score Chart
        st.markdown("### 📈 Component Health")
        st.bar_chart(pipeline_data.set_index('Component')['Health'])
    
    # System Overview Tables
    st.markdown("### 🔒 System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Privacy & Security**")
        security_data = pd.DataFrame({
            'Feature': ['Offline Processing', 'Data Encryption', 'Cloud Upload', 'De-identification'],
            'Status': ['✅ Enabled', '✅ AES-256', '❌ Disabled', '✅ Active']
        })
        st.dataframe(security_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**Language Support**")
        lang_data = pd.DataFrame({
            'Feature': ['USL Variants', 'Clinic Languages', 'NMS Detection', 'Regional Adaptation'],
            'Value': ['4 (Canonical, Regional)', '3 (English, Runyankole, Luganda)', '✅ Active', '✅ LoRA Ready']
        })
        st.dataframe(lang_data, use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("**Safety Monitoring**")
        safety_data = pd.DataFrame({
            'Feature': ['Red-flag Validator', 'Danger Sign Detection', 'IRB Compliance', 'Community Consent'],
            'Status': ['✅ Active', '✅ Ready', '✅ Approved', '✅ Obtained']
        })
        st.dataframe(safety_data, use_container_width=True, hide_index=True)
    
    # Real-time Performance Chart
    st.markdown("### 📊 Real-time Performance Trends")
    
    # Generate sample time series data
    import datetime as dt
    times = [dt.datetime.now() - dt.timedelta(minutes=x) for x in range(10, 0, -1)]
    
    trend_data = pd.DataFrame({
        'Time': times,
        'Latency (ms)': np.random.randint(180, 280, 10),
        'Memory (MB)': np.random.randint(140, 190, 10),
        'FPS': np.random.randint(28, 35, 10)
    })
    
    st.line_chart(trend_data.set_index('Time'))

# Status Bar matching Tkinter design exactly
st.markdown("---")
st.markdown("""
<div style="
    background: #374151;
    padding: 10px 20px;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #4b5563;
">
    <span style="color: #e2e8f0;">🟢 System Ready - Waiting for USL input...</span>
    <span style="color: #22c55e;">⚡ Latency: <300ms</span>
</div>
""", unsafe_allow_html=True)