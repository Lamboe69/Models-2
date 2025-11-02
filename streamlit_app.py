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

def create_avatar_display(pose='neutral', gesture_text='Ready'):
    """Create GTA Vice City-style realistic avatar for sign language"""
    
    html_content = f"""
    <div style="
        width: 100%; 
        height: 520px; 
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    ">
        <!-- GTA-Style Character -->
        <div class="gta-character" data-pose="{pose}">
            <!-- Character Shadow -->
            <div class="character-shadow"></div>
            
            <!-- Main Character Body -->
            <div class="character-body">
                <!-- Head -->
                <div class="head" data-pose="{pose}">
                    <div class="face">
                        <div class="hair"></div>
                        <div class="forehead"></div>
                        <div class="eyes">
                            <div class="eye left-eye"></div>
                            <div class="eye right-eye"></div>
                        </div>
                        <div class="nose"></div>
                        <div class="mouth"></div>
                    </div>
                </div>
                
                <!-- Neck -->
                <div class="neck"></div>
                
                <!-- Torso -->
                <div class="torso">
                    <div class="chest"></div>
                    <div class="medical-coat">
                        <div class="coat-button"></div>
                        <div class="coat-button"></div>
                        <div class="coat-button"></div>
                    </div>
                </div>
                
                <!-- Arms -->
                <div class="arm left-arm" data-pose="{pose}">
                    <div class="upper-arm"></div>
                    <div class="forearm"></div>
                    <div class="hand left-hand">
                        <div class="thumb"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                    </div>
                </div>
                
                <div class="arm right-arm" data-pose="{pose}">
                    <div class="upper-arm"></div>
                    <div class="forearm"></div>
                    <div class="hand right-hand">
                        <div class="thumb"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                        <div class="finger"></div>
                    </div>
                </div>
                
                <!-- Lower Body -->
                <div class="waist"></div>
                <div class="legs">
                    <div class="leg left-leg"></div>
                    <div class="leg right-leg"></div>
                </div>
                <div class="feet">
                    <div class="foot left-foot"></div>
                    <div class="foot right-foot"></div>
                </div>
            </div>
        </div>
        
        <!-- Vice City Style HUD -->
        <div class="vice-city-hud">
            <div class="hud-bar">
                <div class="status-indicator active"></div>
                <span class="gesture-text">USL: {gesture_text}</span>
            </div>
        </div>
        
        <style>
            .gta-character {{
                position: relative;
                transform: scale(1.2);
                animation: character-idle 4s ease-in-out infinite;
            }}
            
            .character-shadow {{
                position: absolute;
                bottom: -20px;
                left: 50%;
                transform: translateX(-50%);
                width: 120px;
                height: 30px;
                background: radial-gradient(ellipse, rgba(0,0,0,0.4) 0%, transparent 70%);
                border-radius: 50%;
            }}
            
            .character-body {{
                position: relative;
                width: 100px;
                height: 300px;
            }}
            
            /* Head Styling - Vice City Realistic */
            .head {{
                width: 65px;
                height: 75px;
                background: radial-gradient(ellipse at 30% 30%, #f4d1ae 0%, #e8c4a0 40%, #d4a574 100%);
                border-radius: 50% 50% 45% 45%;
                position: relative;
                margin: 0 auto;
                box-shadow: 
                    inset -8px -8px 15px rgba(0,0,0,0.15),
                    inset 8px 8px 15px rgba(255,255,255,0.3),
                    0 5px 15px rgba(0,0,0,0.2);
                transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .hair {{
                position: absolute;
                top: -8px;
                left: 3px;
                width: 59px;
                height: 35px;
                background: linear-gradient(145deg, #4a3728 0%, #3d2914 50%, #2a1a0a 100%);
                border-radius: 60% 60% 30% 30%;
                box-shadow: inset 0 3px 8px rgba(0,0,0,0.3);
            }}
            
            .hair::before {{
                content: '';
                position: absolute;
                top: 5px;
                left: 8px;
                width: 43px;
                height: 20px;
                background: linear-gradient(125deg, #5c4a3a 0%, #4a3728 100%);
                border-radius: 50% 50% 25% 25%;
                opacity: 0.6;
            }}
            
            .eyes {{
                position: absolute;
                top: 25px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 12px;
            }}
            
            .eye {{
                width: 12px;
                height: 8px;
                background: radial-gradient(circle at 30% 30%, #ffffff 0%, #f8f8f8 70%, #e0e0e0 100%);
                border-radius: 50%;
                position: relative;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
            }}
            
            .eye::after {{
                content: '';
                position: absolute;
                top: 1px;
                left: 3px;
                width: 6px;
                height: 6px;
                background: radial-gradient(circle at 30% 30%, #2c3e50 0%, #1a252f 100%);
                border-radius: 50%;
            }}
            
            .eye::before {{
                content: '';
                position: absolute;
                top: 2px;
                left: 5px;
                width: 2px;
                height: 2px;
                background: rgba(255,255,255,0.8);
                border-radius: 50%;
                z-index: 1;
            }}
            
            .nose {{
                position: absolute;
                top: 35px;
                left: 50%;
                transform: translateX(-50%);
                width: 6px;
                height: 12px;
                background: linear-gradient(145deg, #e8c4a0 0%, #d4a574 50%, #c49660 100%);
                border-radius: 3px;
                box-shadow: 
                    inset -1px -1px 2px rgba(0,0,0,0.1),
                    inset 1px 1px 2px rgba(255,255,255,0.2);
            }}
            
            .nose::after {{
                content: '';
                position: absolute;
                bottom: 2px;
                left: 1px;
                width: 2px;
                height: 1px;
                background: rgba(0,0,0,0.2);
                border-radius: 50%;
            }}
            
            .nose::before {{
                content: '';
                position: absolute;
                bottom: 2px;
                right: 1px;
                width: 2px;
                height: 1px;
                background: rgba(0,0,0,0.2);
                border-radius: 50%;
            }}
            
            .mouth {{
                position: absolute;
                top: 52px;
                left: 50%;
                transform: translateX(-50%);
                width: 16px;
                height: 4px;
                background: linear-gradient(90deg, #c67b5c 0%, #b8855a 50%, #a0522d 100%);
                border-radius: 8px;
                box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
            }}
            
            .mouth::after {{
                content: '';
                position: absolute;
                top: 1px;
                left: 2px;
                width: 12px;
                height: 1px;
                background: rgba(255,255,255,0.2);
                border-radius: 2px;
            }}
            
            /* Body Styling - Enhanced Realism */
            .neck {{
                width: 28px;
                height: 18px;
                background: radial-gradient(ellipse at 40% 30%, #f4d1ae 0%, #e8c4a0 50%, #d4a574 100%);
                margin: 0 auto;
                border-radius: 14px;
                box-shadow: 
                    inset -3px -3px 6px rgba(0,0,0,0.1),
                    inset 3px 3px 6px rgba(255,255,255,0.2);
            }}
            
            .torso {{
                width: 75px;
                height: 95px;
                background: linear-gradient(145deg, #ffffff 0%, #f8f8f8 50%, #f0f0f0 100%);
                margin: 8px auto;
                border-radius: 20px 20px 12px 12px;
                position: relative;
                box-shadow: 
                    0 8px 20px rgba(0,0,0,0.15),
                    inset 0 2px 4px rgba(255,255,255,0.3);
            }}
            
            .medical-coat {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(145deg, #ffffff 0%, #f8f8f8 30%, #f0f0f0 70%, #e8e8e8 100%);
                border-radius: 20px 20px 12px 12px;
                border: 2px solid #e0e0e0;
                box-shadow: 
                    inset 0 3px 8px rgba(255,255,255,0.4),
                    inset 0 -2px 4px rgba(0,0,0,0.05);
            }}
            
            .coat-button {{
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                width: 6px;
                height: 6px;
                background: radial-gradient(circle at 30% 30%, #888 0%, #666 50%, #444 100%);
                border-radius: 50%;
                box-shadow: 
                    0 2px 4px rgba(0,0,0,0.2),
                    inset 0 1px 2px rgba(255,255,255,0.3);
            }}
            
            .coat-button:nth-child(1) {{ top: 18px; }}
            .coat-button:nth-child(2) {{ top: 35px; }}
            .coat-button:nth-child(3) {{ top: 52px; }}
            
            /* Arms - Realistic Proportions */
            .arm {{
                position: absolute;
                top: 110px;
                transition: all 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .left-arm {{ left: -30px; }}
            .right-arm {{ right: -30px; }}
            
            .upper-arm {{
                width: 20px;
                height: 48px;
                background: radial-gradient(ellipse at 30% 30%, #f4d1ae 0%, #e8c4a0 40%, #d4a574 100%);
                border-radius: 10px;
                margin-bottom: 6px;
                position: relative;
                box-shadow: 
                    inset -3px -3px 8px rgba(0,0,0,0.1),
                    inset 3px 3px 8px rgba(255,255,255,0.2);
            }}
            
            .upper-arm::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 25px;
                background: linear-gradient(145deg, #ffffff 0%, #f0f0f0 100%);
                border-radius: 10px 10px 5px 5px;
                border: 1px solid #e0e0e0;
            }}
            
            .forearm {{
                width: 16px;
                height: 42px;
                background: radial-gradient(ellipse at 30% 30%, #f4d1ae 0%, #e8c4a0 40%, #d4a574 100%);
                border-radius: 8px;
                margin: 0 auto 6px;
                box-shadow: 
                    inset -2px -2px 6px rgba(0,0,0,0.1),
                    inset 2px 2px 6px rgba(255,255,255,0.2);
            }}
            
            .hand {{
                width: 20px;
                height: 24px;
                background: radial-gradient(ellipse at 30% 30%, #f4d1ae 0%, #e8c4a0 40%, #d4a574 100%);
                border-radius: 10px 10px 8px 8px;
                position: relative;
                margin: 0 auto;
                box-shadow: 
                    inset -2px -2px 6px rgba(0,0,0,0.1),
                    inset 2px 2px 6px rgba(255,255,255,0.2);
            }}
            
            .finger {{
                position: absolute;
                width: 3px;
                height: 8px;
                background: linear-gradient(180deg, #e8c4a0 0%, #d4a574 100%);
                border-radius: 2px;
                top: -4px;
                box-shadow: inset 0 1px 2px rgba(255,255,255,0.2);
            }}
            
            .finger:nth-child(2) {{ left: 3px; height: 9px; }}
            .finger:nth-child(3) {{ left: 7px; height: 10px; }}
            .finger:nth-child(4) {{ left: 11px; height: 9px; }}
            .finger:nth-child(5) {{ left: 15px; height: 7px; }}
            
            .thumb {{
                position: absolute;
                width: 3px;
                height: 6px;
                background: linear-gradient(180deg, #e8c4a0 0%, #d4a574 100%);
                border-radius: 2px;
                top: 3px;
                left: -2px;
                box-shadow: inset 0 1px 2px rgba(255,255,255,0.2);
            }}
            
            /* Legs */
            .waist {{
                width: 50px;
                height: 20px;
                background: linear-gradient(145deg, #2c3e50 0%, #1a252f 100%);
                margin: 0 auto;
                border-radius: 10px;
            }}
            
            .legs {{
                display: flex;
                justify-content: center;
                gap: 5px;
                margin-top: 5px;
            }}
            
            .leg {{
                width: 18px;
                height: 60px;
                background: linear-gradient(145deg, #2c3e50 0%, #1a252f 100%);
                border-radius: 9px;
            }}
            
            .feet {{
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-top: 5px;
            }}
            
            .foot {{
                width: 20px;
                height: 8px;
                background: linear-gradient(145deg, #1a1a1a 0%, #000 100%);
                border-radius: 10px 4px 4px 10px;
            }}
            
            /* Pose Animations */
            .left-arm[data-pose="fever"] {{
                transform: rotate(-45deg) translateY(-15px);
                transform-origin: top center;
            }}
            
            .head[data-pose="fever"] {{
                transform: rotate(3deg);
            }}
            
            .left-arm[data-pose="cough"] {{
                transform: rotate(-25deg) translateX(10px) translateY(-5px);
                transform-origin: top center;
            }}
            
            .left-arm[data-pose="question"], .right-arm[data-pose="question"] {{
                transform: rotate(-75deg) translateY(-25px);
                transform-origin: top center;
            }}
            
            .right-arm[data-pose="question"] {{
                transform: rotate(75deg) translateY(-25px);
            }}
            
            /* Vice City HUD */
            .vice-city-hud {{
                position: absolute;
                bottom: 25px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
                padding: 12px 25px;
                border-radius: 25px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                color: white;
                box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
                border: 2px solid rgba(255,255,255,0.3);
            }}
            
            .hud-bar {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            
            .status-indicator {{
                width: 12px;
                height: 12px;
                background: #00ff00;
                border-radius: 50%;
                animation: vice-city-blink 1.5s ease-in-out infinite;
                box-shadow: 0 0 10px #00ff00;
            }}
            
            .gesture-text {{
                font-size: 14px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
            
            /* Animations */
            @keyframes character-idle {{
                0%, 100% {{ transform: scale(1.2) translateY(0px); }}
                50% {{ transform: scale(1.2) translateY(-3px); }}
            }}
            
            @keyframes vice-city-blink {{
                0%, 100% {{ opacity: 1; box-shadow: 0 0 10px #00ff00; }}
                50% {{ opacity: 0.3; box-shadow: 0 0 5px #00ff00; }}
            }}
        </style>
    </div>
    """
    
    return html_content

# Main App
st.title("🏥 MediSign - USL Healthcare Assistant")
st.markdown("### Vice City Style Medical Avatar")

# Display the avatar
avatar_html = create_avatar_display(pose='neutral', gesture_text='Ready for USL')
html(avatar_html, height=550)

# Add some controls
col1, col2 = st.columns(2)

with col1:
    pose = st.selectbox("Select Pose:", ['neutral', 'fever', 'cough', 'question'])
    
with col2:
    gesture_text = st.text_input("Gesture Text:", "Ready for USL")

if st.button("Update Avatar"):
    avatar_html = create_avatar_display(pose=pose, gesture_text=gesture_text)
    html(avatar_html, height=550)