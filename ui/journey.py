# ui/journey.py
import os
import json
import uuid
import datetime
import streamlit as st
from core.storage import get_recent_checkins

JOURNEY_FILE = os.path.join("data", "my_journey.json")

# --- SIMPLE LOCAL STORAGE (NO DEPENDENCIES) ---
def _load_journey_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(JOURNEY_FILE):
        return {"notes": [], "moments": [], "milestones": []}
    try:
        with open(JOURNEY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"notes": [], "moments": [], "milestones": []}

def _save_journey_data(data):
    os.makedirs("data", exist_ok=True)
    with open(JOURNEY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def render_journey_tab():
    # Aesthetic Soft Styling
    st.markdown("""
    <style>
        .journey-header {
            background: linear-gradient(135deg, #FCF9F6 0%, #F7EFE8 100%);
            border: 1px solid #ECE1D6;
            border-radius: 20px;
            padding: 20px 24px;
            margin-bottom: 20px;
        }
        .j-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            padding: 3px 10px;
            border-radius: 12px;
            background: #EFE4DA;
            color: #7A695E;
            margin-bottom: 6px;
        }
        .stat-box {
            background: #FFFFFF;
            border: 1px solid #F0EAE3;
            border-radius: 16px;
            padding: 12px 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }
        .stat-val {
            font-size: 1.4rem;
            font-weight: 700;
            color: #4A3E3D;
        }
        .stat-sub {
            font-size: 0.75rem;
            font-weight: 600;
            color: #8C7B73;
        }
        .entry-card {
            background: #FFFFFF;
            border: 1px solid #EFE8E1;
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.015);
        }
        .tag-pill {
            background: #F8F3EE;
            border: 1px solid #EADDCF;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 0.74rem;
            font-weight: 600;
            color: #6C5B52;
        }
    </style>
    """, unsafe_allow_html=True)

    data = _load_journey_data()
    notes = data.get("notes", [])
    moments = data.get("moments", [])
    milestones = data.get("milestones", [])

    # Fetch Real Check-ins from SQLite
    history_df = get_recent_checkins(limit=30)
    checkins_list = []
    if not history_df.empty:
        checkins_list = history_df.to_dict(orient="records")

    # Combine all dates including Check-ins
    all_dates = set(
        [n["date"] for n in notes] + 
        [m["date"] for m in moments] + 
        [ms["date"] for ms in milestones] +
        [str(c.get("date", "")) for c in checkins_list if c.get("date")]
    )

    # --- 1. HEADER ---
    st.markdown("""
    <div class="journey-header">
        <span class="j-badge">🌷 MY JOURNEY</span>
        <h2 style="margin: 2px 0; font-size: 1.6rem; font-weight: 700; color: #433833;">My Journey</h2>
        <p style="margin: 0; font-size: 0.88rem; color: #7B6B62;">“A little record of the moments that make this journey yours.”</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. COMPACT STATS ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-val">🌸 {len(all_dates)}</div><div class="stat-sub">Days Logged</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-val">🩺 {len(checkins_list)}</div><div class="stat-sub">Check-ins</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-val">✨ {len(moments)}</div><div class="stat-sub">Little Moments</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-box"><div class="stat-val">🎀 {len(milestones)}</div><div class="stat-sub">Milestones</div></div>', unsafe_allow_html=True)

    st.write("")

    # --- 3. SUB NAVIGATION (EASY TABS) ---
    selected_view = st.radio(
        "Navigation",
        ["📖 Journey Timeline", "📝 Write a Note", "✨ Add a Little Moment", "🎀 Add Milestone"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # --- TAB A: WRITE A NOTE ---
    if selected_view == "📝 Write a Note":
        st.markdown("##### 📝 A little note")
        st.caption("Capture how you are feeling, thoughts, or quiet reflections today.")
        note_date = st.date_input("Date", value=datetime.date.today(), key="in_note_date")
        note_text = st.text_area("Your thoughts", placeholder="How are you feeling today? (e.g. Felt energetic today, baby was active in the afternoon...)", height=120)
        
        if st.button("Save Note to Journey 🌸", use_container_width=True):
            if note_text.strip():
                data["notes"].append({
                    "id": str(uuid.uuid4())[:8],
                    "date": note_date.strftime("%Y-%m-%d"),
                    "text": note_text.strip(),
                    "time": datetime.datetime.now().strftime("%I:%M %p")
                })
                _save_journey_data(data)
                st.success("Your note was saved to your journey. 🤍")
                st.rerun()
            else:
                st.warning("Please enter a note before saving.")

    # --- TAB B: ADD LITTLE MOMENT ---
    elif selected_view == "✨ Add a Little Moment":
        st.markdown("##### ✨ Save a Little Moment")
        st.caption("Little things matter: cravings, baby kicks, funny thoughts, or quiet walks.")
        
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            m_title = st.text_input("Moment Title", placeholder="e.g. Baby kicked during lunch, Craved cold mangoes")
        with col_m2:
            m_cat = st.selectbox("Category", ["🍼 Baby Movement", "🍓 Craving / Food", "💗 Emotional", "🌷 Personal Memory"])
            
        m_date = st.date_input("Date", value=datetime.date.today(), key="in_moment_date")
        m_note = st.text_area("Note (Optional)", placeholder="Any details you want to remember...", height=80)

        if st.button("Save Moment ✨", use_container_width=True):
            if m_title.strip():
                data["moments"].append({
                    "id": str(uuid.uuid4())[:8],
                    "date": m_date.strftime("%Y-%m-%d"),
                    "title": m_title.strip(),
                    "category": m_cat,
                    "note": m_note.strip()
                })
                _save_journey_data(data)
                st.success("Moment saved! ✨")
                st.rerun()
            else:
                st.warning("Please give your moment a title.")

    # --- TAB C: ADD MILESTONE ---
    elif selected_view == "🎀 Add Milestone":
        st.markdown("##### 🎀 Pregnancy Milestones")
        st.caption("Mark meaningful personal milestones as you progress.")
        
        col_ms1, col_ms2 = st.columns([2, 1])
        with col_ms1:
            ms_title = st.text_input("Milestone Title", placeholder="e.g. First ultrasound, Nursery set up, Baby name chosen")
        with col_ms2:
            ms_cat = st.selectbox("Type", ["🎀 Scan / Checkup", "👶 Baby Name", "🏡 Nursery", "📸 Bump Photo", "🎉 Celebration", "✨ Special"])
            
        ms_date = st.date_input("Date", value=datetime.date.today(), key="in_ms_date")
        ms_note = st.text_area("Memory Reflection", placeholder="How did this milestone feel?", height=80)

        if st.button("Save Milestone 🎀", use_container_width=True):
            if ms_title.strip():
                data["milestones"].append({
                    "id": str(uuid.uuid4())[:8],
                    "date": ms_date.strftime("%Y-%m-%d"),
                    "title": ms_title.strip(),
                    "category": ms_cat,
                    "note": ms_note.strip()
                })
                _save_journey_data(data)
                st.success("Milestone celebrated & saved! 🎀")
                st.rerun()
            else:
                st.warning("Please enter a title for this milestone.")

    # --- TAB D: TIMELINE VIEW ---
    elif selected_view == "📖 Journey Timeline":
        st.write("")
        
        # Empty State
        if not notes and not moments and not milestones and not checkins_list:
            st.markdown("""
            <div style="text-align:center; padding: 36px 18px; background: #FAF7F4; border-radius: 18px; border: 1px dashed #DFD2C7; margin-top: 10px;">
                <span style="font-size: 2.2rem;">🌷</span>
                <h3 style="color:#4A3F39; margin: 8px 0 4px 0;">Your journey starts here.</h3>
                <p style="color:#8A7B73; font-size: 0.86rem; max-width: 420px; margin: 0 auto 16px auto;">
                    Write a little note, check in your vitals, or save your first moment above to see your story unfold.
                </p>
            </div>
            """, unsafe_allow_html=True)
            return

        sorted_dates = sorted(list(all_dates), reverse=True)

        for day_str in sorted_dates:
            try:
                day_display = datetime.datetime.strptime(day_str, "%Y-%m-%d").strftime("%B %d, %Y")
            except Exception:
                day_display = day_str

            day_notes = [n for n in notes if n["date"] == day_str]
            day_moments = [m for m in moments if m["date"] == day_str]
            day_milestones = [ms for ms in milestones if ms["date"] == day_str]
            day_checkins = [c for c in checkins_list if str(c.get("date")) == day_str]

            st.markdown(f"#### 🌷 {day_display}")

            # 1. Show Check-in Card if exists for this day
            for chk in day_checkins:
                sbp = int(chk.get("systolic_bp", 120))
                dbp = int(chk.get("diastolic_bp", 80))
                hr = int(chk.get("heart_rate", 76))
                tier = chk.get("risk_tier", "Lower-Risk Pattern")
                water = chk.get("water_glasses", 5)

                st.markdown(f"""
                <div class="entry-card" style="border-left: 4px solid #C86D61; background: #FFFDFB;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="tag-pill" style="color:#C86D61; background:#FCECE8; border-color:#F5D7D0;">🩺 Haven Daily Check-in</span>
                        <span style="font-size:0.75rem; font-weight:700; color:#5D8C72;">{tier}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px; font-size:0.84rem; color:#42342E;">
                        <div>🩺 <b>BP:</b> {sbp}/{dbp} mmHg</div>
                        <div>❤️ <b>Pulse:</b> {hr} bpm</div>
                        <div>💧 <b>Water:</b> {water} Glasses</div>
                        <div>🌿 <b>Vitals Check:</b> Complete ✓</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 2. Show Milestones
            for ms in day_milestones:
                with st.container():
                    st.markdown(f"""
                    <div class="entry-card" style="border-left: 4px solid #E28E82; background: #FFFDFB;">
                        <span class="tag-pill">{ms['category']}</span>
                        <div style="font-size:1.05rem; font-weight:700; color:#42342E; margin-top:4px;">{ms['title']}</div>
                        {f'<div style="font-size:0.86rem; color:#6B5B53; margin-top:4px;">{ms["note"]}</div>' if ms.get("note") else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete Milestone", key=f"del_ms_{ms['id']}"):
                        data["milestones"] = [x for x in data["milestones"] if x["id"] != ms["id"]]
                        _save_journey_data(data)
                        st.rerun()

            # 3. Show Little Moments
            for m in day_moments:
                with st.container():
                    st.markdown(f"""
                    <div class="entry-card" style="border-left: 4px solid #DECBC3;">
                        <span class="tag-pill">{m['category']}</span>
                        <div style="font-size:0.95rem; font-weight:700; color:#3F322E; margin-top:4px;">✨ {m['title']}</div>
                        {f'<div style="font-size:0.85rem; color:#6D5D54; margin-top:4px;">{m["note"]}</div>' if m.get("note") else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete Moment", key=f"del_m_{m['id']}"):
                        data["moments"] = [x for x in data["moments"] if x["id"] != m["id"]]
                        _save_journey_data(data)
                        st.rerun()

            # 4. Show Notes
            for n in day_notes:
                with st.container():
                    st.markdown(f"""
                    <div class="entry-card" style="border-left: 4px solid #4E7B5E;">
                        <span class="tag-pill">📝 Note • {n.get('time', '')}</span>
                        <div style="font-size:0.88rem; color:#3E3530; margin-top:6px; font-style:italic;">“{n['text']}”</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete Note", key=f"del_n_{n['id']}"):
                        data["notes"] = [x for x in data["notes"] if x["id"] != n["id"]]
                        _save_journey_data(data)
                        st.rerun()

            st.write("")

    # Privacy Note
    st.markdown("""
    <div style="margin-top:28px; padding:12px 16px; background:#FAF8F6; border-radius:14px; border-left:3px solid #D6CBC4; font-size:0.75rem; color:#8C8078;">
        🌷 <b>A gentle note:</b> My Journey is your personal pregnancy diary. It documents your memories without medical or diagnostic evaluation.
    </div>
    """, unsafe_allow_html=True)