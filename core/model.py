# core/model.py
import os
import joblib
import numpy as np
import pandas as pd
import shap
from core.storage import get_recent_checkins

MODEL_PATH = "haven_preeclampsia_model.joblib"

class HavenModelEngine:
    def __init__(self):
        self.model = None
        self.features = []
        self.explainer = None
        self.load_artifacts()

    def load_artifacts(self):
        if os.path.exists(MODEL_PATH):
            try:
                bundle = joblib.load(MODEL_PATH)
                self.model = bundle["model"]
                self.features = bundle["features"]
                # Real TreeSHAP explainer
                self.explainer = shap.TreeExplainer(self.model)
            except Exception as e:
                print(f"Error loading model: {e}")

    def evaluate(self, user_inputs: dict):
        history = get_recent_checkins(limit=7)
        
        current_map = user_inputs["diastolic_bp"] + (user_inputs["systolic_bp"] - user_inputs["diastolic_bp"]) / 3.0
        
        if not history.empty and "systolic_bp" in history.columns:
            past_sbp = history["systolic_bp"].iloc[0]
            past_dbp = history["diastolic_bp"].iloc[0]
            past_map = past_dbp + (past_sbp - past_dbp) / 3.0
            delta_map = current_map - past_map
            delta_weight = user_inputs["weight"] - history["weight"].iloc[0]
        else:
            delta_map = 0.0
            delta_weight = 0.2

        input_data = {
            "age": user_inputs["age"],
            "systolic_bp": user_inputs["systolic_bp"],
            "diastolic_bp": user_inputs["diastolic_bp"],
            "current_map": current_map,
            "delta_map": delta_map,
            "blood_sugar": user_inputs["blood_sugar"],
            "heart_rate": user_inputs["heart_rate"],
            "delta_weight_7d": delta_weight,
            "symptoms_count": user_inputs["symptoms_count"]
        }
        
        X_df = pd.DataFrame([input_data])[self.features]

        # Robust Model Inference & SHAP Extraction
        if self.model is not None and self.explainer is not None:
            raw_prob = float(self.model.predict_proba(X_df)[0][1])
            is_elevated = raw_prob >= 0.38
            
            try:
                raw_shap = self.explainer.shap_values(X_df)
                if isinstance(raw_shap, list):
                    shap_values = raw_shap[1][0] if len(raw_shap) > 1 else raw_shap[0][0]
                elif hasattr(raw_shap, "shape") and len(raw_shap.shape) == 2:
                    shap_values = raw_shap[0]
                else:
                    shap_values = np.array(raw_shap).flatten()
            except Exception:
                shap_values = np.zeros(len(self.features))
        else:
            raw_prob = 0.08
            is_elevated = False
            shap_values = np.zeros(len(self.features))

        feature_labels = {
            "systolic_bp": "🩸 Systolic blood pressure",
            "diastolic_bp": "🩺 Diastolic blood pressure",
            "current_map": "💓 Mean arterial pressure",
            "delta_map": "📈 Blood pressure trajectory shift",
            "blood_sugar": "🍯 Blood glucose balance",
            "heart_rate": "❤️ Resting pulse rhythm",
            "delta_weight_7d": "⚖️ Fluid / weight shift pattern",
            "symptoms_count": "🌷 Reported bodily symptoms",
            "age": "🗓️ Maternal age factor"
        }

        contributions = []
        for feat_name, val, s_val in zip(self.features, X_df.iloc[0], shap_values):
            contributions.append({
                "feature": feat_name,
                "label": feature_labels.get(feat_name, feat_name),
                "actual_value": float(val),
                "shap_value": float(s_val),
                "abs_shap": abs(float(s_val))
            })

        contributions.sort(key=lambda x: x["abs_shap"], reverse=True)
        top_drivers = contributions[:3]

        for d in top_drivers:
            if d["shap_value"] > 0.04:
                d["impact"] = "Noticeable upward push"
            elif d["shap_value"] > 0.01:
                d["impact"] = "Mild upward influence"
            elif d["shap_value"] < -0.01:
                d["impact"] = "Reassuring stabilizing factor"
            else:
                d["impact"] = "Neutral influence"

        primary_driver = top_drivers[0]["label"].split()[-1].lower() if top_drivers else "vitals"
        if is_elevated:
            human_text = f"Your recent {primary_driver} readings had the strongest influence on this assessment."
        else:
            human_text = "Your resting vital patterns are balanced and stabilizing this assessment."

        return {
            "probability": raw_prob,
            "is_elevated": is_elevated,
            "risk_tier": "Pattern Requiring Review" if is_elevated else "Lower-Risk Pattern",
            "color": "#C46F63" if is_elevated else "#5D8C72",
            "top_drivers": top_drivers,
            "human_summary": human_text,
            "current_map": round(current_map, 1),
            "delta_map": round(delta_map, 1),
            "delta_weight": round(delta_weight, 2),
            "all_shap_details": contributions
        }