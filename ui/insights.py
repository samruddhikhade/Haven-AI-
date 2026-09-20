# ui/insights.py
import os
import datetime
import sqlite3
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

def _load_history_from_db():
    db_path = "haven_storage.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM checkins ORDER BY id ASC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def _evaluate_vitals(latest_row, baseline_map=None):
    sbp = float(latest_row.get("systolic_bp", 120))
    dbp = float(latest_row.get("diastolic_bp", 80))
    hr = float(latest_row.get("heart_rate", 75))
    bs = float(latest_row.get("blood_sugar", 5.8))
    age = float(latest_row.get("age", 28))
    
    current_map = dbp + (sbp - dbp) / 3.0
    delta_map = (current_map - baseline_map) if baseline_map else 0.0
    
    sym_count = int(latest_row.get("symptoms_count", 0))
    if sym_count == 0:
        sym_count = int(latest_row.get("has_headache", 0)) + int(latest_row.get("has_vision", 0)) + int(latest_row.get("has_edema", 0))

    feature_dict = {
        "age": age,
        "systolic_bp": sbp,
        "diastolic_bp": dbp,
        "current_map": current_map,
        "delta_map": delta_map,
        "blood_sugar": bs,
        "heart_rate": hr,
        "delta_weight_7d": float(latest_row.get("delta_weight", 0.0)),
        "symptoms_count": sym_count
    }

    model_loaded = False
    risk_pct = 18.5
    artifact_path = "haven_preeclampsia_model.joblib"

    if os.path.exists(artifact_path):
        try:
            raw_data: object = joblib.load(artifact_path)
            if isinstance(raw_data, dict):
                data_dict: dict = raw_data
                actual_model = data_dict.get("model")
                features = data_dict.get("features", list(feature_dict.keys()))
            else:
                actual_model = raw_data
                features = getattr(actual_model, "feature_names_in_", list(feature_dict.keys()))

            if actual_model is not None and not isinstance(actual_model, dict):
                input_df = pd.DataFrame([{col: feature_dict.get(col, 0.0) for col in features}])
                predict_proba_fn = getattr(actual_model, "predict_proba", None)
                predict_fn = getattr(actual_model, "predict", None)

                if callable(predict_proba_fn):
                    probs = np.asarray(predict_proba_fn(input_df))
                    risk_pct = round(float(probs.item((0, 1))) * 100, 1)
                    model_loaded = True
                elif callable(predict_fn):
                    pred = np.asarray(predict_fn(input_df))
                    risk_pct = 75.0 if int(pred.item(0)) == 1 else 20.0
                    model_loaded = True
        except Exception:
            model_loaded = False

    if not model_loaded:
        risk_score = 15.0
        if sbp >= 140 or dbp >= 90: risk_score += 45.0
        elif sbp >= 130 or dbp >= 85: risk_score += 25.0
        if delta_map >= 6.0: risk_score += 15.0
        if sym_count >= 1: risk_score += 15.0
        risk_pct = min(95.0, risk_score)

    if risk_pct < 35.0:
        tier = "Gentle & Steady"
        bg_tint = "#F2F7F4"
        accent_color = "#749B85"
        msg = "Your vitals are flowing within your personal normal range. Keep resting and nourishing well."
    elif risk_pct < 70.0:
        tier = "Noticed a Slight Shift"
        bg_tint = "#FCF7EE"
        accent_color = "#C79553"
        msg = "Haven noticed mild changes in your pressure readings. Let's do another calm check-in tomorrow."
    else:
        tier = "Worth Sharing with Doctor"
        bg_tint = "#FDF4F2"
        accent_color = "#C77B70"
        msg = "Your body is showing a slight hemodynamic variation. It's a good idea to share these readings with your care provider."

    drivers = [
        {"name": "Systolic Pressure", "reading": f"{int(sbp)} mmHg", "status": "Higher" if sbp >= 130 else "Normal"},
        {"name": "Diastolic Pressure", "reading": f"{int(dbp)} mmHg", "status": "Higher" if dbp >= 85 else "Normal"},
        {"name": "Mean Arterial Drift", "reading": f"{delta_map:+.1f} mmHg", "status": "Shift" if abs(delta_map) >= 5 else "Steady"},
        {"name": "Self-reported Symptoms", "reading": f"{sym_count} reported", "status": "Active" if sym_count > 0 else "None"}
    ]

    return {
        "risk_pct": risk_pct,
        "tier": tier,
        "bg_tint": bg_tint,
        "accent_color": accent_color,
        "message": msg,
        "current_map": round(current_map, 1),
        "drivers": drivers
    }

