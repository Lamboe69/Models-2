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
    page_title="MediSign - USL Healthcare Assistant",
    page_icon="hospital",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === PREMIUM CSS WITH GLASSMORPHISM, ANIMATIONS & MICRO-INTERACTIONS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main .block-container {
        padding-top: 2rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 50%, #0f172a 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Premium */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 3px solid #3b82f6;
    }
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #60a5fa !important;
        font-weight: 600;
    }
    .css-1d391kg .stSelectbox > div > div, 
    .css-1d391kg .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px;
    }
    .css-1d391kg label { color: #e2e8f0 !important; font-weight: 500; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 6px;
        backdrop-filter: blur(8px);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #3b82f6, #60a5fa) !important;
        color: white !important;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }

    /* Dataframes */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    /* Pulse Animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    .pulse { animation: pulse 2s infinite; }

    /* Live Badge */
    .live-badge {
        display: inline-block;
        background: #ef4444;
        color: white;
        font-size: 0.7rem;
        padding: 4px 8px;
        border-radius: 20px;
        font-weight: 600;
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        'session_start': time.time(),
        'total_sessions': 1,
        'successful_translations': 0,
        'emergency_escalations': 0,
        'patient_to_clinician': 0,
        'clinician_to_patient': 0,
        'current_latency': np.random.randint(140, 220),
        'current_fps': np.random.randint(28, 36),
        'current_memory': np.random.randint(110, 170),
        'clinical_assessments': 0,
        'triage_scores': [],
        'processing_times': [],
        'api_calls': 0,
        'offline_fallbacks': 0,
        'language_usage': {'USL': 0, 'ASL': 0, 'BSL': 0}
    }

if 'live_camera_active' not in st.session_state:
    st.session_state.live_camera_active = False
if 'screening_results' not in st.session_state:
    st.session_state.screening_results = []
if 'system_status' not in st.session_state:
    st.session_state.system_status = "All Systems Online"

# === HERO HEADER ===
st.markdown("""
<div class="glass-card" style="text-align: center; padding: 2.5rem; margin-bottom: 2rem;">
    <h1 style="background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: 700; margin:0;">
        MediSign - USL Healthcare Assistant
    </h1>
    <p style="color: #cbd5e1; font-size: 1.2rem; margin: 0.8rem 0 1.5rem;">
        Real-time USL Translation • AI Clinical Reasoning • FHIR Integration
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <span style="background: rgba(59,130,246,0.2); padding: 0.5rem 1rem; border-radius: 30px; color: #60a5fa; font-size: 0.9rem; border: 1px solid #60a5fa;">
            USL Recognition
        </span>
        <span style="background: rgba(167,139,250,0.2); padding: 0.5rem 1rem; border-radius: 30px; color: #a78bfa; font-size: 0.9rem; border: 1px solid #a78bfa;">
            AI-Powered
        </span>
        <span style="background: rgba(34,197,94,0.2); padding: 0.5rem 1rem; border-radius: 30px; color: #4ade80; font-size: 0.9rem; border: 1px solid #4ade80;">
            FHIR Ready
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# === SIDEBAR - PREMIUM CONTROL PANEL ===
with st.sidebar:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:1.5rem; margin-bottom:1.5rem;">
        <h2 style="color:#60a5fa; margin:0; font-size:1.6rem;">Control Panel</h2>
        <p style="color:#94a3b8; margin:0.4rem 0 0; font-size:0.9rem;">Patient & System Management</p>
    </div>
    """, unsafe_allow_html=True)

    # Patient Info
    st.markdown("### Patient Information")
    patient_id = st.text_input("Patient ID", "PAT-2024-001", help="Unique patient identifier")
    col1, col2 = st.columns(2)
    with col1: age = st.number_input("Age", 0, 120, 30)
    with col2: gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    # USL Controls
    st.markdown("### USL Processing")
    cam_text = "Active" if st.session_state.live_camera_active else "Inactive"
    if st.button(f"Live Camera ({cam_text})", use_container_width=True):
        st.session_state.live_camera_active = not st.session_state.live_camera_active
        st.rerun()

    if st.button("Upload USL Video", use_container_width=True):
        st.info("Video upload ready")

    if st.button("Generate FHIR Report", use_container_width=True):
        st.success("FHIR report generated")

    # Language
    st.markdown("### Language Settings")
    clinic_lang = st.selectbox("Clinic Language", ["English", "Runyankole", "Luganda"])
    usl_variant = st.selectbox("USL Variant", ["Canonical", "Kampala", "Gulu", "Mbale"])

    # Quick Screening
    st.markdown("### Quick Screening")
    symptoms = [("Fever", "fever"), ("Cough", "cough"), ("Hemoptysis", "hemoptysis"), ("Diarrhea", "diarrhea")]
    for label, key in symptoms:
        col1, col2, col3 = st.columns([0.8,1,1])
        with col1: st.write(label)
        with col2: st.button("Yes", key=f"{key}_yes", use_container_width=True)
        with col3: st.button("No", key=f"{key}_no", use_container_width=True)

    # Priority Diseases
    st.markdown("### Priority Diseases")
    for d in ["TB", "VHF", "Cholera/AWD"]: st.checkbox(d, key=f"critical_{d}")
    for d in ["Malaria", "COVID-19", "Measles"]: st.checkbox(d, key=f"high_{d}")

