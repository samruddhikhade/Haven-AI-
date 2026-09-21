# ui/styles.py
import streamlit as st

def apply_haven_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Force Light Theme Colors across Mobile & Dark Mode Devices */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #FDF9F7 !important;
        color: #3D2B28 !important;
    }

    /* Remove Default Streamlit Headers */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 680px !important;
    }

    /* Ensure All Form Labels & Number Inputs Are Visible and Readable */
    label, p, span, div {
        color: #3D2B28 !important;
    }

    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EADCD6 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"] input {
        color: #3D2B28 !important;
        -webkit-text-fill-color: #3D2B28 !important;
        font-weight: 600 !important;
    }

    /* Replace the Big Oval With Modern Individual Floating Pills */
    div[data-testid="stRadio"] > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        justify-content: center !important;
        margin: 12px 0 18px 0 !important;
        padding: 0 !important;
    }

    /* Hide ugly black radio circles */
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* Individual Abstract Floating Tabs */
    div[data-testid="stRadio"] label {
        background: #FFFFFF !important;
        border: 1px solid #F0DFD8 !important;
        border-radius: 16px !important;
        padding: 8px 14px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(74, 59, 57, 0.04) !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Active Tab Glow */
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FBECE8 !important;
        border: 1px solid #E6A89F !important;
        box-shadow: 0 4px 12px rgba(211, 109, 97, 0.18) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stRadio"] label[data-checked="true"] span {
        color: #B8584B !important;
        font-weight: 700 !important;
    }

    /* Soft General Buttons */
    .stButton > button {
        background: #FCECE8 !important;
        color: #B8584B !important;
        font-weight: 600 !important;
        border-radius: 9999px !important;
        border: 1px solid #F5D7D0 !important;
        padding: 8px 18px !important;
        font-size: 0.84rem !important;
    }
    </style>
    """, unsafe_allow_html=True)