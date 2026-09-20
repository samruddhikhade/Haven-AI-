# ui/home.py
import datetime
import random
import streamlit as st

def get_dynamic_greeting(name: str):
    safe_name = name if name else "Mama"
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return f"Good morning, {safe_name} 🌷", "Sending you and baby a warm, gentle morning hug."
    elif 12 <= hour < 17:
        return f"Good afternoon, {safe_name} ☀️", "Hope your feet are kicked up and you're feeling cozy."
    else:
        return f"Good evening, {safe_name} 🌙", "Time to unwind, soft breaths, and quiet evening vibes."

GESTATIONAL_FRUITS = {
    (4, 8): ("First Trimester", "Raspberry 🍓"),
    (9, 13): ("First Trimester", "Sweet Plum 🍑"),
    (14, 18): ("Second Trimester", "Avocado 🥑"),
    (19, 23): ("Second Trimester", "Mango 🥭"),
    (24, 27): ("Second Trimester", "Papaya 🍈"),
    (28, 32): ("Third Trimester", "Coconut 🥥"),
    (33, 36): ("Third Trimester", "Pineapple 🍍"),
    (37, 42): ("Third Trimester", "Watermelon 🍉"),
}

def get_fruit_and_trimester(week: int):
    for (start, end), (trimester, fruit) in GESTATIONAL_FRUITS.items():
        if start <= week <= end:
            return trimester, fruit
    return "Second Trimester", "Mango 🥭"

# --- DYNAMIC MOOD RESPONSES (Random & Engaging) ---
MOOD_POOLS = {
    "Serene": [
        "Your calm heartbeat is baby's favorite melody right now. Keep floating on this peaceful cloud 🌸",
        "Breathing in pure soft peace. Baby is curled up so safe and content inside you 🌿",
        "Gentle mama energy is truly a superpower. Radiating total tranquility today ✨"
    ],
    "Energized": [
        "Look at you glowing! Baby is doing tiny little somersaults to match your sparkle ✨",
        "Unstoppable mama mode activated! Don't forget to take sweet little breathers too 💃",
        "Such happy, vibrant vibes today—peanut is definitely feeling that sunshine energy ☀️"
    ],
    "Sleepy": [
        "Pillow fortress time! Growing eyelashes and tiny fingers is serious full-time work ☁️",
        "Permission granted to cozy up, kick your feet high, and take the gentlest snooze 🥱",
        "Soft blankets, warm socks, and quiet dreams. Rest up, mama bear 🧸"
    ],
    "Hungry": [
        "Snack radar activated! Little one is gently whispering: 'Send the treats, please!' 🥑",
        "Baby's official lunch order has arrived. Time for something wholesome and delicious 🍓",
        "Tummy rumbles mean teamwork! Let's find you the coziest craving fix right away 🥨"
    ],
    "Sensitive": [
        "Sending the biggest, softest warm blanket hug. Growing a miracle is deeply emotional, and you are doing so well 🕊️",
        "It's completely okay to feel all the feelings today. You are safe, tender, and deeply cherished 💗",
        "Deep breath in, mama. You don't have to carry the whole world today—just rest your heart 🌸"
    ],
    "Grounded": [
        "Deep roots and steady love. You are providing such a stable, calm home for your baby 🌿",
        "Centered, mindful, and strong. You and little one are moving in total harmony today 🧘",
        "Such quiet elegance in your peace today. Keep trusting your body's wisdom ✨"
    ],
    "Busy": [
        "Little busy bee! Remember to pause for 30 seconds and let baby feel a calm breath 🐝",
        "Getting things done, but your comfort comes first! Sip some water and soften your shoulders 💧",
        "One step at a time, super mama. Peanut loves it when you pause for a gentle sigh 🌷"
    ],
    "Need Hug": [
        "Wrapping you in the warmest, fluffiest digital hug imaginable. You are so fiercely loved 🧸",
        "Here is an extra tight cuddle for you and peanut. Lean back and let yourself be cared for today 💗",
        "You are never alone on this journey. Take a deep, gentle breath—you're doing wonderful 🌸"
    ]
}