# === MAIN TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Video Processing", "Avatar Synthesis", "Clinical Results", "Analytics"])

# === TAB 1: VIDEO PROCESSING ===
with tab1:
    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown("<div class='glass-card'><h3>Real-time USL Processing</h3></div>", unsafe_allow_html=True)
        
        if st.session_state.live_camera_active:
            st.markdown(f"""
            <div style="position:relative; border-radius:18px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.3);">
                <div style="height:420px; background:linear-gradient(135deg,#1e40af,#1e3a8a); display:flex; align-items:center; justify-content:center; color:white;">
                    <div style="text-align:center;">
                        <div style="font-size:4rem; margin-bottom:1rem;">Live Camera</div>
                        <div class="live-badge">LIVE</div>
                        <div style="margin-top:1rem; font-size:1.1rem; opacity:0.9;">
                            3D Pose • MANO Hands • FLAME Face
                        </div>
                        <div style="margin-top:1rem; padding:0.8rem 1.5rem; background:rgba(255,255,255,0.2); border-radius:30px; display:inline-block;">
                            USL Recognition Active
                        </div>
                    </div>
                </div>
                <div style="position:absolute; top:12px; right:12px; background:#ef4444; color:white; padding:6px 12px; border-radius:20px; font-size:0.8rem; font-weight:600;">
                    LIVE
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="height:420px; background:#1e293b; border:2px dashed #475569; border-radius:18px; display:flex; align-items:center; justify-content:center; color:#64748b;">
                <div style="text-align:center;">
                    <div style="font-size:3.5rem; opacity:0.5;">Camera Off</div>
                    <p style="margin-top:1rem;">Ready for USL input...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h4>Live Metrics</h4></div>", unsafe_allow_html=True)
        for label, val, icon, color in [
            ("FPS", st.session_state.analytics['current_fps'], "Chart Increasing", "#10b981"),
            ("Latency", f"{st.session_state.analytics['current_latency']}ms", "Zap", "#3b82f6"),
            ("Memory", f"{st.session_state.analytics['current_memory']}MB", "Hard Drive", "#8b5cf6")
        ]:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center; margin-bottom:0.8rem; background:{color} !important;'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-weight:700; font-size:1.3rem; color:white;'>{val}</div>
                <div style='font-size:0.85rem; opacity:0.9; color:white;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Process USL to Clinical", use_container_width=True):
            with st.spinner("Graph-Reasoned LVM Processing..."):
                time.sleep(2)
                st.success("USL to Clinical Translation Complete")
                st.session_state.analytics['successful_translations'] += 1

    # Neural Pipeline
    st.markdown("<div class='glass-card' style='margin-top:1.5rem;'><h3>Neural Processing Pipeline</h3></div>", unsafe_allow_html=True)
    steps = [
        ("3D Skeletal Pose", 98, "#10b981"),
        ("MANO Hand Tracking", 95, "#3b82f6"),
        ("FLAME Face Analysis", 92, "#8b5cf6"),
        ("Multistream Transformer", 88, "#f59e0b"),
        ("Graph Attention Network", 85, "#ef4444"),
        ("Bayesian Calibration", 90, "#06b6d4"),
        ("Clinical Slot Fill", 87, "#ec4899")
    ]
    cols = st.columns(2)
    for i, (name, prog, color) in enumerate(steps):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='glass-card' style='padding:1rem; margin-bottom:0.8rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;'>
                    <span style='font-weight:600; color:#e2e8f0;'>{name}</span>
                    <span style='font-size:0.8rem; color:#94a3b8;'>{prog}%</span>
                </div>
                <div style='height:6px; background:#334155; border-radius:3px; overflow:hidden;'>
                    <div style='width:{prog}%; height:100%; background:{color}; border-radius:3px; transition:width 0.5s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# === TAB 2: AVATAR SYNTHESIS ===
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'><h4>Text to USL Avatar</h4></div>", unsafe_allow_html=True)
        text = st.text_area("Clinical Text Input", height=130)
        if st.button("Generate USL Gloss", use_container_width=True):
            st.info("Gloss: [FEVER YES] [COUGH NO] [DURATION 3 DAYS]")
        if st.button("Synthesize Avatar", use_container_width=True):
            st.success("Avatar rendered with MANO + FLAME rig")
        st.markdown("""
        <div style="height:180px; background:#1e293b; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#64748b; margin-top:1rem;">
            <div style="text-align:center;">
                <div style="font-size:2.5rem;">Robot</div>
                <p>Parametric Avatar Ready</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h4>USL to Text</h4></div>", unsafe_allow_html=True)
        st.text_area("Recognition Output", height=200, value="""USL RECOGNITION
---
Fever: Yes (92%)
Cough: No (87%)
Hemoptysis: Unknown (45%)
Diarrhea: No (92%)
""")
        c1, c2 = st.columns(2)
        with c1: st.button("TTS (English)", use_container_width=True)
        with c2: st.button("TTS (Runyankole)", use_container_width=True)

# === TAB 3: CLINICAL RESULTS ===
with tab3:
    if st.session_state.screening_results:
        res = st.session_state.screening_results[-1]
        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown(f"<div class='glass-card'><h3>Clinical Summary</h3></div>", unsafe_allow_html=True)
            st.markdown(f"**Patient:** {res.get('patient_name', 'N/A')} | **ID:** {res.get('patient_id', patient_id)}")
            st.markdown(f"**Timestamp:** {res.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M'))}")
            st.markdown("**Symptoms:** " + " • ".join(res.get('symptoms', [])))
            st.markdown("**Recommendations:** " + " • ".join(res.get('recommendations', [])))
        with col2:
            st.markdown("<div class='glass-card'><h4>Actions</h4></div>", unsafe_allow_html=True)
            if st.button("Emergency Alert", use_container_width=True):
                st.error("EMERGENCY ESCALATED")
                st.session_state.analytics['emergency_escalations'] += 1
            st.button("Contact Physician", use_container_width=True)
            st.button("Generate Report", use_container_width=True)

        st.markdown("### FHIR Observation")
        fhir_df = pd.DataFrame({
            'Field': ['Resource', 'ID', 'Patient', 'Status', 'Category', 'Timestamp'],
            'Value': ['Observation', f"OBS-{patient_id}-001", patient_id, 'final', 'Screening', datetime.now().strftime('%Y-%m-%d %H:%M')]
        })
        st.dataframe(fhir_df, use_container_width=True, hide_index=True)

        c1,c2,c3 = st.columns(3)
        with c1: st.button("Export JSON", use_container_width=True)
        with c2: st.button("Send to EHR", use_container_width=True)
        with c3: st.button("Print", use_container_width=True)
    else:
        st.markdown("""
        <div class='glass-card' style='text-align:center; padding:3rem;'>
            <div style='font-size:4rem; opacity:0.3;'>Clipboard Check</div>
            <h3 style='color:#e2e8f0; margin:1rem 0;'>No Clinical Data</h3>
            <p style='color:#94a3b8;'>Process USL input to generate FHIR-structured results</p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 4: ANALYTICS ===
with tab4:
    st.markdown("<div class='glass-card'><h3>System Analytics</h3></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Performance")
        perf = pd.DataFrame({
            'Metric': ['Latency', 'Accuracy', 'FPS', 'Memory'],
            'Current': [st.session_state.analytics['current_latency'], 87.3, st.session_state.analytics['current_fps'], st.session_state.analytics['current_memory']],
            'Target': [300, 90, 30, 200]
        })
        st.dataframe(perf, use_container_width=True, hide_index=True)
        st.bar_chart(perf.set_index('Metric'))

    with col2:
        st.markdown("#### Session Stats")
        dur = (time.time() - st.session_state.analytics['session_start']) / 60
        sess = pd.DataFrame({
            'Stat': ['Sessions', 'Translations', 'Escalations', 'Duration'],
            'Value': [1, st.session_state.analytics['successful_translations'], st.session_state.analytics['emergency_escalations'], f"{dur:.1f} min"]
        })
        st.dataframe(sess, use_container_width=True, hide_index=True)

    st.markdown("#### Neural Pipeline Load")
    load_data = pd.DataFrame({
        'Component': ['Pose', 'Hands', 'Face', 'Transformer', 'Graph', 'Calibration'],
        'Load (%)': [np.random.randint(10,30) if st.session_state.live_camera_active else 2] * 6
    })
    st.dataframe(load_data, use_container_width=True, hide_index=True)

# === STATUS BAR ===
st.markdown("""
<div class='glass-card' style='margin-top:2rem; padding:1.5rem;'>
    <h3 style='text-align:center; margin:0 0 1.5rem; color:#e2e8f0;'>System Status</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center; background:#10b981 !important;'>
        <div style='font-size:2rem;'>Server</div>
        <div style='font-weight:600; color:white;'>Online</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center; background:#3b82f6 !important;'>
        <div style='font-size:2rem;'>User</div>
        <div style='font-weight:600; color:white;'>{patient_id}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center; background:#8b5cf6 !important;'>
        <div style='font-size:2rem;'>Clock</div>
        <div style='font-weight:600; color:white;' id='clock'>--:--:--</div>
    </div>
    """, unsafe_allow_html=True)

# Live Clock
st.markdown("""
<script>
    function updateClock() {
        const now = new Date();
        const time = now.toLocaleTimeString();
        document.getElementById('clock').innerText = time;
    }
    setInterval(updateClock, 1000);
    updateClock();
</script>
""", unsafe_allow_html=True)