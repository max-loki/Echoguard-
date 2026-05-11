import streamlit as st
import librosa
import io
import time
from Project import load_model, improved_detection_logic

# Page Config
st.set_page_config(page_title="EchoGuard Forensics", layout="wide", page_icon="🛡️")

# Full Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #050a0e;
    color: #c8d8e0;
}
.stApp {
    background: #050a0e;
}
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,255,200,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,200,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    position: relative;
    z-index: 1;
}
h1 {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 2.8rem !important;
    color: #00ffcc !important;
    text-shadow: 0 0 20px rgba(0,255,200,0.5), 0 0 40px rgba(0,255,200,0.2);
    letter-spacing: 4px !important;
    margin-bottom: 0 !important;
    animation: flicker 8s infinite;
}
h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    color: #00ffcc !important;
    letter-spacing: 2px !important;
    font-weight: 600 !important;
}
.subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: #4a7a8a;
    font-size: 0.85rem;
    letter-spacing: 3px;
    margin-top: -5px;
    margin-bottom: 2rem;
}
[data-testid="stFileUploader"] {
    background: rgba(0,255,200,0.02) !important;
    border: 1px solid rgba(0,255,200,0.2) !important;
    border-radius: 4px !important;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,255,200,0.5) !important;
    background: rgba(0,255,200,0.05) !important;
    box-shadow: 0 0 20px rgba(0,255,200,0.1);
}
.stButton > button {
    background: transparent !important;
    border: 1px solid #00ffcc !important;
    color: #00ffcc !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 3px !important;
    padding: 0.7rem 2rem !important;
    border-radius: 2px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: rgba(0,255,200,0.1) !important;
    box-shadow: 0 0 25px rgba(0,255,200,0.3) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stMetric"] {
    background: rgba(0,10,15,0.8) !important;
    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 4px !important;
    padding: 1.5rem !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(to bottom, #00ffcc, transparent);
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #4a7a8a !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #00ffcc !important;
    font-size: 2.5rem !important;
    text-shadow: 0 0 15px rgba(0,255,200,0.4);
}
.stAlert {
    border-radius: 4px !important;
    border: none !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px !important;
    font-size: 0.85rem !important;
}
hr {
    border-color: rgba(0,255,200,0.1) !important;
    margin: 1.5rem 0 !important;
}
audio {
    width: 100%;
    filter: invert(1) hue-rotate(150deg);
    opacity: 0.8;
}
[data-testid="stSidebar"] {
    background: rgba(0,5,10,0.95) !important;
    border-right: 1px solid rgba(0,255,200,0.1) !important;
}
[data-testid="stSidebar"] * {
    color: #c8d8e0 !important;
}
.status-badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 2px;
    margin-bottom: 1rem;
}
.status-online {
    background: rgba(0,255,100,0.1);
    border: 1px solid rgba(0,255,100,0.3);
    color: #00ff88;
}
.status-offline {
    background: rgba(255,50,50,0.1);
    border: 1px solid rgba(255,50,50,0.3);
    color: #ff4444;
}
@keyframes flicker {
    0%, 95%, 100% { opacity: 1; }
    96% { opacity: 0.8; }
    97% { opacity: 1; }
    98% { opacity: 0.6; }
    99% { opacity: 1; }
}
@keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}
.scanline {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(to right, transparent, rgba(0,255,200,0.1), transparent);
    animation: scanline 6s linear infinite;
    pointer-events: none;
    z-index: 999;
}
</style>
<div class="scanline"></div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛡️ ECHOGUARD")
    st.markdown('<p style="font-family: Share Tech Mono; font-size:0.7rem; color:#4a7a8a; letter-spacing:2px;">NEURAL FORENSIC SUITE v2.0</p>', unsafe_allow_html=True)
    st.markdown("---")

    model = load_model()
    if model:
        st.markdown('<span class="status-badge status-online">● MODEL ONLINE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-offline">● MODEL OFFLINE</span>', unsafe_allow_html=True)
        st.warning("Run train.py to generate model")

    st.markdown("---")
    st.markdown("**SYSTEM INFO**")
    st.markdown('<p style="font-family: Share Tech Mono; font-size:0.75rem; color:#4a7a8a;">Classifier: Random Forest<br>Features: MFCC · Flatness · Centroid<br>Training Set: 1200 samples<br>Classes: REAL / SYNTHETIC</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="font-family: Share Tech Mono; font-size:0.65rem; color:#2a4a5a;">ECHOGUARD FORENSICS<br>DEEPFAKE AUDIO DETECTION</p>', unsafe_allow_html=True)

# Header
st.markdown("# ECHOGUARD")
st.markdown('<p class="subtitle">// DEEPFAKE AUDIO FORENSICS SYSTEM //</p>', unsafe_allow_html=True)
st.markdown("---")

# Upload
st.markdown("### 📡 AUDIO INPUT")
uploaded_file = st.file_uploader("Drop a WAV or MP3 file for forensic analysis", type=['wav', 'mp3'])

if uploaded_file is not None:
    st.markdown("---")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📁 SOURCE FILE")
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/wav')
        st.markdown(f'<p style="font-family: Share Tech Mono; font-size:0.75rem; color:#4a7a8a;">FILE: {uploaded_file.name}<br>SIZE: {len(audio_bytes)/1024:.1f} KB</p>', unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚙️ ANALYSIS CONTROLS")
        st.markdown('<p style="font-family: Share Tech Mono; font-size:0.75rem; color:#4a7a8a; margin-bottom:1rem;">READY TO SCAN — CLICK TO INITIATE FORENSIC PROTOCOL</p>', unsafe_allow_html=True)

        if st.button("🚀 INITIATE FORENSIC SCAN", use_container_width=True):
            with st.spinner("Analyzing spectral artifacts..."):
                time.sleep(1)
                y, sr = librosa.load(io.BytesIO(audio_bytes), duration=5)
                is_fake, confidence = improved_detection_logic(y, sr)

            st.markdown("---")
            st.markdown("### 📊 SCAN RESULTS")

            m1, m2 = st.columns(2)
            auth_score = f"{100 - confidence}%" if is_fake else f"{confidence}%"
            ai_prob = f"{confidence}%" if is_fake else f"{100 - confidence}%"

            m1.metric("AUTHENTICITY SCORE", auth_score)
            m2.metric("AI PROBABILITY", ai_prob)

            st.markdown("<br>", unsafe_allow_html=True)

            if is_fake:
                st.error("🚨  THREAT DETECTED — HIGH PROBABILITY OF SYNTHETIC VOICE CLONING")
                st.markdown(f'<p style="font-family: Share Tech Mono; font-size:0.75rem; color:#ff4444;">VERDICT: SYNTHETIC &nbsp;|&nbsp; CONFIDENCE: {confidence}% &nbsp;|&nbsp; STATUS: FLAGGED</p>', unsafe_allow_html=True)
            else:
                st.success("✅  VERIFIED — VOICE PATTERNS MATCH HUMAN BIOLOGICAL MARKERS")
                st.markdown(f'<p style="font-family: Share Tech Mono; font-size:0.75rem; color:#00ff88;">VERDICT: AUTHENTIC &nbsp;|&nbsp; CONFIDENCE: {confidence}% &nbsp;|&nbsp; STATUS: CLEARED</p>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="font-family: Share Tech Mono; font-size:0.65rem; color:#2a4a5a; text-align:center;">ECHOGUARD FORENSICS · NEURAL DEEPFAKE DETECTION · ALL RIGHTS RESERVED</p>', unsafe_allow_html=True)