def render_insights_tab():
    df = _load_history_from_db()

    # --- TOP SOS / SAFETY PILL (WITH CLICKABLE PHONE LINKS) ---
    st.markdown("""
<div style="background:#FFF6F4; border:1px solid #F5DFD9; border-radius:16px; padding:12px 18px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
    <div style="font-size:0.85rem; color:#78524B;">
        🆘 <b>In doubt or sudden discomfort?</b> Don't wait for apps. Call your OB-GYN or maternal helpline:
        <a href="tel:102" style="background:#FBEAE6; color:#C76558; font-weight:700; text-decoration:none; padding:3px 10px; border-radius:8px; margin:0 4px; border:1px solid #F2D2CB; display:inline-block;">📞 102</a>
        or
        <a href="tel:108" style="background:#FBEAE6; color:#C76558; font-weight:700; text-decoration:none; padding:3px 10px; border-radius:8px; margin:0 4px; border:1px solid #F2D2CB; display:inline-block;">📞 108</a>
    </div>
    <span style="font-size:0.72rem; background:#F8E6E2; color:#A64D40; font-weight:700; padding:4px 10px; border-radius:10px; letter-spacing:0.5px;">SAFETY FIRST</span>
</div>
""", unsafe_allow_html=True)

    # Empty State Condition
    if df.empty:
        st.markdown("""
<div style="text-align:center; padding: 36px 18px; background: #FFFFFF; border-radius: 20px; border: 1px dashed #E8DDD5; margin-top: 10px;">
    <span style="font-size: 2.2rem;">🌷</span>
    <h3 style="color:#4A3E3D; margin: 8px 0 4px 0; font-size:1.2rem;">Haven needs a couple of entries</h3>
    <p style="color:#8C7B73; font-size: 0.86rem; max-width: 380px; margin: 0 auto;">
        Log a check-in or two, and your gentle pattern insights will appear here.
    </p>
</div>
""", unsafe_allow_html=True)
    else:
        # Explicitly inside the else block so Pylance knows both variables ALWAYS exist
        latest = df.iloc[-1]
        baseline_map = float(df["current_map"].mean()) if "current_map" in df.columns else None
        eval_res = _evaluate_vitals(latest, baseline_map)

        # --- MINIMALIST VITALS SUMMARY ROW ---
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
<div style="background:#FFFFFF; border:1px solid #EFEAE5; border-radius:16px; padding:14px; text-align:center;">
    <div style="font-size:0.75rem; color:#8C7B73; font-weight:600; text-transform:uppercase;">Recent BP</div>
    <div style="font-size:1.35rem; font-weight:700; color:#4A3E3D; margin:2px 0;">{int(latest["systolic_bp"])}/{int(latest["diastolic_bp"])}</div>
    <div style="font-size:0.72rem; color:#749B85; font-weight:600;">mmHg</div>
</div>
""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
<div style="background:#FFFFFF; border:1px solid #EFEAE5; border-radius:16px; padding:14px; text-align:center;">
    <div style="font-size:0.75rem; color:#8C7B73; font-weight:600; text-transform:uppercase;">Pulse</div>
    <div style="font-size:1.35rem; font-weight:700; color:#4A3E3D; margin:2px 0;">{int(latest.get("heart_rate", 76))}</div>
    <div style="font-size:0.72rem; color:#8C7B73;">bpm</div>
</div>
""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
<div style="background:#FFFFFF; border:1px solid #EFEAE5; border-radius:16px; padding:14px; text-align:center;">
    <div style="font-size:0.75rem; color:#8C7B73; font-weight:600; text-transform:uppercase;">Surveillance</div>
    <div style="font-size:1.05rem; font-weight:700; color:{eval_res['accent_color']}; margin-top:5px;">{eval_res['tier']}</div>
</div>
""", unsafe_allow_html=True)

        st.write("")

        # --- GENTLE RISK CARD ---
        st.markdown(f"""
<div style="background:{eval_res['bg_tint']}; border:1px solid rgba(220, 200, 195, 0.4); border-radius:18px; padding:16px 20px; margin-bottom:20px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <span style="font-size:0.8rem; font-weight:700; color:{eval_res['accent_color']}; letter-spacing:0.5px;">HAVEN'S PATTERN CHECK</span>
        <span style="font-size:0.75rem; font-weight:600; color:#7A6A64;">Early Screening Note</span>
    </div>
    <p style="font-size:0.9rem; color:#4A3E3D; margin:0 0 10px 0; line-height:1.45;">
        {eval_res['message']}
    </p>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
