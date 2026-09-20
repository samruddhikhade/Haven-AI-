# ui/sanctuary.py
import datetime
import uuid
import random
import time
import streamlit as st
import pandas as pd
from core.storage import get_sanctuary_history, save_sanctuary_session

# --- GENTLE PRENATAL EXERCISE DECKS ---
EXERCISE_DECKS = [
    {
        "title": "🌸 Gentle Cat-Cow Spine Relief",
        "focus": "Lower back decompression & pelvic circulation",
        "steps": [
            ("Position", "Come onto hands and knees with knees hip-width apart and wrists under shoulders."),
            ("Inhale (Cow)", "Gently drop the belly down, draw shoulders back, and gaze softly forward without straining."),
            ("Exhale (Cat)", "Tuck chin slightly, round your spine up toward the ceiling, and relax your neck completely."),
            ("Repetitions", "Flow gently between both postures for 6 to 8 smooth breaths at your own pace.")
        ],
        "tip": "Avoid over-extending your back; keep the movements small, fluid, and comfortable."
    },
    {
        "title": "🕊️ Seated Pelvic Tilts & Side Stretch",
        "focus": "Easing hip tightness & expanding ribcage room",
        "steps": [
            ("Position", "Sit comfortably on a yoga block, chair, or cross-legged with an upright, soft spine."),
            ("Side Arc", "Place right palm beside you, sweep left arm gently overhead, breathing into the left side ribs."),
            ("Switch", "Lower left arm down and gently sweep right arm overhead. Repeat twice on each side."),
            ("Pelvic Rolls", "Place hands on knees and make small, slow circular motions with your pelvis clockwise, then counter-clockwise.")
        ],
        "tip": "Keep both sit-bones firmly rooted on the surface; never force a deep stretch."
    },
    {
        "title": "🤍 Side-Lying Restorative Clamshell",
        "focus": "Glute activation & stabilizing pelvic ligaments",
        "steps": [
            ("Position", "Lie on your left side with knees bent at a 45-degree angle, supporting your head on your arm or a pillow."),
            ("Engage", "Keep feet pinned together and gently open the top knee upward without rolling your hips backwards."),
            ("Lower", "Slowly lower the knee back down with control."),
            ("Repetitions", "Perform 8 slow pulses on the left, rest, then flip to the right side.")
        ],
        "tip": "Place a small folded blanket under your bump if you need extra support while resting."
    },
    {
        "title": "🌿 Supported Ankle & Calf Pump Flow",
        "focus": "Enhancing lower leg venous return & reducing pedal edema",
        "steps": [
            ("Position", "Sit back comfortably in a supportive armchair with feet resting out straight on an ottoman."),
            ("Flex & Point", "Point your toes downward away from you, then flex toes back toward your shins slowly."),
            ("Ankle Circles", "Roll both ankles in outward circles 10 times, then reverse inward circles 10 times."),
            ("Rest", "Elevate feet slightly above hip level for a minute to encourage fluid drainage.")
        ],
        "tip": "Great for relieving evening heavy legs or mild ankle puffiness."
    }
]

# --- WIND DOWN DECKS ---
WIND_DOWN_DECKS = [
    {
        "title": "🌙 Evening Softening",
        "quote": "Release the expectations of the day. You grew life today; your body has done enough.",
        "steps": [
            "Dim the room lighting or switch to warm lamps.",
            "Unclench your jaw, soften your eyelids, and drop your shoulders down.",
            "Rest both hands over your bump or heart and take three quiet, unhurried breaths."
        ]
    },
    {
        "title": "🕊️ Quiet Bedtime Transition",
        "quote": "Nothing in tomorrow requires your energy tonight. Rest is your only task.",
        "steps": [
            "Put phones and screens face down on nightstand mode.",
            "Place a soft pillow between your knees or under your side for support.",
            "Silently whisper: 'Everything can wait until the sun rises.'"
        ]
    }
]

