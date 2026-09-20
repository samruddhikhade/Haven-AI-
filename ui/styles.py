# ui/styles.py
import streamlit as st

def apply_haven_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Replace the wildcard selector in ui/styles.py with target elements: */
html, body, p, span, div, h1, h2, h3, h4, h5, h6, input, label, button {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

    /* 1. Cotton Candy Animated Background (Targeting ALL root containers) */
    @keyframes cottonCandyShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(125deg, #FDECEF 0%, #EBF4FC 35%, #FFF0F5 70%, #E3EDFB 100%) !important;
        background-size: 300% 300% !important;
        animation: cottonCandyShift 14s ease infinite !important;
        background-attachment: fixed !important;
        color: #3E3032 !important;
    }

    /* Backgrounds of default wrappers transparent */
    [data-testid="stHeader"], [data-testid="stToolbar"], .main, [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }

    #MainMenu, header, footer {
        visibility: hidden !important;
        height: 0px !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 760px !important;
    }

    /* 2. Top Header Brand Typography */
    .haven-brand-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.3rem !important;
        font-weight: 600 !important;
        color: #3D292E !important;
        letter-spacing: -0.5px !important;
        line-height: 1.1 !important;
    }

    /* 3. Navigation Bar (Floating Frosted Glass) */
    div[data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 9999px !important;
        padding: 5px !important;
        display: flex !important;
        justify-content: space-around !important;
        border: 1px solid rgba(240, 214, 222, 0.8) !important;
        box-shadow: 0 4px 18px rgba(220, 175, 190, 0.18) !important;
        margin: 10px 0 18px 0 !important;
    }
    div[data-testid="stRadio"] label {
        border-radius: 9999px !important;
        padding: 6px 14px !important;
        color: #7D6368 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FFFFFF !important;
        color: #D36D81 !important;
        box-shadow: 0 2px 10px rgba(211, 109, 129, 0.2) !important;
    }

    /* 4. Soft Frosted Cards (Translucent so cotton candy shines through) */
    .warm-card {
        background: rgba(255, 255, 255, 0.78) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 22px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 8px 24px rgba(205, 180, 200, 0.12) !important;
        margin-bottom: 16px !important;
    }

    /* 5. Soft Pill Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.85) !important;
        color: #A9566A !important;
        font-weight: 600 !important;
        border-radius: 9999px !important;
        border: 1px solid #F5D3DC !important;
        padding: 6px 16px !important;
        font-size: 0.82rem !important;
        box-shadow: 0 2px 6px rgba(210, 150, 170, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #FFF5F7 !important;
        color: #8C3E52 !important;
        border-color: #EBB5C4 !important;
        transform: translateY(-1px) !important;
    }

    /* Primary Sweet CTA Button */
    .primary-pill .stButton > button {
        background: linear-gradient(135deg, #EAA1B1 0%, #C48EBF 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(205, 140, 175, 0.35) !important;
    }
    .primary-pill .stButton > button:hover {
        background: linear-gradient(135deg, #E493A5 0%, #BA81B4 100%) !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)