""", unsafe_allow_html=True)

        pills_html = ""
        for d in eval_res["drivers"]:
            pills_html += f'<span style="background:#FFFFFF; border:1px solid #EAE2DA; color:#61504B; font-size:0.75rem; padding:4px 10px; border-radius:12px;"><b>{d["name"]}:</b> {d["reading"]}</span>'
        st.markdown(pills_html + "</div></div>", unsafe_allow_html=True)

        # --- FLO-STYLE SOFT GRAPH ---
        st.markdown("""
<div style="background:#FFFFFF; border:1px solid #EFEAE5; border-radius:20px; padding:18px; margin-bottom:20px;">
    <span style="font-size:0.75rem; color:#8C7B73; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">YOUR BLOOD PRESSURE WAVE</span>
    <p style="font-size:0.82rem; color:#8C7B73; margin:2px 0 12px 0;">Soft curves showing day-to-day rhythm without scary spikes.</p>
""", unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["systolic_bp"],
            name="Upper (Systolic)",
            line=dict(color="#D98A80", width=2.5, shape="spline", smoothing=1.3),
            mode="lines+markers",
            marker=dict(size=6, color="#D98A80")
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["diastolic_bp"],
            name="Lower (Diastolic)",
            line=dict(color="#88A594", width=2.5, shape="spline", smoothing=1.3),
            mode="lines+markers",
            marker=dict(size=6, color="#88A594")
        ))
        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis=dict(showgrid=False, linecolor="#EDE5DE", tickfont=dict(size=10, color="#8C7B73")),
            yaxis=dict(showgrid=True, gridcolor="#F8F4F0", title=dict(text="mmHg", font=dict(size=10, color="#8C7B73")), tickfont=dict(size=10, color="#8C7B73")),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- CLEAN DOCTOR EXPORT CARD ---
        st.markdown("""
<div style="background:#FFFFFF; border:1px solid #EFEAE5; border-radius:18px; padding:18px; margin-bottom:20px;">
    <h4 style="margin:0 0 4px 0; color:#4A3E3D; font-size:0.98rem; font-weight:700;">📋 Doctor-Ready Export</h4>
    <p style="font-size:0.8rem; color:#8C7B73; margin:0 0 12px 0;">Share a concise vitals summary with your OB-GYN.</p>
""", unsafe_allow_html=True)

        summary_text = f"""HAVEN MATERNAL LOG (PRENATAL VISIT SUMMARY)
Date: {datetime.datetime.now().strftime("%B %d, %Y")}
Latest BP: {int(latest['systolic_bp'])}/{int(latest['diastolic_bp'])} mmHg
Mean Arterial Pressure: {eval_res['current_map']} mmHg
Pulse: {int(latest.get('heart_rate', 76))} bpm
Recorded Days: {len(df)}
Status Pattern: {eval_res['tier']}

*Algorithmic surveillance summary for antenatal consultations. Does not replace diagnostic clinical evaluation.*
"""
        st.download_button(
            label="Download Clean Summary (.txt) 📋",
            data=summary_text,
            file_name="haven_vitals_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- COMPANION FOOTNOTE ---
    st.markdown("""
<div style="margin-top: 35px; border-top: 1px dashed #E8DDD5; padding-top: 20px; text-align: center;">
<div style="display: inline-block; background: #FFF7F5; border: 1px solid #F5E3DE; border-radius: 20px; padding: 5px 14px; margin-bottom: 12px;">
<span style="font-size: 0.8rem; color: #7A5C55; font-style: italic;">
🌸 <b>Mama's Note:</b> “You are doing an incredible job growing life today. Rest easy.”
</span>
</div>
<p style="font-size: 0.92rem; color: #4A3E3D; margin: 0 0 4px 0; font-weight: 600;">
Crafted with ☕ iced coffee, 🌷 warm hugs & explainable code by <b>Samruddhi</b>
</p>
<p style="font-size: 0.78rem; color: #8F7D74; margin: 0 0 10px 0; font-style: italic;">
“Because mamas deserve gentle companions, not scary clinical dashboards.” ✨
</p>
<div style="display: flex; justify-content: center; gap: 12px; font-size: 0.7rem; color: #A89B93; flex-wrap: wrap; text-transform: uppercase; letter-spacing: 0.5px;">
<span>🟢 Local & Private Data</span>
<span>•</span>
<span>🩺 Not a Medical Diagnosis</span>
<span>•</span>
<span>🌸 Haven v1.2</span>
</div>
</div>
""", unsafe_allow_html=True)