# --- SENSORY GROUNDING DECKS ---
GROUNDING_DECKS = [
    {
        "title": "Five Little Senses",
        "steps": [
            ("👀 See", "Notice 5 subtle colors or quiet shapes around you"),
            ("✋ Touch", "Feel the texture of 4 things (blanket, clothes, cool pillow, your hands)"),
            ("👂 Hear", "Listen for 3 gentle sounds (fan breeze, distant stillness, your breath)"),
            ("👃 Smell", "Catch 2 aromas lingering quietly in the air"),
            ("🤍 Cherish", "Name 1 gentle grace you give yourself today")
        ]
    }
]

def render_sanctuary_tab():
    st.markdown(
        """<style>
        .sanctuary-header {
            background: linear-gradient(135deg, #FBF8F5 0%, #F5EFE9 100%);
            border: 1px solid #ECE3DA;
            border-radius: 20px;
            padding: 18px 22px;
            margin-bottom: 18px;
        }
        .s-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            padding: 3px 10px;
            border-radius: 12px;
            background: #EFE8E1;
            color: #7A6B63;
            margin-bottom: 6px;
        }
        .sanctuary-card {
            background: #FFFFFF;
            border: 1px solid #F0EAE4;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            margin-bottom: 12px;
            min-height: 125px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .breathing-orb {
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, #FAF4F0 0%, #F4EAE4 75%);
            border: 3px solid #DECBC3;
            border-radius: 50%;
            margin: 16px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 25px rgba(222, 203, 195, 0.45);
            box-sizing: border-box;
            padding: 16px;
            text-align: center;
        }
        .pause-canvas {
            background: linear-gradient(180deg, #FBF9F7 0%, #F5EFEA 100%);
            border-radius: 20px;
            border: 1px solid #EBE4DD;
            padding: 24px 18px;
            text-align: center;
            margin-bottom: 16px;
        }
        </style>""",
        unsafe_allow_html=True
    )

    if "sanctuary_mode" not in st.session_state:
        st.session_state.sanctuary_mode = "home"
    if "session_completed" not in st.session_state:
        st.session_state.session_completed = False
    if "exercise_idx" not in st.session_state:
        st.session_state.exercise_idx = 0
    if "wind_down_idx" not in st.session_state:
        st.session_state.wind_down_idx = 0
    if "grounding_idx" not in st.session_state:
        st.session_state.grounding_idx = 0

    st.markdown(
        """<div class="sanctuary-header">
            <span class="s-badge">🕊️ HAVEN SANCTUARY</span>
            <h2 style="margin:2px 0; font-size:1.6rem; font-weight:700; color:#3E3733;">Sanctuary</h2>
            <p style="margin:3px 0 0 0; font-size:0.88rem; font-weight:600; color:#786960;">“Take a quiet moment. Gentle care for your mind and body.”</p>
        </div>""",
        unsafe_allow_html=True
    )

    if st.session_state.session_completed:
        st.markdown(
            """<div class="pause-canvas">
                <h3 style="color:#4A403A; margin:0 0 8px 0;">🤍 You gave yourself a mindful pause.</h3>
                <p style="color:#786B63; font-size:0.86rem; margin:0 0 16px 0;">Consistency and softness over perfection.</p>
            </div>""",
            unsafe_allow_html=True
        )
        st.caption("How do you feel right now?")
        fb_cols = st.columns(5)
        options = ["😌 Calmer", "🥰 Soothed", "😴 Restful", "😊 Refreshed", "🤍 Just Okay"]
        for idx, fb in enumerate(options):
            with fb_cols[idx]:
                if st.button(fb, key=f"fb_btn_{idx}", use_container_width=True):
                    entry = {
                        "id": str(uuid.uuid4())[:8],
                        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "time": datetime.datetime.now().strftime("%I:%M %p"),
                        "activity_type": st.session_state.get("last_activity", "General"),
                        "duration_min": st.session_state.get("last_duration", 3),
                        "sound_used": "None",
                        "feedback": fb
                    }
                    save_sanctuary_session(entry)
                    st.session_state.session_completed = False
                    st.session_state.sanctuary_mode = "home"
                    st.rerun()
        return

    mode = st.session_state.sanctuary_mode

    # --- 1. HOME DASHBOARD ---
    if mode == "home":
        st.markdown("##### What would support you right now?")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """<div class="sanctuary-card">
                    <span style="font-size:1.7rem;">🌬️</span>
                    <strong style="color:#403632; font-size:0.95rem;">Counted Breathing</strong>
                    <span style="color:#8A7B73; font-size:0.75rem;">Inhale (4s) • Hold (4s) • Exhale (4s) visual flow</span>
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Open Breathing Timer", key="card_btn_breath", use_container_width=True):
                st.session_state.sanctuary_mode = "breathe"
                st.rerun()

        with c2:
            st.markdown(
                """<div class="sanctuary-card">
                    <span style="font-size:1.7rem;">🧘‍♀️</span>
                    <strong style="color:#403632; font-size:0.95rem;">Gentle Movement</strong>
                    <span style="color:#8A7B73; font-size:0.75rem;">Prenatal-safe stretches & low-back release routines</span>
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Open Gentle Movement", key="card_btn_exercise", use_container_width=True):
                st.session_state.exercise_idx = random.randint(0, len(EXERCISE_DECKS) - 1)
                st.session_state.sanctuary_mode = "exercise"
                st.rerun()

        c3, c4 = st.columns(2)
        with c3:
            st.markdown(
                """<div class="sanctuary-card">
                    <span style="font-size:1.7rem;">🌙</span>
                    <strong style="color:#403632; font-size:0.92rem;">Wind Down</strong>
                    <span style="color:#8A7B73; font-size:0.75rem;">Bedtime rituals & unhurried nervous system soothing</span>
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Open Wind Down", key="card_btn_wind", use_container_width=True):
                st.session_state.wind_down_idx = random.randint(0, len(WIND_DOWN_DECKS) - 1)
                st.session_state.sanctuary_mode = "winddown"
                st.rerun()

        with c4:
            st.markdown(
                """<div class="sanctuary-card">
                    <span style="font-size:1.7rem;">🌿</span>
                    <strong style="color:#403632; font-size:0.92rem;">Sensory Grounding</strong>
                    <span style="color:#8A7B73; font-size:0.75rem;">5-4-3-2-1 centering awareness deck</span>
                </div>""",
                unsafe_allow_html=True
            )
            if st.button("Open Grounding", key="card_btn_ground", use_container_width=True):
                st.session_state.grounding_idx = random.randint(0, len(GROUNDING_DECKS) - 1)
                st.session_state.sanctuary_mode = "ground"
                st.rerun()

        history = get_sanctuary_history()
        if not history.empty:
            st.write("")
            st.markdown("##### 🕊️ Quiet Moments Shared")
            total_mins = history["duration_min"].astype(int).sum() if "duration_min" in history else 0
            st.markdown(
                f"""<div style="background:#FAF8F5; border:1px solid #EBE4DD; border-radius:14px; padding:12px 18px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.85rem; color:#6B5F58;">Total mindful minutes logged:</span>
                    <span style="font-size:1.05rem; font-weight:700; color:#524640;">{total_mins} mins</span>
                </div>""",
                unsafe_allow_html=True
            )

    # --- 2. COUNTED BREATHING ---
    elif mode == "breathe":
        st.button("← Back to Sanctuary", on_click=lambda: setattr(st.session_state, "sanctuary_mode", "home"))

        st.markdown(
            """<div class="pause-canvas">
                <span style="font-size:0.76rem; font-weight:700; color:#9E8B82; text-transform:uppercase;">Rhythmic Paced Breathing</span>
                <h3 style="color:#3B322D; margin:4px 0 0 0;">4-4-4 Gentle Flow 🌸</h3>
                <p style="color:#786B63; font-size:0.84rem; margin-top:4px;">
                    Count along as you gently breathe in, hold, and release.
                </p>
            </div>""",
            unsafe_allow_html=True
        )

        col_c1, _ = st.columns([1, 1])
        with col_c1:
            cycles = st.selectbox("Number of Breath Cycles:", [3, 5, 8], index=0, format_func=lambda x: f"{x} Cycles (~{x*14}s)")

        cycle_status_placeholder = st.empty()
        orb_placeholder = st.empty()

        cycle_status_placeholder.markdown(
            "<div style='text-align:center; font-size:0.85rem; font-weight:600; color:#8C7B73; margin-bottom:4px;'>🌸 Press Start to begin breathing together</div>", 
            unsafe_allow_html=True
        )
        orb_placeholder.markdown(
            """<div class="breathing-orb">
                <span style="font-size:1.05rem; font-weight:700; color:#685850;">Ready</span>
                <span style="font-size:2.8rem; font-weight:300; color:#403632; margin-top:4px;">—</span>
            </div>""",
            unsafe_allow_html=True
        )

        btn_start_col, btn_stop_col = st.columns(2)
        with btn_start_col:
            start_btn = st.button("▶ Start Counted Breath", use_container_width=True)
        with btn_stop_col:
            finish_btn = st.button("Complete Session 🤍", use_container_width=True)

        if start_btn:
            phases = [
                ("Inhale 🌿", 4, "#4E7B5E"),
                ("Hold 🤍", 4, "#7E6E66"),
                ("Exhale ☁️", 4, "#A85E52"),
                ("Rest 🕊️", 2, "#8F7D74")
            ]

            for cycle in range(1, cycles + 1):
                cycle_status_placeholder.markdown(
                    f"<div style='text-align:center; font-size:0.88rem; font-weight:700; color:#5A4D46; margin-bottom:4px;'>🌿 Cycle {cycle} of {cycles}</div>", 
                    unsafe_allow_html=True
                )
                for phase_name, count_seconds, phase_color in phases:
                    for sec in range(count_seconds, 0, -1):
                        orb_placeholder.markdown(
                            f"""<div class="breathing-orb" style="border-color:{phase_color};">
                                <span style="font-size:1.05rem; font-weight:700; color:{phase_color}; letter-spacing:0.5px;">
                                    {phase_name}
                                </span>
                                <span style="font-size:3.6rem; font-weight:300; color:#382D28; margin-top:4px; line-height:1;">
                                    {sec}
                                </span>
                            </div>""",
                            unsafe_allow_html=True
                        )
                        time.sleep(1)

            cycle_status_placeholder.empty()
            orb_placeholder.markdown(
                """<div class="breathing-orb" style="border-color:#4E7B5E;">
                    <span style="font-size:2.2rem;">🌸</span>
                    <span style="font-size:1.05rem; font-weight:700; color:#4E7B5E; margin-top:6px;">Well Done</span>
                </div>""",
                unsafe_allow_html=True
            )
            st.success("🤍 You completed your breathing rhythm. Take a calm breath.")

        if finish_btn:
            st.session_state.last_activity = "Counted Breath"
            st.session_state.last_duration = max(1, (cycles * 14) // 60)
            st.session_state.session_completed = True
            st.rerun()

    # --- 3. GENTLE MOVEMENT & EXERCISE (REPLACED JUST PAUSE) ---
    elif mode == "exercise":
        c_nav1, c_nav2 = st.columns([2, 1])
        with c_nav1:
            st.button("← Back to Sanctuary", on_click=lambda: setattr(st.session_state, "sanctuary_mode", "home"))
        with c_nav2:
            if st.button("✨ Another Stretch", use_container_width=True):
                st.session_state.exercise_idx = (st.session_state.exercise_idx + 1) % len(EXERCISE_DECKS)
                st.rerun()

        deck = EXERCISE_DECKS[st.session_state.exercise_idx]
        st.markdown(
            f"""<div class="pause-canvas">
                <span style="font-size:2rem;">🧘‍♀️</span>
                <h3 style="color:#3B322D; margin:4px 0 2px 0;">{deck['title']}</h3>
                <p style="color:#8A7A71; font-size:0.85rem; margin:0 0 10px 0; font-weight:600;">
                    Focus: {deck['focus']}
                </p>
            </div>""",
            unsafe_allow_html=True
        )

        for step_title, step_desc in deck["steps"]:
            st.markdown(f"**{step_title}:** {step_desc}")

        st.markdown(
            f"""<div style="background:#FAF6F3; border:1px dashed #E0D3CB; border-radius:12px; padding:10px 14px; margin-top:14px; font-size:0.82rem; color:#786960;">
                💡 <b>Gentle Tip:</b> {deck['tip']}
            </div>""",
            unsafe_allow_html=True
        )

        st.write("")
        if st.button("Complete Movement Routine 🤍", use_container_width=True):
            st.session_state.last_activity = "Gentle Movement"
            st.session_state.last_duration = 5
            st.session_state.session_completed = True
            st.rerun()

    # --- 4. WIND DOWN ---
    elif mode == "winddown":
        c_nav1, c_nav2 = st.columns([2, 1])
        with c_nav1:
            st.button("← Back to Sanctuary", on_click=lambda: setattr(st.session_state, "sanctuary_mode", "home"))
        with c_nav2:
            if st.button("✨ Another Routine", use_container_width=True):
                st.session_state.wind_down_idx = (st.session_state.wind_down_idx + 1) % len(WIND_DOWN_DECKS)
                st.rerun()

        deck = WIND_DOWN_DECKS[st.session_state.wind_down_idx]
        st.markdown(
            f"""<div class="pause-canvas">
                <span style="font-size:2rem;">🌙</span>
                <h3 style="color:#3B322D; margin:4px 0 2px 0;">{deck['title']}</h3>
                <p style="color:#7D7068; font-size:0.86rem; font-style:italic; margin-bottom:16px;">
                    “{deck['quote']}”
                </p>
            </div>""",
            unsafe_allow_html=True
        )
        for i, step in enumerate(deck["steps"], 1):
            st.markdown(f"**{i}.** {step}")

        st.write("")
        if st.button("Complete Wind-Down 🤍", use_container_width=True):
            st.session_state.last_activity = "Wind Down"
            st.session_state.last_duration = 5
            st.session_state.session_completed = True
            st.rerun()

    # --- 5. GROUNDING ---
    elif mode == "ground":
        st.button("← Back to Sanctuary", on_click=lambda: setattr(st.session_state, "sanctuary_mode", "home"))

        g_deck = GROUNDING_DECKS[0]
        st.markdown(
            f"""<div class="pause-canvas">
                <span style="font-size:2rem;">🌿</span>
                <h3 style="color:#3A312C; margin:4px 0 2px 0;">{g_deck['title']}</h3>
                <p style="color:#786B63; font-size:0.85rem; margin-bottom:14px;">
                    Follow these gentle cues to anchor your awareness.
                </p>
            </div>""",
            unsafe_allow_html=True
        )
        for tag, text in g_deck["steps"]:
            st.markdown(f"**{tag}:** {text}")

        st.write("")
        if st.button("I Feel Centered 🌿", use_container_width=True):
            st.session_state.last_activity = "Grounding"
            st.session_state.last_duration = 3
            st.session_state.session_completed = True
            st.rerun()

    st.markdown(
        """<div style="margin-top:28px; padding:12px 16px; background:#FAF8F6; border-radius:14px; border-left:3px solid #D6CBC4; font-size:0.75rem; color:#8C8078;">
            🕊️ <b>Sanctuary Comfort Note:</b> Sanctuary is a quiet wellness space inside Haven. 
            It is designed for stress relief, calm breathing, and gentle movement. It does not provide medical diagnosis or replace prenatal clinical advice.
        </div>""",
        unsafe_allow_html=True
    )