# --- DYNAMIC HYDRATION MILESTONE CHEERS ---
HYDRATION_CHEERS = {
    0: "Ready for your first fresh sip of the day? Baby's waiting! 💧",
    1: "First sip down! Like morning dew for your little sprout 🌱",
    2: "Two dewdrops in! Cellular refreshment feels so good 🌿",
    3: "Glug glug! Amniotic cushion staying cozy and nourished 🌊",
    4: "Halfway mark reached! You're glowing like a pearl mama 🪞",
    5: "Five cups of pure love! Energy levels thanking you right now 🌸",
    6: "Smooth sailing! Circulation and gentle vitals are loving this rhythm 🍃",
    7: "Just one more to the daily crown! You're an absolute star ⭐",
    8: "Goal accomplished! Hydration Queen status unlocked today 👑",
}

@st.dialog("🌸 Mama's Little Corner (Profile & Week)")
def edit_mama_profile():
    st.caption("Customize your personal journey details anytime.")
    curr_name = st.session_state.get("mama_name", "Mama")
    curr_age = st.session_state.get("mama_age", 28)
    curr_week = st.session_state.get("gestational_week", 24)

    new_name = st.text_input("Your Name / Nickname", value=str(curr_name))
    new_age = st.number_input("Maternal Age", min_value=16, max_value=50, value=int(curr_age))
    new_week = st.number_input("Pregnancy Week (1 - 42)", min_value=1, max_value=42, value=int(curr_week))
    
    if st.button("Save My Details 🌸", use_container_width=True):
        clean_name = str(new_name).strip() if new_name else "Mama"
        st.session_state.mama_name = clean_name if len(clean_name) > 0 else "Mama"
        st.session_state.mama_age = new_age
        st.session_state.gestational_week = new_week
        st.rerun()

