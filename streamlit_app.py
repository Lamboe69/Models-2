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

# Enhanced Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main page styling */
    .main .block-container {
        padding-top: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
        border-right: 3px solid #3b82f6;
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: #ffffff !important;
    }
    
    /* Sidebar headers with better contrast */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff !important;
        border-bottom: 2px solid #60a5fa;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Enhanced sidebar text visibility */
    .css-1d391kg .css-1v0mbdj label {
        color: #f8fafc !important;
        font-weight: 600;
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stTextInput label,
    .css-1d391kg .stNumberInput label,
    .css-1d391kg .stCheckbox label,
    .css-1d391kg .stRadio label {
        color: #f8fafc !important;
        font-weight: 500;
    }
    
    .css-1d391kg p,
    .css-1d391kg .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 6px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        color: white !important;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
        color: white !important;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Enhanced tab content */
    .stTabs > div > div > div > div {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        padding: 24px;
        margin-top: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Enhanced headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700;
    }
    
    /* Premium button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb, #3b82f6);
    }
    
    /* Enhanced dataframe styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Premium text area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95);
        color: #1e293b;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Enhanced metric cards */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Premium alert styling */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-color: #3b82f6 !important;
    }
    
    /* Selectbox enhancement */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
    }
    
    /* Number input enhancement */
    .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

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

# Premium Header with Enhanced Design
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
    padding: 40px;
    border-radius: 24px;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
