# ui/styles.py
import streamlit as st

def apply_haven_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Text elements par font apply karein, icon fonts par nahi */
    html, body, p, h1, h2, h3, h4, h5, h6, label, input, button, .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Streamlit icons ko text banne se bachayein */
    [data-testid="stIconMaterial"], 
    .material-symbols-rounded, 
    .material-icons,
    [data-testid="stExpander"] svg,
    [data-testid="stExpanderToggleIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    .stApp {
        background-color: #FDF9F7;
        color: #4A3B39;
    }

    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 740px !important;
    }

    .haven-brand-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.2rem;
        font-weight: 600;
        color: #3B2B28;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    /* Soft Pastel Navigation Pills */
    div[data-testid="stRadio"] > div {
        background: #F5EAE6 !important;
        border-radius: 9999px !important;
        padding: 5px !important;
        display: flex !important;
        justify-content: space-around !important;
        border: 1px solid #EBDAD4 !important;
        margin: 16px 0 20px 0 !important;
    }
    div[data-testid="stRadio"] label {
        border-radius: 9999px !important;
        padding: 6px 14px !important;
        color: #7D6B67 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FFFFFF !important;
        color: #C86D61 !important;
        box-shadow: 0 2px 8px rgba(200, 109, 97, 0.12) !important;
    }

    /* Soft Warm Card - No Harsh Lines */
    .warm-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #F5E7E2;
        box-shadow: 0 4px 18px rgba(74, 59, 57, 0.03);
        margin-bottom: 16px;
    }

    /* Buttons */
    .stButton > button {
        background: #FCECE8 !important;
        color: #B8584B !important;
        font-weight: 600 !important;
        border-radius: 9999px !important;
        border: 1px solid #F5D7D0 !important;
        padding: 6px 18px !important;
        font-size: 0.84rem !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background: #F7DDD6 !important;
        color: #9E4539 !important;
        border-color: #EBC3B9 !important;
        transform: translateY(-1px);
    }

    .primary-pill .stButton > button {
        background: linear-gradient(135deg, #E89588 0%, #D87B6D 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 3px 12px rgba(216, 123, 109, 0.25) !important;
    }
    .primary-pill .stButton > button:hover {
        background: linear-gradient(135deg, #DF8678 0%, #CB6B5D 100%) !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)