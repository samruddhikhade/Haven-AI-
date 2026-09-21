# ui/journey.py
import os
import json
import uuid
import datetime
import streamlit as st
from core.storage import get_recent_checkins

JOURNEY_FILE = os.path.join("data", "my_journey.json")

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
    # --- MINIMALIST COMPACT STYLING ---
    st.markdown("""
    <style>
        .journey-header-mini {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 2px 14px 2px;
        }
        .filter-chip {
            background: #FFFFFF;
            border: 1px solid #ECE1DA;
            border-radius: 999px;
            padding: 4px 14px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #6E5A54;
            display: inline-block;
        }
        .mini-card {
            background: #FFFFFF;
            border: 1px solid #F1E5E0;
            border-radius: 14px;
            padding: 10px 14px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.15s ease;
        }
        .mini-card:hover {
            border-color: #E6D0C7;
        }
        .badge-soft {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    data = _load_journey_data()
    notes = data.get("notes", [])
    moments = data.get("moments", [])
    milestones = data.get("milestones", [])

    history_df = get_recent_checkins(limit=30)
    checkins_list = history_df.to_dict(orient="records") if not history_df.empty else []

    all_dates = set(
        [n["date"] for n in notes] + 
        [m["date"] for m in moments] + 
        [ms["date"] for ms in milestones] +
        [str(c.get("date", "")) for c in checkins_list if c.get("date")]
    )

    # 1. MINIMAL HEADER WITH SUMMARY BAR
    st.markdown("""
    <div class="journey-header-mini">
        <div>
            <h3 style="margin:0; font-size:1.45rem; font-weight:700; color:#3D2B28;">🌸 My Journey</h3>
            <p style="margin:2px 0 0 0; font-size:0.82rem; color:#8C7571;">Your personal moments, milestones & health logs.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Minimal inline stats
    st.markdown(f"""
    <div style="display:flex; gap:8px; margin-bottom:14px; overflow-x:auto;">
        <span class="filter-chip">📅 <b>{len(all_dates)}</b> Days Logged</span>
        <span class="filter-chip">🩺 <b>{len(checkins_list)}</b> Vitals</span>
        <span class="filter-chip">🎀 <b>{len(milestones)}</b> Milestones</span>
        <span class="filter-chip">✨ <b>{len(moments) + len(notes)}</b> Memories</span>
    </div>
    """, unsafe_allow_html=True)

    # 2. QUICK ADD & TIMELINE SWITCHER (Segmented control)
    tab_view = st.radio(
        "Journey Nav",
        ["📖 Timeline", "➕ Quick Add Memory", "🎀 Add Milestone"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # --- TAB: QUICK ADD MEMORY (Note or Moment) ---
    if tab_view == "➕ Quick Add Memory":
        st.markdown("<div class='warm-card' style='margin-top:10px;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#3D2B28;'>✨ Capture a Note or Moment</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            entry_type = st.radio("Type", ["📝 Quiet Note", "✨ Little Moment (Kick, Craving)"], horizontal=True)
        with c2:
            entry_date = st.date_input("Date", value=datetime.date.today(), key="q_date")

        if "Note" in entry_type:
            note_txt = st.text_area("What's on your mind?", placeholder="Soft thoughts, feelings, or how baby moved today...", height=90)
            if st.button("Save Note 🌸", use_container_width=True):
                if note_txt.strip():
                    data["notes"].append({
                        "id": str(uuid.uuid4())[:8],
                        "date": entry_date.strftime("%Y-%m-%d"),
                        "text": note_txt.strip(),
                        "time": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    _save_journey_data(data)
                    st.success("Note saved beautifully!")
                    st.rerun()
        else:
            m_title = st.text_input("Title", placeholder="e.g. Felt baby hiccups, First flutter")
            m_cat = st.selectbox("Category", ["🍼 Baby Movement", "🍓 Craving", "💗 Emotional Moment", "🌷 Daily Memory"])
            m_note = st.text_input("Short note (optional)")
            if st.button("Save Moment ✨", use_container_width=True):
                if m_title.strip():
                    data["moments"].append({
                        "id": str(uuid.uuid4())[:8],
                        "date": entry_date.strftime("%Y-%m-%d"),
                        "title": m_title.strip(),
                        "category": m_cat,
                        "note": m_note.strip()
                    })
                    _save_journey_data(data)
                    st.success("Moment pinned to your journey!")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB: ADD MILESTONE ---
    elif tab_view == "🎀 Add Milestone":
        st.markdown("<div class='warm-card' style='margin-top:10px;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#3D2B28;'>🎀 Celebrate a Milestone</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            ms_title = st.text_input("Milestone Name", placeholder="e.g. 20-Week Scan, First Kick Heard by Dad")
        with c2:
            ms_cat = st.selectbox("Category", ["🎀 Scan / Vitals", "👶 Baby Movement", "📸 Bump Photo", "🎉 Celebration"])
            
        ms_date = st.date_input("Date", value=datetime.date.today(), key="ms_q_date")
        ms_note = st.text_area("Memory Reflection", placeholder="How did this milestone feel?", height=75)

        if st.button("Pin Milestone 🎀", use_container_width=True):
            if ms_title.strip():
                data["milestones"].append({
                    "id": str(uuid.uuid4())[:8],
                    "date": ms_date.strftime("%Y-%m-%d"),
                    "title": ms_title.strip(),
                    "category": ms_cat,
                    "note": ms_note.strip()
                })
                _save_journey_data(data)
                st.success("Milestone celebrated & saved!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB: MINIMALIST TIMELINE ---
    elif tab_view == "📖 Timeline":
        # 3. INTERACTIVE CATEGORY FILTER (Scroll kam karne ke liye)
        filter_col, search_col = st.columns([2.2, 1.2])
        with filter_col:
            category_filter = st.selectbox(
                "Filter View",
                ["🌸 All Entries", "🎀 Milestones Only", "🩺 Health Check-ins", "✨ Notes & Moments"],
                label_visibility="collapsed"
            )

        if not all_dates:
            st.markdown("""
            <div style="text-align:center; padding: 28px 14px; background: #FAF7F4; border-radius: 16px; border: 1px dashed #DFD2C7; margin-top: 10px;">
                <span style="font-size: 1.8rem;">🌷</span>
                <div style="color:#4A3F39; font-weight:600; font-size:0.95rem; margin-top:4px;">No memory entries yet</div>
                <p style="color:#8A7B73; font-size:0.8rem; margin:2px 0 0 0;">Use Quick Add above or log a Check-in to build your scrapbook.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        sorted_dates = sorted(list(all_dates), reverse=True)

        # Date loop - Accordion / Compact list representation
        for idx, day_str in enumerate(sorted_dates):
            try:
                date_obj = datetime.datetime.strptime(day_str, "%Y-%m-%d")
                day_display = date_obj.strftime("%d %b %Y (%A)")
                is_today = (date_obj.date() == datetime.date.today())
            except Exception:
                day_display = day_str
                is_today = False

            day_notes = [n for n in notes if n["date"] == day_str]
            day_moments = [m for m in moments if m["date"] == day_str]
            day_milestones = [ms for ms in milestones if ms["date"] == day_str]
            day_checkins = [c for c in checkins_list if str(c.get("date")) == day_str]

            # Apply Filter
            if category_filter == "🎀 Milestones Only":
                day_notes, day_moments, day_checkins = [], [], []
            elif category_filter == "🩺 Health Check-ins":
                day_notes, day_moments, day_milestones = [], [], []
            elif category_filter == "✨ Notes & Moments":
                day_milestones, day_checkins = [], []

            total_items = len(day_notes) + len(day_moments) + len(day_milestones) + len(day_checkins)
            if total_items == 0:
                continue

            # Pehla din (ya today) by default open rahega, baaki dates collapsed rahengi
            expander_title = f"{'⭐ Today • ' if is_today else ''}{day_display} ({total_items} items)"
            with st.expander(expander_title, expanded=(idx == 0)):
                
                # A. Check-in item (Compact badge design)
                for chk in day_checkins:
                    sbp = int(chk.get("systolic_bp", 120))
                    dbp = int(chk.get("diastolic_bp", 80))
                    hr = int(chk.get("heart_rate", 76))
                    tier = chk.get("risk_tier", "Lower-Risk")
                    badge_bg = "#EBF5EE" if "Lower" in tier else "#FDEEEB"
                    badge_color = "#3B7A57" if "Lower" in tier else "#B8584B"

                    st.markdown(f"""
                    <div class="mini-card">
                        <div>
                            <span style="font-weight:700; font-size:0.86rem; color:#3D2B28;">🩺 Daily Vitals</span>
                            <span style="font-size:0.8rem; color:#786460; margin-left:8px;">BP: <b>{sbp}/{dbp}</b> • Pulse: <b>{hr}</b> bpm</span>
                        </div>
                        <span class="badge-soft" style="background:{badge_bg}; color:{badge_color};">{tier}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # B. Milestones item
                for ms in day_milestones:
                    st.markdown(f"""
                    <div class="mini-card" style="border-left: 3px solid #E28E82;">
                        <div>
                            <span style="font-weight:700; font-size:0.86rem; color:#3D2B28;">🎀 {ms['title']}</span>
                            <div style="font-size:0.78rem; color:#8C7571; margin-top:2px;">{ms.get('note', '')}</div>
                        </div>
                        <span class="badge-soft" style="background:#FFF0EC; color:#B35547;">{ms.get('category', 'Milestone')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_ms_{ms['id']}"):
                        data["milestones"] = [x for x in data["milestones"] if x["id"] != ms["id"]]
                        _save_journey_data(data)
                        st.rerun()

                # C. Moments item
                for m in day_moments:
                    st.markdown(f"""
                    <div class="mini-card" style="border-left: 3px solid #DECBC3;">
                        <div>
                            <span style="font-weight:600; font-size:0.84rem; color:#42322E;">✨ {m['title']}</span>
                            {f'<div style="font-size:0.78rem; color:#8C7571; margin-top:2px;">{m.get("note")}</div>' if m.get("note") else ''}
                        </div>
                        <span class="badge-soft" style="background:#F7F1EE; color:#7A6963;">{m.get('category', 'Moment')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_m_{m['id']}"):
                        data["moments"] = [x for x in data["moments"] if x["id"] != m["id"]]
                        _save_journey_data(data)
                        st.rerun()

                # D. Notes item
                for n in day_notes:
                    st.markdown(f"""
                    <div class="mini-card" style="border-left: 3px solid #A8C9B9;">
                        <div>
                            <span style="font-weight:600; font-size:0.82rem; color:#3D2B28; font-style:italic;">“{n['text']}”</span>
                            <div style="font-size:0.72rem; color:#9E8783; margin-top:2px;">Logged at {n.get('time', '')}</div>
                        </div>
                        <span class="badge-soft" style="background:#EEF5F1; color:#4E7B5E;">Note</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_n_{n['id']}"):
                        data["notes"] = [x for x in data["notes"] if x["id"] != n["id"]]
                        _save_journey_data(data)
                        st.rerun()

    # Minimal Privacy Footer
    st.markdown("""
    <div style="margin-top:20px; text-align:center; font-size:0.73rem; color:#A89890;">
        🌸 Haven Journey • Your memories are stored locally and privately.
    </div>
    """, unsafe_allow_html=True)