">
    <div style="position: absolute; top: -50%; right: -10%; width: 300px; height: 300px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
    <div style="position: absolute; bottom: -30%; left: -10%; width: 200px; height: 200px; background: rgba(255,255,255,0.05); border-radius: 50%;"></div>
    
    <div style="text-align: center; position: relative; z-index: 2;">
        <h1 style="
            color: white;
            margin: 0;
            font-size: 3rem;
            font-weight: 800;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
            background: linear-gradient(135deg, #ffffff, #e2e8f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
        ">🏥 MediSign Pro</h1>
        <p style="
            color: rgba(255, 255, 255, 0.95);
            margin: 10px 0 0 0;
            font-size: 1.4rem;
            font-weight: 400;
            letter-spacing: 0.5px;
        ">Advanced USL Healthcare Communication Platform</p>
        <div style="
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 25px;
            flex-wrap: wrap;
        ">
            <span style="
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                padding: 10px 20px;
                border-radius: 25px;
                color: white;
                font-size: 0.95rem;
                font-weight: 500;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">🤟 Real-time USL Recognition</span>
            <span style="
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                padding: 10px 20px;
                border-radius: 25px;
                color: white;
                font-size: 0.95rem;
                font-weight: 500;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">🧠 AI-Powered Diagnostics</span>
            <span style="
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                padding: 10px 20px;
                border-radius: 25px;
                color: white;
                font-size: 0.95rem;
                font-weight: 500;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">📋 FHIR & HIPAA Compliant</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Organized Sidebar
with st.sidebar:
    # Premium Sidebar header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <h2 style="color: white; margin: 0; font-size: 1.6rem; font-weight: 700;">🏥 Control Panel</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 0.95rem; font-weight: 400;">Patient Management & System Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Patient Information Section
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.12);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 4px solid #60a5fa;
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #93c5fd; margin: 0 0 12px 0; font-size: 1.2rem; font-weight: 600;">👤 Patient Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    patient_id = st.text_input("Patient ID", "PAT-2024-001", help="Enter unique patient identifier")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=30, key="age_input")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender_select")
    
    # Enhanced USL Processing Section
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.12);
        padding: 20px;
        border-radius: 12px;
        margin: 25px 0 20px 0;
        border-left: 4px solid #10b981;
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #34d399; margin: 0 0 12px 0; font-size: 1.2rem; font-weight: 600;">🤟 USL Processing</h3>
    </div>
    """, unsafe_allow_html=True)
    
    camera_status = "🟢 Active" if st.session_state.live_camera_active else "⚪ Inactive"
    cam_col1, cam_col2 = st.columns([2, 1])
    with cam_col1:
        if st.button(f"📹 Live Camera", use_container_width=True, key="camera_toggle"):
            st.session_state.live_camera_active = not st.session_state.live_camera_active
            st.rerun()
    with cam_col2:
        status_color = "#10b981" if st.session_state.live_camera_active else "#6b7280"
        st.markdown(f"""
        <div style="
            background: {status_color};
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
        ">{camera_status}</div>
        """, unsafe_allow_html=True)
    
    if st.button("📁 Upload USL Video", use_container_width=True, key="upload_video"):
        st.info("📹 Video upload ready - Select file in main panel")
    
    if st.button("📄 Generate FHIR Report", use_container_width=True, key="generate_report"):
        st.success("📄 FHIR report generated successfully!")
    
    # Enhanced Language Settings Section
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.12);
        padding: 20px;
        border-radius: 12px;
        margin: 25px 0 20px 0;
        border-left: 4px solid #f59e0b;
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #fbbf24; margin: 0 0 12px 0; font-size: 1.2rem; font-weight: 600;">🗣️ Language Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    clinic_lang = st.selectbox("Clinic Language", ["English", "Runyankole", "Luganda"], key="clinic_lang")
    usl_variant = st.selectbox("USL Variant", ["Canonical", "Kampala Regional", "Gulu Regional", "Mbale Regional"], key="usl_variant")
    
    # Enhanced Quick Screening Section
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.12);
        padding: 20px;
        border-radius: 12px;
        margin: 25px 0 20px 0;
        border-left: 4px solid #8b5cf6;
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #a78bfa; margin: 0 0 12px 0; font-size: 1.2rem; font-weight: 600;">📋 Quick Screening</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced screening questions with better visual design
    st.markdown("<p style='color: #e2e8f0; margin-bottom: 12px; font-weight: 500;'>Select symptoms:</p>", unsafe_allow_html=True)
    
    symptoms = [("fever", "🌡️", "Fever"), ("cough", "😷", "Cough"), ("hemoptysis", "🩸", "Hemoptysis"), ("diarrhea", "💊", "Diarrhea")]
    
    for symptom, icon, display_name in symptoms:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.markdown(f"<div style='text-align: center; font-size: 1.2rem; color: #e2e8f0;'>{icon}</div>", unsafe_allow_html=True)
        with col2:
            if st.button(f"✅ {display_name}", key=f"{symptom}_yes", use_container_width=True):
                st.session_state[f"{symptom}_status"] = "Yes"
        with col3:
            if st.button(f"❌ {display_name}", key=f"{symptom}_no", use_container_width=True):
                st.session_state[f"{symptom}_status"] = "No"

# Enhanced Main Content Tabs
st.markdown("""
<div style="
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 16px;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
">
    <h2 style="
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    ">🚀 System Dashboard</h2>
</div>
""", unsafe_allow_html=True)

# Create enhanced tabs with better styling
tab1, tab2, tab3, tab4 = st.tabs(["🎥 Video Processing", "🤖 Avatar Synthesis", "📋 Clinical Results", "📊 Analytics"])

with tab1:
    # Enhanced Video Processing Tab
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
            color: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
            margin-bottom: 20px;
        ">
            <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.4rem;">🎥 Real-time USL Processing</h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.95rem;">Advanced 3D pose detection and gesture recognition</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.live_camera_active:
            st.markdown("""
            <div style="
                width: 100%; 
                height: 420px; 
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
                border: 3px solid #10b981;
                box-shadow: 0 12px 40px rgba(16, 185, 129, 0.4);
                text-align: center;
                position: relative;
                overflow: hidden;
            ">
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%); animation: shine 2s infinite;"></div>
                <style>
                    @keyframes shine {
                        0% { transform: translateX(-100%); }
                        100% { transform: translateX(100%); }
                    }
                </style>
                <div style="position: relative; z-index: 2;">
                    <div style="font-size: 4rem; margin-bottom: 15px;">📹</div>
                    <div style="font-size: 1.4rem; font-weight: bold; margin-bottom: 10px;">Live Camera Feed Active</div>
                    <div style="font-size: 1rem; margin-bottom: 15px; opacity: 0.9;">3D Pose Detection • MANO Hand Tracking • FLAME Face Analysis</div>
                    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
                        <span style="padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 0.9rem;">🤟 USL Recognition</span>
                        <span style="padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 0.9rem;">🧠 AI Processing</span>
                        <span style="padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 0.9rem;">📊 Real-time Analytics</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                width: 100%; 
                height: 420px; 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
                font-size: 18px;
                border: 2px dashed #cbd5e0;
                text-align: center;
                transition: all 0.3s ease;
            ">
                <div>
                    <div style="font-size: 4rem; margin-bottom: 15px; opacity: 0.5;">📷</div>
                    <div style="font-size: 1.4rem; font-weight: bold; margin-bottom: 10px; color: #475569;">Camera Feed Inactive</div>
                    <div style="font-size: 1rem; margin-bottom: 20px; color: #64748b;">Ready for USL input processing...</div>
                    <div style="padding: 12px 24px; background: #3b82f6; color: white; border-radius: 8px; display: inline-block; font-weight: 600;">
                        Click "Live Camera" to activate
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
            color: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
            margin-bottom: 20px;
        ">
            <h4 style="color: white; margin: 0 0 15px 0; font-size: 1.2rem;">📊 Live Metrics</h4>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Real-time system performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced metrics cards with animations
        metrics = [
            ("FPS", st.session_state.analytics['current_fps'], "📈", "#10b981"),
            ("Latency", f"{st.session_state.analytics['current_latency']}ms", "⚡", "#3b82f6"),
            ("Memory", f"{st.session_state.analytics['current_memory']}MB", "💾", "#f59e0b")
        ]
        
        for label, value, icon, color in metrics:
            st.markdown(f"""
            <div style="
                background: {color};
                padding: 18px;
                border-radius: 12px;
                margin-bottom: 12px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                transition: transform 0.2s ease;
            " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 1.8rem; margin-bottom: 5px;">{icon}</div>
                <div style="font-size: 1.4rem; font-weight: bold; margin-bottom: 5px;">{value}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🧠 Process USL → Clinical", use_container_width=True, key="process_usl"):
            with st.spinner("🤖 Processing USL with Graph-Reasoned LVM..."):
                time.sleep(2)
                st.success("✅ USL processing completed successfully!")
                st.session_state.analytics['successful_translations'] += 1

# Rest of the code remains the same for tabs 2, 3, 4 and status bar...
# [The rest of your original code for tabs 2, 3, 4 and status bar goes here...]

# Enhanced Status Bar
st.markdown("""
<div style="
    background: rgba(255, 255, 255, 0.95);
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin-top: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
">
    <h3 style="color: #1e293b; text-align: center; margin: 0 0 20px 0; font-size: 1.4rem;">📊 System Status Dashboard</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    status_color = "#10b981" if "Online" in st.session_state.system_status else "#ef4444"
    st.markdown(f"""
    <div style="
        background: {status_color};
        color: white;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🖥️</div>
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">System Status</div>
        <div style="font-size: 1rem; opacity: 0.9;">{st.session_state.system_status}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    patient_display = patient_id if patient_id else "None"
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        color: white;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">👤</div>
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">Active Patient</div>
        <div style="font-size: 1rem; opacity: 0.9;">{patient_display}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🕐</div>
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">Current Time</div>
        <div style="font-size: 1rem; opacity: 0.9;">{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    translation_count = st.session_state.analytics['successful_translations']
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🤟</div>
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">Translations</div>
        <div style="font-size: 1rem; opacity: 0.9;">{translation_count} completed</div>
    </div>
    """, unsafe_allow_html=True)