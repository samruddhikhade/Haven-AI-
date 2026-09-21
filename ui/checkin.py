# ui/checkin.py
import datetime
import streamlit as st
from core.storage import save_checkin

def render_checkin_tab(engine):
    today_str = datetime.date.today().strftime("%A, %d %B")
    week = st.session_state.get("gestational_week", 24)

    # 1. Header
    st.markdown(f"""
    <div style="padding: 6px 2px 18px 2px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <h2 style="margin:0; font-size:1.65rem; font-weight:700; color:#3D2B28;">
                    💗 Today’s Check-in
                </h2>
                <p style="margin:3px 0 0 0; font-size:0.88rem; color:#856E6A;">
                    A little check-in for you and your little one.
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

    # If already completed today
    if st.session_state.get("checkin_completed") and not st.session_state.get("editing_checkin", False):
        last_eval = st.session_state.get("latest_evaluation", {})
        last_inputs = st.session_state.get("latest_inputs", {})
        
        sbp_val = int(last_inputs.get("systolic_bp", 120))
        dbp_val = int(last_inputs.get("diastolic_bp", 80))
        hr_val = int(last_inputs.get("heart_rate", 75))
        wt_val = last_inputs.get("weight", 65.0)
        bs_val = last_inputs.get("blood_sugar", 6.0)
        syms_val = last_inputs.get("symptoms_summary", "None reported")

        # Soft Card - No Harsh Green Side Border!
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

    # 2. Vitals Form
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#3D2B28;'>🩺 Today’s Vitals</div>", unsafe_allow_html=True)
    st.caption("Values needed for hemodynamic trajectory assessment.")

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

    # 3. Symptoms Form
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#3D2B28;'>🌷 How are you feeling bodily?</div>", unsafe_allow_html=True)
    st.caption("Tap any noticeable symptoms experiencing today.")

    s_c1, s_c2 = st.columns(2)
    with s_c1:
        headache = st.selectbox("Headache", ["None", "Mild", "Persistent / Severe"])
        vision = st.selectbox("Vision changes (blur / sparkles)", ["No", "Yes"])
        swelling = st.selectbox("Swelling (hands or face)", ["None", "Mild", "Noticeable / Puffy"])

    with s_c2:
        breath = st.selectbox("Shortness of breath (resting)", ["No", "Yes"])
        nausea = st.selectbox("Nausea / vomiting", ["None", "Mild", "Significant"])
        epigastric = st.selectbox("Upper right abdominal ache", ["No", "Yes"])
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Optional Wellness
    st.markdown("<div class='warm-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#3D2B28;'>🌿 Today’s Daily Comfort (Optional)</div>", unsafe_allow_html=True)
    st.caption("Purely for your companion journey tracking—not used in clinical assessment.")

    w_c1, w_c2 = st.columns(2)
    with w_c1:
        sleep_quality = st.select_slider("Sleep Quality", ["Poor", "Okay", "Restful & Good"], value="Okay")
    with w_c2:
        energy_level = st.select_slider("Daily Energy", ["Tired", "Steady", "Grounded"], value="Steady")
    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Submit Button
    st.markdown("<div class='primary-pill' style='margin-top:10px;'>", unsafe_allow_html=True)
    if st.button("Check in with Haven →", key="btn_submit_checkin", use_container_width=True):
        if sbp <= dbp:
            st.error("Please verify your readings: Systolic pressure must be higher than diastolic.")
            return

        symptoms_present = []
        if headache != "None": symptoms_present.append(f"{headache.lower()} headache")
        if vision == "Yes": symptoms_present.append("visual changes")
        if swelling != "None": symptoms_present.append(f"{swelling.lower()} swelling")
        if breath == "Yes": symptoms_present.append("shortness of breath")
        if nausea != "None": symptoms_present.append(f"{nausea.lower()} nausea")
        if epigastric == "Yes": symptoms_present.append("epigastric discomfort")

        has_urgent_symptoms = (
            headache == "Persistent / Severe" or 
            vision == "Yes" or 
            epigastric == "Yes" or
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
            "symptoms_summary": ", ".join(symptoms_present) if symptoms_present else "None reported",
            "sleep_quality": sleep_quality,
            "energy_level": energy_level,
            "has_urgent_symptoms": has_urgent_symptoms
        }

        eval_result = engine.evaluate(user_inputs)

        record = {
            **user_inputs,
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

    # Safety Notice
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

    # Haven's Assessment - Clean Soft Border (No Green Line)
    st.markdown(f"""
    <div class="warm-card" style="border:1px solid #F2E3DE; margin-top:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.8rem; font-weight:700; color:#9E8783; text-transform:uppercase; letter-spacing:0.8px;">
                ✨ HAVEN’S ASSESSMENT
            </span>
            <span style="background:#FAF2EF; color:{badge_col}; font-weight:700; font-size:0.8rem; padding:3px 12px; border-radius:9999px; border:1px solid #EFE4E0;">
                {tier}
            </span>
        </div>
        
        <p style="font-size:0.84rem; color:#786460; margin:8px 0 12px 0;">
            Your current readings were assessed by Haven’s machine learning model based on clinical hemodynamic patterns.
        </p>

        <div style="display:flex; align-items:baseline; gap:10px;">
            <div style="font-size:2.2rem; font-weight:700; color:{badge_col}; line-height:1;">
                {prob_pct}%
            </div>
            <span style="font-size:0.82rem; color:#8C7571;">Relative risk stratification score</span>
        </div>

        <p style="font-size:0.88rem; color:#4A3B39; margin:12px 0 0 0; line-height:1.4;">
            {"Haven noticed a pattern in your readings that may benefit from closer attention and discussion with your maternity team." if eval_result.get("is_elevated") else "No concerning hemodynamic patterns were identified in the information provided today."}
        </p>

        <div style="margin-top:14px; font-size:0.72rem; color:#A8918D; border-top:1px dashed #F2E4DF; padding-top:8px;">
            ℹ️ Haven provides AI-generated risk information for surveillance and support. It is not a diagnosis and does not replace professional medical care.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SHAP Explainability Card
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

    with st.expander("Technical SHAP Details"):
        st.caption("Feature values passed into XGBoost and corresponding TreeSHAP coefficients:")
        shap_table = [
            {"Feature": item["label"], "Recorded Value": round(item["actual_value"], 2), "SHAP Contribution": round(item["shap_value"], 4)}
            for item in eval_result.get("all_shap_details", [])
        ]
        st.dataframe(shap_table, hide_index=True, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Next Steps
    st.markdown("""
    <div class="warm-card" style="margin-top:16px;">
        <div style="font-size:1rem; font-weight:700; color:#3D2B28;">🌷 What now?</div>
        <div style="font-size:0.85rem; color:#5A4744; margin-top:6px; line-height:1.5;">
    """, unsafe_allow_html=True)

    if eval_result.get("is_elevated") or user_inputs.get("has_urgent_symptoms"):
        st.markdown("""
        • <b>Review with your Doctor:</b> Mention today's blood pressure reading at your next scheduled visit, or sooner if symptoms persist.<br>
        • <b>Hydrate & Rest:</b> Sit comfortably, elevate your feet for 15 minutes, and take slow, deep breaths.<br>
        • <b>Re-check when calm:</b> If advised by your provider, re-measure your blood pressure after 30 minutes of quiet rest.
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        • <b>Keep up your steady rhythm:</b> Daily check-ins allow Haven to detect subtle drift before clinical symptoms appear.<br>
        • <b>Stay hydrated:</b> Log your water dewdrops on Home to keep circulation fluid and comfortable.<br>
        • <b>Rest your mind:</b> Take a quiet moment in Sanctuary whenever you need a breather.
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([2, 1])
    with col_nav2:
        if st.button("View Journey History →", key="btn_goto_journey_from_chk"):
            st.session_state.active_tab_redirect = "📖 Journey"
            st.rerun()