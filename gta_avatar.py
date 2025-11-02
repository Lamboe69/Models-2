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
            
            /* Head Styling */
            .head {{
                width: 50px;
                height: 60px;
                background: linear-gradient(145deg, #d4a574 0%, #c49660 100%);
                border-radius: 50% 50% 45% 45%;
                position: relative;
                margin: 0 auto;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
                transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .hair {{
                position: absolute;
                top: -5px;
                left: 5px;
                width: 40px;
                height: 25px;
                background: linear-gradient(145deg, #3d2914 0%, #2a1a0a 100%);
                border-radius: 50% 50% 20% 20%;
            }}
            
            .eyes {{
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 8px;
            }}
            
            .eye {{
                width: 8px;
                height: 6px;
                background: white;
                border-radius: 50%;
                position: relative;
            }}
            
            .eye::after {{
                content: '';
                position: absolute;
                top: 1px;
                left: 2px;
                width: 4px;
                height: 4px;
                background: #2c3e50;
                border-radius: 50%;
            }}
            
            .nose {{
                position: absolute;
                top: 30px;
                left: 50%;
                transform: translateX(-50%);
                width: 4px;
                height: 8px;
                background: linear-gradient(145deg, #c49660 0%, #b8855a 100%);
                border-radius: 2px;
            }}
            
            .mouth {{
                position: absolute;
                top: 42px;
                left: 50%;
                transform: translateX(-50%);
                width: 12px;
                height: 3px;
                background: #8b4513;
                border-radius: 2px;
            }}
            
            /* Body Styling */
            .neck {{
                width: 20px;
                height: 15px;
                background: linear-gradient(145deg, #d4a574 0%, #c49660 100%);
                margin: 0 auto;
                border-radius: 10px;
            }}
            
            .torso {{
                width: 60px;
                height: 80px;
                background: linear-gradient(145deg, #ffffff 0%, #f0f0f0 100%);
                margin: 5px auto;
                border-radius: 15px 15px 10px 10px;
                position: relative;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            
            .medical-coat {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(145deg, #ffffff 0%, #e8e8e8 100%);
                border-radius: 15px 15px 10px 10px;
                border: 2px solid #ddd;
            }}
            
            .coat-button {{
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                width: 4px;
                height: 4px;
                background: #666;
                border-radius: 50%;
            }}
            
            .coat-button:nth-child(1) {{ top: 15px; }}
            .coat-button:nth-child(2) {{ top: 30px; }}
            .coat-button:nth-child(3) {{ top: 45px; }}
            
            /* Arms */
            .arm {{
                position: absolute;
                top: 95px;
                transition: all 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .left-arm {{ left: -25px; }}
            .right-arm {{ right: -25px; }}
            
            .upper-arm {{
                width: 15px;
                height: 40px;
                background: linear-gradient(145deg, #d4a574 0%, #c49660 100%);
                border-radius: 8px;
                margin-bottom: 5px;
            }}
            
            .forearm {{
                width: 12px;
                height: 35px;
                background: linear-gradient(145deg, #d4a574 0%, #c49660 100%);
                border-radius: 6px;
                margin: 0 auto 5px;
            }}
            
            .hand {{
                width: 16px;
                height: 20px;
                background: linear-gradient(145deg, #d4a574 0%, #c49660 100%);
                border-radius: 8px 8px 6px 6px;
                position: relative;
                margin: 0 auto;
            }}
            
            .finger {{
                position: absolute;
                width: 2px;
                height: 6px;
                background: #c49660;
                border-radius: 1px;
                top: -3px;
            }}
            
            .finger:nth-child(2) {{ left: 3px; }}
            .finger:nth-child(3) {{ left: 6px; }}
            .finger:nth-child(4) {{ left: 9px; }}
            .finger:nth-child(5) {{ left: 12px; }}
            
            .thumb {{
                position: absolute;
                width: 2px;
                height: 5px;
                background: #c49660;
                border-radius: 1px;
                top: 2px;
                left: -2px;
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