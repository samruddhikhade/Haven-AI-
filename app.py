# app.py
import streamlit as st
from ui.styles import apply_haven_theme
from ui.home import render_home_tab, render_top_header
from ui.checkin import render_checkin_tab
from core.model import HavenModelEngine
from ui.cravings import render_cravings_tab
from ui.sanctuary import render_sanctuary_tab
from ui.journey import render_journey_tab
from ui.insights import render_insights_tab

st.set_page_config(
    page_title="Haven | Maternal Surveillance & Sanctuary",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apply_haven_theme()

# Model Engine Load (Cached so it only runs once)
@st.cache_resource
def get_engine():
    return HavenModelEngine()

engine = get_engine()

# 1. Top Header (Logo + Sanctuary Info)
render_top_header()

# 2. Navigation Bar (Tabs)
nav_tabs = ["🌷 Home", "🩺 Check-in", "🍓 Cravings", "🧘 Sanctuary", "📖 Journey", "📊 Insights"]

if "active_tab_redirect" not in st.session_state:
    st.session_state.active_tab_redirect = "🌷 Home"

selected_index = nav_tabs.index(st.session_state.active_tab_redirect) if st.session_state.active_tab_redirect in nav_tabs else 0

nav = st.radio(
    "Navigation Menu",
    nav_tabs,
    index=selected_index,
    horizontal=True,
    label_visibility="collapsed"
)

st.session_state.active_tab_redirect = nav

# 3. Tab Routing
if nav == "🌷 Home":
    render_home_tab()

elif nav == "🩺 Check-in":
    render_checkin_tab(engine)

elif nav == "🍓 Cravings":
    render_cravings_tab()

elif nav == "🧘 Sanctuary":
    render_sanctuary_tab()

elif nav == "📖 Journey":
    render_journey_tab()

elif nav == "📊 Insights":
    render_insights_tab()