def render_top_header():
    """Permanent header directly at the very top."""
    if "gestational_week" not in st.session_state:
        st.session_state.gestational_week = 24
    
    trimester, fruit_size = get_fruit_and_trimester(st.session_state.gestational_week)

    head_col1, head_col2 = st.columns([1.1, 2.0])
    with head_col1:
        st.markdown("""
        <div style="padding-top: 4px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:1.5rem;">🌿</span>
                <span class="haven-brand-title">Haven</span>
            </div>
            <span style="font-size:0.75rem; color:#9E8783; font-weight:500;">
                Your daily warm sanctuary
            </span>
        </div>
        """, unsafe_allow_html=True)

    with head_col2:
        st.markdown(f"""
        <div style="background:#FFF9F8; border:1px solid #F5E5E1; border-radius:18px; padding:10px 14px; text-align:right;">
            <div style="font-size:0.75rem; font-weight:700; color:#C86D61; text-transform:uppercase; letter-spacing:0.6px;">
                🌿 Surveillance & Sanctuary
            </div>
            <div style="font-size:0.72rem; color:#8C7571; margin-top:2px;">
                Predicting preeclampsia earlier through daily vitals & explainable ML
            </div>
            <div style="margin-top:6px; font-size:0.78rem; font-weight:600; color:#4A3B39;">
                <span style="background:#F6EBE7; padding:2px 8px; border-radius:10px; color:#9E5246;">{trimester}</span>
                <span style="margin-left:4px;">Baby is the size of a <b>{fruit_size}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_home_tab():
    if "mama_name" not in st.session_state:
        st.session_state.mama_name = "Mama"
    if "mama_age" not in st.session_state:
        st.session_state.mama_age = 28
    if "gestational_week" not in st.session_state:
        st.session_state.gestational_week = 24
    if "water_count" not in st.session_state:
        st.session_state.water_count = 4
    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = None
    if "mood_note_text" not in st.session_state:
        st.session_state.mood_note_text = None
    if "selected_craving" not in st.session_state:
        st.session_state.selected_craving = None
    if "checkin_completed" not in st.session_state:
        st.session_state.checkin_completed = False
    if "needs_gentle_review" not in st.session_state:
        st.session_state.needs_gentle_review = False

    # 1. Dynamic Greeting
    greeting_title, greeting_sub = get_dynamic_greeting(st.session_state.mama_name)
    today_date_str = datetime.date.today().strftime("%A, %d %b")

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    g_col1, g_col2 = st.columns([2.4, 1.2])
    with g_col1:
        st.markdown(f"""
        <div>
            <h2 style="margin:0; font-size:1.6rem; font-weight:700; color:#3D2B28;">
                {greeting_title}
            </h2>
            <p style="margin:2px 0 0 0; font-size:0.88rem; color:#876F6B;">
                {greeting_sub}
            </p>
        </div>
        """, unsafe_allow_html=True)
    with g_col2:
        st.markdown(f"""
        <div style="text-align:right;">
            <span style="font-size:0.74rem; color:#8C7571; font-weight:600; background:#FAF2EF; padding:4px 10px; border-radius:12px; border:1px solid #EFE2DD; display:inline-block;">
                🗓️ {today_date_str}
            </span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"⚙️ Week {st.session_state.gestational_week} • Edit", key="edit_profile_btn", use_container_width=True):
            edit_mama_profile()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # 2. Today's Haven Check Card
    st.markdown("<div class='warm-card' style='border:1px solid #F3DDD7; background:linear-gradient(135deg, #FFFFFF 0%, #FFF9F7 100%);'>", unsafe_allow_html=True)
    chk_c1, chk_c2 = st.columns([2.3, 1.2])

    with chk_c1:
        st.markdown("""
        <div style="font-size:1.15rem; font-weight:700; color:#3B2B28;">
            💗 Today’s Haven Check
        </div>
        <div style="font-size:0.85rem; color:#856E6A; margin-top:2px;">
            A gentle 60-second vitals tune-up for you and peanut.
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.checkin_completed:
            st.markdown("<div style='margin-top:8px; font-size:0.75rem; color:#B8584B; font-weight:600;'>⏳ Takes about a minute • Zero rush</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='margin-top:8px; font-size:0.75rem; color:#4B8664; font-weight:600;'>✓ All done today! You are glowing mama 🌸</div>", unsafe_allow_html=True)

    with chk_c2:
        st.markdown("<div class='primary-pill' style='margin-top:6px;'>", unsafe_allow_html=True)
        if not st.session_state.checkin_completed:
            if st.button("Start Check-in →", key="home_btn_checkin"):
                st.session_state.active_tab_redirect = "🩺 Check-in"
                st.rerun()
        else:
            if st.button("View check-in →", key="home_btn_view_checkin"):
                st.session_state.active_tab_redirect = "🩺 Check-in"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Quick Mood Check (Dynamic randomized notes)
    st.markdown("""
    <div style="font-size:0.9rem; font-weight:700; color:#3D2B28; margin: 18px 0 8px 2px;">
        How are you feeling today, mama? 💭
    </div>
    """, unsafe_allow_html=True)

    mood_row1 = [("🌸 Serene", "Serene"), ("✨ Energized", "Energized"), ("🥱 Sleepy", "Sleepy"), ("🥑 Hungry", "Hungry")]
    mood_row2 = [("☁️ Sensitive", "Sensitive"), ("🧘 Grounded", "Grounded"), ("🐝 Busy", "Busy"), ("💆 Need a hug", "Need Hug")]

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    for i, (label, val) in enumerate(mood_row1):
        with [m_col1, m_col2, m_col3, m_col4][i]:
            is_active = (st.session_state.selected_mood == val)
            label_display = f"✓ {label}" if is_active else label
            if st.button(label_display, key=f"mood_pill_{val}", use_container_width=True):
                st.session_state.selected_mood = val
                st.session_state.mood_note_text = random.choice(MOOD_POOLS[val])
                st.rerun()

    m_col5, m_col6, m_col7, m_col8 = st.columns(4)
    for i, (label, val) in enumerate(mood_row2):
        with [m_col5, m_col6, m_col7, m_col8][i]:
            is_active = (st.session_state.selected_mood == val)
            label_display = f"✓ {label}" if is_active else label
            if st.button(label_display, key=f"mood_pill_{val}", use_container_width=True):
                st.session_state.selected_mood = val
                st.session_state.mood_note_text = random.choice(MOOD_POOLS[val])
                st.rerun()

    if st.session_state.selected_mood and st.session_state.mood_note_text:
        st.markdown(f"""
        <div style="background:#FFF8F6; border:1px solid #F5E3DE; border-radius:14px; padding:11px 16px; margin-top:9px; display:flex; align-items:center; gap:10px;">
            <span style="font-size:1.2rem;">💌</span>
            <span style="font-size:0.84rem; color:#784F48; font-weight:500; font-style:italic; line-height:1.4;">
                “{st.session_state.mood_note_text}”
            </span>
        </div>
        """, unsafe_allow_html=True)

    # 4. Craving Corner Preview
    st.markdown("""
    <div class="warm-card" style="margin-top:16px; padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.95rem; font-weight:700; color:#3D2B28;">🍓 Craving Corner</span>
                <p style="font-size:0.82rem; color:#826D69; margin:2px 0 0 0;">
                    What sounds delicious today? Let’s whip up a nourishing, guilt-free craving match.
                </p>
            </div>
    """, unsafe_allow_html=True)

    cr_left, cr_right = st.columns([2.2, 1.2])
    with cr_left:
        if st.session_state.selected_craving:
            st.markdown(f"<div style='margin-top:8px; font-size:0.85rem; color:#423230;'>Today’s craving match: <b style='color:#C86D61;'>{st.session_state.selected_craving}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='margin-top:8px; font-size:0.82rem; color:#A38E8A; font-style:italic;'>No cravings locked in yet. Explore what baby is nudging you for!</div>", unsafe_allow_html=True)

    with cr_right:
        st.markdown("<div style='text-align:right; margin-top:4px;'>", unsafe_allow_html=True)
        if st.button("Explore cravings →", key="home_explore_cravings_btn"):
            st.session_state.active_tab_redirect = "🍓 Cravings"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Gentle Hydration Dewdrops with Live Cheerleader
    current_cups = st.session_state.water_count
    cheer_text = HYDRATION_CHEERS.get(current_cups, f"{current_cups} cups! Supercharged and thriving mama 💧")

    st.markdown(f"""
    <div class="warm-card" style="margin-top:16px; padding:16px 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div>
                <span style="font-size:0.9rem; font-weight:700; color:#3D2B28;">💧 Gentle Hydration Dewdrops</span>
                <span style="font-size:0.76rem; color:#8C7571; margin-left:6px;">Cellular nourishment for you and little one.</span>
            </div>
            <span style="font-size:0.84rem; font-weight:700; color:#5D8C72;">{current_cups} of 8 Cups</span>
        </div>
        <div style="font-size:0.78rem; color:#A45B50; font-weight:600; font-style:italic; margin-bottom:8px;">
            ✨ {cheer_text}
        </div>
    """, unsafe_allow_html=True)

    dewdrops_html = "".join([
        f"<span style='display:inline-block; width:18px; height:24px; border-radius:50% 50% 50% 50% / 60% 60% 40% 40%; background:{'#A8D5C2' if i < current_cups else '#EDE4E0'}; margin:0 4px; box-shadow:{'0 2px 6px rgba(168,213,194,0.4)' if i < current_cups else 'none'};'></span>"
        for i in range(8)
    ])

    hyd_col1, hyd_col2, hyd_col3 = st.columns([2.5, 1, 1])
    with hyd_col1:
        st.markdown(f"<div style='margin-top:4px; display:flex; align-items:center;'>{dewdrops_html}</div>", unsafe_allow_html=True)
    with hyd_col2:
        if st.button("💧 +1 Cup", key="dewdrop_add_btn", use_container_width=True):
            if st.session_state.water_count < 12:
                st.session_state.water_count += 1
                st.rerun()
    with hyd_col3:
        if st.button("↺ Reset", key="dewdrop_reset_btn", use_container_width=True):
            st.session_state.water_count = 0
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. Today's Little Snapshot
    st.markdown("""
    <div style="font-size:0.9rem; font-weight:700; color:#3D2B28; margin: 18px 0 10px 2px;">
        Today’s Little Snapshot 📸
    </div>
    """, unsafe_allow_html=True)

    snap1, snap2, snap3, snap4 = st.columns(4)
    with snap1:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #F2E4DF; border-radius:16px; padding:12px; text-align:center;">
            <div style="font-size:0.75rem; color:#99837F; font-weight:600;">💧 Hydration</div>
            <div style="font-size:1.15rem; font-weight:700; color:#3D2B28; margin:3px 0;">{st.session_state.water_count} / 8</div>
            <div style="font-size:0.68rem; color:#5D8C72; font-weight:600;">Dewdrops</div>
        </div>
        """, unsafe_allow_html=True)

    with snap2:
        mood_label = st.session_state.selected_mood if st.session_state.selected_mood else "Not logged"
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #F2E4DF; border-radius:16px; padding:12px; text-align:center;">
            <div style="font-size:0.75rem; color:#99837F; font-weight:600;">😊 Mood</div>
            <div style="font-size:0.85rem; font-weight:700; color:#3D2B28; margin:5px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                {mood_label}
            </div>
            <div style="font-size:0.68rem; color:#A38E8A;">Daily rhythm</div>
        </div>
        """, unsafe_allow_html=True)

    with snap3:
        chk_label = "Complete ✓" if st.session_state.checkin_completed else "Pending"
        chk_col = "#5D8C72" if st.session_state.checkin_completed else "#C86D61"
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #F2E4DF; border-radius:16px; padding:12px; text-align:center;">
            <div style="font-size:0.75rem; color:#99837F; font-weight:600;">💗 Check-in</div>
            <div style="font-size:0.95rem; font-weight:700; color:{chk_col}; margin:5px 0;">{chk_label}</div>
            <div style="font-size:0.68rem; color:#A38E8A;">Peace of mind</div>
        </div>
        """, unsafe_allow_html=True)

    with snap4:
        crav_label = st.session_state.selected_craving if st.session_state.selected_craving else "Waiting"
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #F2E4DF; border-radius:16px; padding:12px; text-align:center;">
            <div style="font-size:0.75rem; color:#99837F; font-weight:600;">🍓 Craving</div>
            <div style="font-size:0.85rem; font-weight:700; color:#3D2B28; margin:5px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                {crav_label}
            </div>
            <div style="font-size:0.68rem; color:#A38E8A;">Guilt-free bite</div>
        </div>
        """, unsafe_allow_html=True)

    # 7. Haven's Notice
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    if not st.session_state.needs_gentle_review:
        st.markdown("""
        <div style="background:#FBF8F6; border:1px solid #EFE4DF; border-radius:18px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.86rem; font-weight:700; color:#3D2B28;">✨ Haven’s Whisper</span>
                <p style="font-size:0.82rem; color:#786460; margin:3px 0 0 0;">
                    Your baseline rhythm is smooth and steady today. You and baby are in great harmony!
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Insights →", key="notice_view_insights"):
            st.session_state.active_tab_redirect = "📊 Insights"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#FFF6F4; border:1px solid #F2DCD7; border-radius:18px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.86rem; font-weight:700; color:#B8584B;">✨ Haven’s Friendly Nudge</span>
                <p style="font-size:0.82rem; color:#7A4B43; margin:3px 0 0 0;">
                    Haven noticed a tiny shift in your vitals rhythm today. Let’s take a gentle peek together!
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Review Check-in →", key="notice_review_checkin"):
            st.session_state.active_tab_redirect = "🩺 Check-in"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 8. Footprints / Recent Activity
    st.markdown("""
    <div class="warm-card" style="margin-top:16px; padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.88rem; font-weight:700; color:#3D2B28;">🌷 Little Footprints Today</span>
        </div>
    """, unsafe_allow_html=True)

    activity_log = []
    if st.session_state.checkin_completed:
        activity_log.append("✓ Logged morning vitals & checked off today's shield")
    if st.session_state.selected_mood:
        activity_log.append(f"😊 Checked in with your heart: feeling {st.session_state.selected_mood.lower()}")
    if st.session_state.selected_craving:
        activity_log.append(f"🍓 Craving radar on: {st.session_state.selected_craving}")
    activity_log.append(f"💧 Nourished baby with {st.session_state.water_count} fresh dewdrops of water")

    for act in activity_log:
        st.markdown(f"""
        <div style="font-size:0.82rem; color:#6B5652; padding:4px 0; display:flex; align-items:center; gap:8px;">
            <span style="color:#C86D61; font-size:0.6rem;">🌸</span> {act}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px; text-align:right;'>", unsafe_allow_html=True)
    if st.button("View Journey →", key="home_btn_journey"):
        st.session_state.active_tab_redirect = "📖 Journey"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)