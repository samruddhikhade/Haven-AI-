# ui/cravings.py
import datetime
import uuid
import streamlit as st
import pandas as pd
from zoneinfo import ZoneInfo
import datetime

def get_current_ist_time_str():
    try:
        now_ist = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
    except Exception:
        # Fallback if zoneinfo tzdata is missing
        now_ist = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    return now_ist.strftime("%Y-%m-%d • %I:%M %p")
from core.storage import (
    get_cravings_history, save_craving_entry, delete_craving_entry,
    get_saved_pantry, save_pantry
)
from core.craving_engine import (
    PANTRY_STAPLES, FLAVOR_MATRIX, get_craving_recipes, get_surprise_recipe
)

def render_cravings_tab():
    st.markdown("""
    <style>
    .craving-header {
        background: linear-gradient(135deg, #FFF7F5 0%, #FDF3F0 100%);
        border: 1px solid #F5E5E0;
        border-radius: 20px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(226, 142, 130, 0.06);
    }
    .c-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 12px;
        background: #FEECE8;
        color: #C46F63;
        margin-bottom: 6px;
    }
    .recipe-tier-card {
        background: #FFFFFF;
        border: 1px solid #F6E9E5;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .tier-tag {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        padding: 2px 8px;
        border-radius: 8px;
    }
    .tag-easy { background: #E8F5E9; color: #2E7D32; }
    .tag-time { background: #FFF3E0; color: #E65100; }
    .tag-exotic { background: #F3E5F5; color: #7B1FA2; }
    .timeline-item {
        background: #FFFFFF;
        border-left: 4px solid #E28E82;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. Header
    st.markdown("""
    <div class="craving-header">
        <span class="c-badge">🍓 HAVEN COMPANION</span>
        <h2 style="margin:2px 0; font-size:1.6rem; font-weight:700; color:#3D2B28;">Craving Corner</h2>
        <p style="margin:2px 0 0 0; font-size:0.95rem; font-weight:600; color:#856E6A;">
            “Okay mama, what are we craving today?”
        </p>
        <p style="margin:4px 0 0 0; font-size:0.82rem; color:#A8918D;">
            Sweet, salty, sour, crunchy… Haven has room for all of it. 💗
        </p>
    </div>
    """, unsafe_allow_html=True)

    # State Initializations
    if "selected_craving" not in st.session_state:
        st.session_state.selected_craving = "🍫 Sweet"
    if "selected_secondary" not in st.session_state:
        st.session_state.selected_secondary = "None"
    if "selected_vibe" not in st.session_state:
        st.session_state.selected_vibe = "🍫 “I deserve a treat.”"
    if "active_pantry" not in st.session_state:
        st.session_state.active_pantry = get_saved_pantry()
    if "cached_recipes" not in st.session_state:
        st.session_state.cached_recipes = None
    if "cached_recipe_category" not in st.session_state:
        st.session_state.cached_recipe_category = ""
    if "craving_input_box" not in st.session_state:
        st.session_state["craving_input_box"] = ""

    # 2. Hydration Bar
    current_water = st.session_state.get("water_count", 4)
    st.markdown(f"""
    <div style="background:#F2F8F9; border:1px solid #D6EBEE; border-radius:16px; padding:12px 18px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span style="font-size:0.85rem; font-weight:700; color:#2E6770;">💧 Little hydration check</span>
            <p style="margin:2px 0 0 0; font-size:0.8rem; color:#4B7E87;">
                Before you chase that craving… have you had some water recently? 💗
            </p>
        </div>
        <div style="text-align:right;">
            <span style="font-size:1.1rem; font-weight:800; color:#2E6770;">{current_water} / 8</span>
            <span style="font-size:0.75rem; color:#4B7E87;"> glasses</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    h_col1, h_col2, _ = st.columns([1, 1, 2])
    with h_col1:
        if st.button("💧 +1 Glass", key="btn_crav_plus_water_btn", use_container_width=True):
            st.session_state.water_count = current_water + 1
            st.rerun()
    with h_col2:
        if st.button("🥛 -1 Glass", key="btn_crav_minus_water_btn", use_container_width=True):
            st.session_state.water_count = max(0, current_water - 1)
            st.rerun()

    st.write("")

    # 3. Categories
    st.markdown("##### 🍓 What are you craving?")
    craving_categories = list(FLAVOR_MATRIX.keys())
    
    grid_cols = st.columns(5)
    for i, cat in enumerate(craving_categories):
        col_idx = i % 5
        with grid_cols[col_idx]:
            is_active = (st.session_state.selected_craving == cat)
            label = f"✓ {cat}" if is_active else cat
            if st.button(label, key=f"cat_pill_{i}", use_container_width=True):
                st.session_state.selected_craving = cat
                st.session_state.cached_recipes = None
                st.rerun()

    with st.expander("✨ Craving a secondary mix? (e.g. Sweet + Salty)"):
        sec_options = ["None"] + [c for c in craving_categories if c != st.session_state.selected_craving]
        st.session_state.selected_secondary = st.selectbox(
            "Add a secondary note:",
            sec_options,
            index=sec_options.index(st.session_state.selected_secondary) if st.session_state.selected_secondary in sec_options else 0
        )

    # 4. Vibe
    st.markdown("##### What's the vibe? 💭")
    vibes = [
        "🍫 “I deserve a treat.”",
        "🥺 “I need comfort.”",
        "😋 “I just WANT IT.”",
        "😴 “I'm hungry and tired.”",
        "🤷 “Random pregnancy craving.”"
    ]
    vibe_cols = st.columns(len(vibes))
    for i, v in enumerate(vibes):
        with vibe_cols[i]:
            is_vibe_active = (st.session_state.selected_vibe == v)
            short_vibe = v.split("“")[1].replace("”", "").replace(".", "")
            btn_txt = f"★ {short_vibe}" if is_vibe_active else short_vibe
            if st.button(btn_txt, key=f"vibe_pill_{i}", use_container_width=True):
                st.session_state.selected_vibe = v
                st.rerun()

    st.write("")

    # 5. Pantry
    st.markdown("<div style='background:#FFFDFD; border:1px solid #F3EAE7; border-radius:16px; padding:16px; margin-bottom:18px;'>", unsafe_allow_html=True)
    p_head1, p_head2 = st.columns([3, 1])
    with p_head1:
        st.markdown("<h5 style='margin:0; color:#3D2B28;'>🌷 What's in your pantry?</h5>", unsafe_allow_html=True)
        st.caption("Haven pairs your craving with ingredients already sitting in your kitchen.")
    with p_head2:
        surprise_clicked = st.button("✨ Surprise Me", key="btn_surprise_unique", use_container_width=True)

    safe_defaults = [x for x in st.session_state.active_pantry if x in PANTRY_STAPLES]
    selected_pantry = st.multiselect(
        "Select your available kitchen staples:",
        PANTRY_STAPLES,
        default=safe_defaults,
        placeholder="Search pantry (e.g. Banana, Makhana, Curd)..."
    )
    if selected_pantry != st.session_state.active_pantry:
        st.session_state.active_pantry = selected_pantry
        save_pantry(selected_pantry)
        st.session_state.cached_recipes = None

    st.markdown("</div>", unsafe_allow_html=True)

    if surprise_clicked:
        surprise = get_surprise_recipe(selected_pantry)
        st.session_state["craving_input_box"] = surprise['recipe']
        st.markdown(f"""
        <div style="background:#FFF9F0; border:1px dashed #E0A96D; border-radius:14px; padding:14px; margin-bottom:16px;">
            <span style="font-size:0.75rem; font-weight:700; color:#C27803;">🌷 HAVEN PICKED FOR YOU</span>
            <div style="font-size:1.05rem; font-weight:700; color:#4A382A; margin:4px 0;">{surprise['recipe']}</div>
            <p style="font-size:0.8rem; color:#786455; margin:0;">
                Category: <b>{surprise['category']}</b> • {surprise['tier_label']}<br>
                <i>“{surprise['summary']}”</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 6. Ideas
    if (st.session_state.cached_recipes is None or 
        st.session_state.cached_recipe_category != st.session_state.selected_craving):
        st.session_state.cached_recipes = get_craving_recipes(
            st.session_state.selected_craving,
            st.session_state.selected_vibe,
            selected_pantry
        )
        st.session_state.cached_recipe_category = st.session_state.selected_craving
        st.session_state["craving_input_box"] = st.session_state.cached_recipes['quick']

    recipes = st.session_state.cached_recipes

    st.markdown(f"##### ✨ Little ideas for you ({st.session_state.selected_craving})")
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        st.markdown(f"""
        <div class="recipe-tier-card">
            <span class="tier-tag tag-easy">⚡ Quick & Accessible</span>
            <p style="font-size:0.88rem; font-weight:600; color:#3D2B28; margin:8px 0 4px 0;">{recipes['quick']}</p>
            <span style="font-size:0.72rem; color:#7B8A82;">Ready in 2 mins • Desi comfort</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pick This Idea", key="btn_pick_idea_1", use_container_width=True):
            st.session_state["craving_input_box"] = recipes['quick']
            st.rerun()

    with col_t2:
        st.markdown(f"""
        <div class="recipe-tier-card">
            <span class="tier-tag tag-time">⏳ Takes a Little Love</span>
            <p style="font-size:0.88rem; font-weight:600; color:#3D2B28; margin:8px 0 4px 0;">{recipes['time']}</p>
            <span style="font-size:0.72rem; color:#9E7356;">Aromatic & warm • Desi kitchen</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pick This Idea", key="btn_pick_idea_2", use_container_width=True):
            st.session_state["craving_input_box"] = recipes['time']
            st.rerun()

    with col_t3:
        st.markdown(f"""
        <div class="recipe-tier-card">
            <span class="tier-tag tag-exotic">✨ Exotic Twist</span>
            <p style="font-size:0.88rem; font-weight:600; color:#3D2B28; margin:8px 0 4px 0;">{recipes['exotic']}</p>
            <span style="font-size:0.72rem; color:#7E5A8A;">Fun fusion • Gourmet craving</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pick This Idea", key="btn_pick_idea_3", use_container_width=True):
            st.session_state["craving_input_box"] = recipes['exotic']
            st.rerun()

    st.write("")

    # 7. Form
    st.markdown("<div style='background:#FFFFFF; border:1px solid #F5EAE6; border-radius:18px; padding:18px; box-shadow:0 2px 10px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
    st.markdown("<h5 style='margin:0; color:#3D2B28;'>🌷 Save today's craving</h5>", unsafe_allow_html=True)
    
    user_idea = st.text_input("Selected Food / Idea:", key="craving_input_box")
    user_note = st.text_input("Anything else? (Optional note)", key="craving_note_box", placeholder="Tell Haven what's on your mind…")

    if st.button("Save Craving 🍓", key="btn_final_save_craving", use_container_width=True):
        now = datetime.datetime.now()
        entry = {
            "id": str(uuid.uuid4())[:8],
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%I:%M %p"),
            "category": st.session_state.selected_craving,
            "secondary_category": st.session_state.selected_secondary,
            "vibe": st.session_state.selected_vibe,
            "idea": user_idea,
            "pantry_matched": ", ".join(recipes["matched_pantry"]) if recipes["matched_pantry"] else "None",
            "note": user_note
        }
        save_craving_entry(entry)
        st.session_state["last_saved_craving"] = entry
        st.success("Craving saved 🍓 “Got it. Haven remembers.”")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 8. Today's Card
    history_df = get_cravings_history()
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    latest_entry = None
    if st.session_state.get("last_saved_craving") is not None:
        latest_entry = st.session_state["last_saved_craving"]
    elif not history_df.empty and "date" in history_df.columns:
        today_records = history_df[history_df["date"] == today_str]
        if not today_records.empty:
            latest_entry = today_records.iloc[0].to_dict()

    if latest_entry:
        st.markdown(f"""
        <div style="background:#FFF6F4; border:1px solid #F7DBD5; border-radius:16px; padding:14px 18px; margin-top:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.75rem; font-weight:700; color:#C46F63; text-transform:uppercase;">Today's Craving Logged</span>
                <span style="font-size:0.75rem; color:#8C7571;">🕓 {latest_entry.get('time', '')}</span>
            </div>
            <div style="font-size:1.15rem; font-weight:700; color:#3D2B28; margin:4px 0;">{latest_entry.get('category', '')}</div>
            <p style="font-size:0.85rem; color:#6B534F; margin:0;">
                💭 <i>{latest_entry.get('vibe', '')}</i><br>
                ✨ <b>{latest_entry.get('idea', '')}</b>
            </p>
            {"<p style='font-size:0.78rem; color:#8C7571; margin-top:4px;'>📝 " + str(latest_entry.get('note')) + "</p>" if latest_entry.get('note') else ""}
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 9. Clean & Pretty Palate Diary
    st.markdown("##### 🌸 Your Palate & Craving Moods")
    if history_df.empty:
        st.markdown("""
        <div style="text-align:center; padding:24px; background:#FAF6F5; border-radius:18px; border:1px dashed #E8DBD7; color:#8C7571; font-size:0.85rem;">
            🍓 <b>Your craving story hasn't started yet.</b><br>
            Log a few cravings and Haven will reveal your unique pregnancy palate profile here! 💗
        </div>
        """, unsafe_allow_html=True)
    else:
        tab_diary, tab_pattern = st.tabs(["📖 Daily Log", "✨ Palate Breakdown"])
        
        with tab_diary:
            for _, row in history_df.head(6).iterrows():
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #F7ECE8; border-left:4px solid #E28E82; border-radius:14px; padding:12px 16px; margin-bottom:10px; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; font-size:0.9rem; color:#3D2B28;">{row.get('category')}</span>
                        <span style="font-size:0.75rem; color:#A38C88; background:#FBF5F4; padding:2px 8px; border-radius:10px;">{row.get('date')} • {row.get('time')}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#6B534F; margin-top:4px;">
                        💭 <i>{row.get('vibe')}</i><br>
                        ✨ <b>{row.get('idea')}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_pattern:
            clean_cats = history_df["category"].dropna().astype(str)
            if clean_cats.empty:
                st.caption("No patterns to show yet.")
            else:
                cat_counts = clean_cats.value_counts()
                top_category = str(cat_counts.index[0])
                total_logs = len(clean_cats)

                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #FFF6F3 0%, #FDF1EE 100%); border:1px solid #F5DBD4; border-radius:18px; padding:16px; margin-bottom:16px; text-align:center;">
                    <span style="font-size:0.72rem; font-weight:800; color:#C46F63; text-transform:uppercase; letter-spacing:0.8px;">Dominant Craving Vibe</span>
                    <div style="font-size:1.35rem; font-weight:800; color:#3D2B28; margin:4px 0;">{top_category} is ruling! 👑</div>
                    <div style="font-size:0.82rem; color:#856C68;">Based on your last <b>{total_logs} logged cravings</b>.</div>
                </div>
                """, unsafe_allow_html=True)

                for raw_cat_name, count in cat_counts.items():
                    cat_name = str(raw_cat_name)
                    pct = int((count / total_logs) * 100)
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #F5EAE6; border-radius:14px; padding:12px 14px; margin-bottom:10px; box-shadow:0 2px 5px rgba(0,0,0,0.02);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:0.88rem; font-weight:700; color:#3D2B28;">{cat_name}</span>
                            <span style="background:#FEECE8; color:#C46F63; font-size:0.75rem; font-weight:700; padding:2px 10px; border-radius:12px;">
                                {count} {'times' if count > 1 else 'time'} • {pct}%
                            </span>
                        </div>
                        <div style="background:#F4ECE9; height:10px; border-radius:20px; overflow:hidden;">
                            <div style="background:linear-gradient(90deg, #F8B4C0 0%, #E28E82 100%); width:{pct}%; height:100%; border-radius:20px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # 10. Footer
    st.markdown("""
    <div style="margin-top:30px; padding:12px 16px; border-top:1px dashed #E8DAD6; text-align:center;">
        <span style="font-size:0.72rem; color:#A8938F; line-height:1.4;">
            🌸 <b>Haven Companion Note:</b> Craving Corner is for personal tracking and joyful food inspiration. 
            It is completely separate from Haven's medical ML prediction models and does not diagnose nutritional deficiencies or gestational conditions.
        </span>
    </div>
    """, unsafe_allow_html=True)