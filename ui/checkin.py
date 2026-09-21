# ui/checkin.py
import datetime
import streamlit as st
from core.storage import save_checkin

def render_checkin_tab(engine):
    today_str = datetime.date.today().strftime("%A, %d %B")
    week = st.session_state.get("gestational_week", 24)

    # Initialize Symptom & Comfort Session States
    if "symptom_headache" not in st.session_state:
        st.session_state.symptom_headache = "None"
    if "symptom_vision" not in st.session_state:
        st.session_state.symptom_vision = "Clear & Normal"
    if "symptom_swelling" not in st.session_state:
        st.session_state.symptom_swelling = "None"
    if "symptom_breath" not in st.session_state:
        st.session_state.symptom_breath = "Easy & Calm"
    if "symptom_tummy" not in st.session_state:
        st.session_state.symptom_tummy = "Comfortable"

    if "comfort_sleep" not in st.session_state:
        st.session_state.comfort_sleep = "Deep & Dreamy 🌙"
    if "comfort_energy" not in st.session_state:
        st.session_state.comfort_energy = "Steady Pace 🌿"

    # 1. Header
    st.markdown(f"""
    <div style="padding: 4px 2px 16px 2px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <h2 style="margin:0; font-size:1.65rem; font-weight:700; color:#3D2B28;">
                    💗 Today’s Check-in
                </h2>
                <p style="margin:3px 0 0 0; font-size:0.88rem; color:#856E6A;">
                    A gentle, 60-second vitals tune-up for you and peanut.
                </p>
            </div>
            <div style="text-align:right;">
                <span style="font-size:0.75rem; color:#8C7571; font-weight:600; background:#FAF2EF; padding:4px 10px; border-radius:12px; border:1px solid #EFE2DD; display:inline-block;">
                    🗓️ {today_str} • W{week}
                </span>
                <div style="margin-top:4px; font-size:0.75rem; font-weight:700; color:{'#4B8664' if st.session_state.get('checkin_completed') else '#B8584B'};">
                    {'✓ Completed today' if st.session_state.get('checkin_completed') else '⏳ Incomplete'}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # If already completed today, show Summary
    if st.session_state.get("checkin_completed") and not st.session_state.get("editing_checkin", False):
        last_eval = st.session_state.get("latest_evaluation", {})
        last_inputs = st.session_state.get("latest_inputs", {})
        
        sbp_val = int(last_inputs.get("systolic_bp", 120))
        dbp_val = int(last_inputs.get("diastolic_bp", 80))
        hr_val = int(last_inputs.get("heart_rate", 75))
        wt_val = last_inputs.get("weight", 65.0)
        bs_val = last_inputs.get("blood_sugar", 6.0)
        syms_val = last_inputs.get("symptoms_summary", "None reported")

        st.markdown(f"""
        <div class="warm-card" style="background:#FFFFFF; border:1px solid #EFE3DF;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.92rem; font-weight:700; color:#3D2B28;">✓ Today’s Check-in is on Record</span>
                <span style="font-size:0.75rem; color:#5D8C72; background:#EDF5F0; padding:3px 10px; border-radius:10px; font-weight:600;">Saved & Safe</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:14px; font-size:0.85rem; color:#5A4744;">
                <div>🩺 <b>Blood Pressure:</b> {sbp_val}/{dbp_val} mmHg</div>
                <div>❤️ <b>Pulse:</b> {hr_val} bpm</div>
                <div>⚖️ <b>Weight:</b> {wt_val} kg</div>
                <div>🍯 <b>Fasting Sugar:</b> {bs_val} mmol/L</div>
            </div>
            <div style="margin-top:10px; font-size:0.82rem; color:#786460; border-top:1px dashed #F2E4DF; padding-top:8px;">
                <b>Body Sensations:</b> {syms_val}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✏️ Edit Today's Check-in", key="btn_reopen_checkin"):
            st.session_state.editing_checkin = True
            st.rerun()

        render_assessment_results(last_eval, last_inputs)
        return

    # ----------------------------------------------------
    # 2. VITALS SECTION
    # ----------------------------------------------------
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#3D2B28;'>🩺 Today’s Vitals</div>", unsafe_allow_html=True)
    st.caption("Standard home-monitor readings for baseline hemodynamic tracking.")

    v1, v2 = st.columns(2)
    with v1:
        sbp = st.number_input("Systolic BP (Upper)", min_value=70, max_value=220, value=120, step=1)
        dbp = st.number_input("Diastolic BP (Lower)", min_value=40, max_value=140, value=80, step=1)
        weight = st.number_input("Weight Today (kg)", min_value=35.0, max_value=160.0, value=65.0, step=0.1)

    with v2:
        hr = st.number_input("Resting Heart Rate (bpm)", min_value=45, max_value=160, value=76, step=1)
        blood_sugar = st.number_input("Fasting Glucose (mmol/L)", min_value=2.5, max_value=22.0, value=6.2, step=0.1)
        age = st.session_state.get("mama_age", 28)
        st.markdown(f"""
        <div style="margin-top:28px; background:#FAF5F2; padding:10px 14px; border-radius:12px; font-size:0.8rem; color:#786460;">
            Maternal Age: <b>{age} years</b> (from profile)
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 3. HOW ARE YOU FEELING BODILY?
    # ----------------------------------------------------
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:1.05rem; font-weight:700; color:#3D2B28;">🌷 How are you feeling bodily?</div>
            <div style="font-size:0.82rem; color:#856E6A; margin-top:2px;">Tap what resonates today—no heavy questionnaires.</div>
        </div>
        <span style="font-size:0.75rem; background:#FAF2EF; color:#B8584B; padding:3px 10px; border-radius:10px; font-weight:600;">Tap to select</span>
    </div>
    <div style="height:12px;"></div>
    """, unsafe_allow_html=True)

    st.markdown("<span style='font-size:0.82rem; font-weight:700; color:#5A4744;'>Head & Clarity</span>", unsafe_allow_html=True)
    hc1, hc2, hc3, hc4 = st.columns(4)
    with hc1:
        if st.button(f"{'✓ ' if st.session_state.symptom_headache == 'None' else ''}Clear Head 🌸", key="chip_h_none", use_container_width=True):
            st.session_state.symptom_headache = "None"
            st.rerun()
    with hc2:
        if st.button(f"{'✓ ' if st.session_state.symptom_headache == 'Mild' else ''}Mild Heaviness ☁️", key="chip_h_mild", use_container_width=True):
            st.session_state.symptom_headache = "Mild"
            st.rerun()
    with hc3:
        if st.button(f"{'✓ ' if st.session_state.symptom_headache == 'Severe' else ''}Throbbing Ache ⚡", key="chip_h_sev", use_container_width=True):
            st.session_state.symptom_headache = "Severe"
            st.rerun()
    with hc4:
        has_aura = (st.session_state.symptom_vision == "Sparkles / Blur")
        if st.button(f"{'✓ ' if has_aura else ''}Visual Sparks ✨", key="chip_v_sparks", use_container_width=True):
            st.session_state.symptom_vision = "Clear & Normal" if has_aura else "Sparkles / Blur"
            st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.82rem; font-weight:700; color:#5A4744;'>Swelling & Digestion</span>", unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        is_sw_none = (st.session_state.symptom_swelling == "None")
        if st.button(f"{'✓ ' if is_sw_none else ''}No Swelling 🕊️", key="chip_sw_none", use_container_width=True):
            st.session_state.symptom_swelling = "None"
            st.rerun()
    with fc2:
        is_sw_puffy = (st.session_state.symptom_swelling == "Puffy Feet")
        if st.button(f"{'✓ ' if is_sw_puffy else ''}Puffy Ankles / Hands 🫧", key="chip_sw_puffy", use_container_width=True):
            st.session_state.symptom_swelling = "Puffy Feet"
            st.rerun()
    with fc3:
        has_tummy = (st.session_state.symptom_tummy == "Upper Rib Pain")
        if st.button(f"{'✓ ' if has_tummy else ''}Upper Rib Ache 🩺", key="chip_tummy_ache", use_container_width=True):
            st.session_state.symptom_tummy = "Comfortable" if has_tummy else "Upper Rib Pain"
            st.rerun()

    if st.session_state.symptom_swelling == "Puffy Feet":
        st.markdown("<div style='font-size:0.78rem; color:#8C7571; font-style:italic; margin-top:6px;'>💡 Pro-tip: Elevate your feet above heart level for 15 minutes to let fluids drain gently.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 4. TODAY’S DAILY COMFORT
    # ----------------------------------------------------
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:700; color:#3D2B28;">🌿 Today’s Daily Comfort</div>
    <div style="font-size:0.82rem; color:#856E6A; margin-top:2px;">A gentle pulse check for your scrapbook journey (non-clinical).</div>
    <div style="height:12px;"></div>
    """, unsafe_allow_html=True)

    st.markdown("<span style='font-size:0.82rem; font-weight:700; color:#5A4744;'>Sleep Sanctuary</span>", unsafe_allow_html=True)
    sl1, sl2, sl3 = st.columns(3)
    with sl1:
        if st.button(f"{'✓ ' if st.session_state.comfort_sleep == 'Tossing & Turning 🪺' else ''}Restless 🪺", key="sleep_restless", use_container_width=True):
            st.session_state.comfort_sleep = "Tossing & Turning 🪺"
            st.rerun()
    with sl2:
        if st.button(f"{'✓ ' if st.session_state.comfort_sleep == 'A Bit Light ☁️' else ''}A Bit Light ☁️", key="sleep_light", use_container_width=True):
            st.session_state.comfort_sleep = "A Bit Light ☁️"
            st.rerun()
    with sl3:
        if st.button(f"{'✓ ' if st.session_state.comfort_sleep == 'Deep & Dreamy 🌙' else ''}Deep & Dreamy 🌙", key="sleep_deep", use_container_width=True):
            st.session_state.comfort_sleep = "Deep & Dreamy 🌙"
            st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.82rem; font-weight:700; color:#5A4744;'>Energy Battery</span>", unsafe_allow_html=True)
    eg1, eg2, eg3 = st.columns(3)
    with eg1:
        if st.button(f"{'✓ ' if st.session_state.comfort_energy == 'Slow Motion 🪫' else ''}Slow Motion 🪫", key="energy_slow", use_container_width=True):
            st.session_state.comfort_energy = "Slow Motion 🪫"
            st.rerun()
    with eg2:
        if st.button(f"{'✓ ' if st.session_state.comfort_energy == 'Steady Pace 🌿' else ''}Steady Pace 🌿", key="energy_steady", use_container_width=True):
            st.session_state.comfort_energy = "Steady Pace 🌿"
            st.rerun()
    with eg3:
        if st.button(f"{'✓ ' if st.session_state.comfort_energy == 'Sparkly & Bright ✨' else ''}Sparkly ✨", key="energy_spark", use_container_width=True):
            st.session_state.comfort_energy = "Sparkly & Bright ✨"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 5. SUBMIT BUTTON
    # ----------------------------------------------------
    st.markdown("<div class='primary-pill' style='margin-top:10px;'>", unsafe_allow_html=True)
    if st.button("Check in with Haven →", key="btn_submit_checkin", use_container_width=True):
        if sbp <= dbp:
            st.error("Please verify your readings: Systolic pressure must be higher than diastolic.")
            return

        symptoms_present = []
        if st.session_state.symptom_headache != "None":
            symptoms_present.append(f"{st.session_state.symptom_headache.lower()} headache")
        if st.session_state.symptom_vision == "Sparkles / Blur":
            symptoms_present.append("visual changes")
        if st.session_state.symptom_swelling == "Puffy Feet":
            symptoms_present.append("swelling")
        if st.session_state.symptom_tummy == "Upper Rib Pain":
            symptoms_present.append("epigastric discomfort")

        has_urgent_symptoms = (
            st.session_state.symptom_headache == "Severe" or 
            st.session_state.symptom_vision == "Sparkles / Blur" or 
            st.session_state.symptom_tummy == "Upper Rib Pain" or
            (sbp >= 140 or dbp >= 90)
        )

        user_inputs = {
            "age": age,
            "systolic_bp": float(sbp),
            "diastolic_bp": float(dbp),
            "weight": float(weight),
            "heart_rate": float(hr),
            "blood_sugar": float(blood_sugar),
            "symptoms_count": len(symptoms_present),
            "symptoms_summary": ", ".join(symptoms_present) if symptoms_present else "Comfortable & clear",
            "sleep_quality": st.session_state.comfort_sleep,
            "energy_level": st.session_state.comfort_energy,
            "has_urgent_symptoms": has_urgent_symptoms
        }

        eval_result = engine.evaluate(user_inputs)

        record = {
            **user_inputs,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "risk_tier": eval_result["risk_tier"],
            "risk_percentage": int(eval_result["probability"] * 100),
            "water_glasses": st.session_state.get("water_count", 5),
            "mood": st.session_state.get("selected_mood", "Serene"),
            "journal_note": ""
        }
        save_checkin(record)

        st.session_state.checkin_completed = True
        st.session_state.editing_checkin = False
        st.session_state.latest_evaluation = eval_result
        st.session_state.latest_inputs = user_inputs
        st.session_state.needs_gentle_review = eval_result["is_elevated"] or has_urgent_symptoms

        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_assessment_results(eval_result, user_inputs):
    if not eval_result:
        return

    # Safety Notice Banner
    if user_inputs.get("has_urgent_symptoms"):
        st.markdown("""
        <div style="background:#FFF6F4; border:1px solid #F5D2CB; border-radius:18px; padding:16px 20px; margin-top:20px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.1rem;">🩺</span>
                <span style="font-size:0.88rem; font-weight:700; color:#A84335;">Symptom Safety Notice</span>
            </div>
            <p style="font-size:0.84rem; color:#6B433D; margin:6px 0 0 0; line-height:1.4;">
                You recorded symptoms or blood pressure readings that warrant prompt medical review. 
                Even if overall indicators fluctuate, we encourage you to contact your healthcare provider or clinic today for reassurance.
            </p>
        </div>
        """, unsafe_allow_html=True)

    prob_pct = int(eval_result.get("probability", 0.0) * 100)
    tier = eval_result.get("risk_tier", "Lower-Risk Pattern")
    badge_col = eval_result.get("color", "#5D8C72")
    summary = eval_result.get("human_summary", "Vitals are within expected ranges.")
    is_elevated = eval_result.get("is_elevated", False)

    advisory_text = (
        "Haven noticed a pattern in your readings that may benefit from closer attention and discussion with your maternity team."
        if is_elevated else
        "No concerning hemodynamic patterns were identified in the information provided today."
    )

    assessment_html = f"""
    <div class="warm-card" style="border:1px solid #F2E3DE; margin-top:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.8rem; font-weight:700; color:#9E8783; text-transform:uppercase; letter-spacing:0.8px;">
                ✨ Haven’s Assessment
            </span>
            <span style="background:#FAF2EF; color:{badge_col}; font-weight:700; font-size:0.8rem; padding:3px 12px; border-radius:9999px; border:1px solid #EFE4E0;">
                {tier}
            </span>
        </div>
        <p style="font-size:0.84rem; color:#786460; margin:8px 0 12px 0;">
            Your current readings were assessed by Haven’s machine learning model based on clinical hemodynamic patterns.
        </p>
        <div style="display:flex; align-items:baseline; gap:10px;">
            <span style="font-size:2.2rem; font-weight:700; color:{badge_col}; line-height:1;">
                {prob_pct}%
            </span>
            <span style="font-size:0.82rem; color:#8C7571;">Relative risk stratification score</span>
        </div>
        <p style="font-size:0.88rem; color:#4A3B39; margin:12px 0 0 0; line-height:1.4;">
            {advisory_text}
        </p>
        <div style="margin-top:14px; font-size:0.72rem; color:#A8918D; border-top:1px dashed #F2E4DF; padding-top:8px;">
            ℹ️ Haven provides AI-generated risk information for surveillance and support. It is not a diagnosis and does not replace professional medical care.
        </div>
    </div>
    """
    st.markdown(assessment_html, unsafe_allow_html=True)

    # SHAP Explainability Card (Clean, Simple, No Empty Boxes)
    st.markdown(f"""
    <div class="warm-card" style="margin-top:16px;">
        <div style="font-size:1rem; font-weight:700; color:#3D2B28;">
            🔍 Why did Haven give this result?
        </div>
        <p style="font-size:0.84rem; color:#786460; margin:4px 0 12px 0;">
            <b>In simple words:</b> {summary}
        </p>
        <div style="font-size:0.82rem; font-weight:700; color:#5A4744; margin-bottom:8px;">
            What influenced this result the most?
        </div>
    """, unsafe_allow_html=True)

    for dr in eval_result.get("top_drivers", []):
        st.markdown(f"""
        <div style="background:#FAF6F4; border:1px solid #F3E8E4; border-radius:12px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-weight:600; color:#3D2B28; font-size:0.85rem;">{dr['label']}</span><br>
                <span style="font-size:0.75rem; color:#8C7571;">{dr['impact']}</span>
            </div>
            <span style="font-size:0.78rem; font-weight:700; color:#9E5246; background:#F5E5E1; padding:2px 8px; border-radius:8px;">
                Top Signal
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Next Steps Card
    st.markdown("""
    <div class="warm-card" style="margin-top:16px;">
        <div style="font-size:1rem; font-weight:700; color:#3D2B28;">🌷 What now?</div>
        <div style="font-size:0.85rem; color:#5A4744; margin-top:6px; line-height:1.5;">
    """, unsafe_allow_html=True)

    if is_elevated or user_inputs.get("has_urgent_symptoms"):
        st.markdown("""
        • <b>Review with your Doctor:</b> Mention today's readings and symptoms at your next visit or clinic call.<br>
        • <b>Hydrate & Rest:</b> Sit comfortably, elevate your feet for 15 minutes, and take slow, deep breaths.<br>
        • <b>Re-check when calm:</b> If advised by your provider, re-measure vitals after quiet rest.
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        • <b>Keep up your steady rhythm:</b> Daily check-ins help detect subtle shifts early.<br>
        • <b>Stay hydrated:</b> Log your water dewdrops on Home.<br>
        • <b>Rest your mind:</b> Take a quiet moment in Sanctuary whenever you need a pause.
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([2, 1])
    with col_nav2:
        if st.button("View Journey History →", key="btn_goto_journey_from_chk"):
            st.session_state.active_tab_redirect = "📖 Journey"
            st.rerun()