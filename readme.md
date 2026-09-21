# 🌸 Haven — Maternal Health & Preeclampsia Risk Companion

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://haven-ai-04.streamlit.app)
![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-EB8921?style=flat)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-0.970-success?style=flat)
![Accuracy](https://img.shields.io/badge/Accuracy-92.73%25-brightgreen?style=flat)

> **Haven** bridges daily maternal wellness tracking with clinical predictive intelligence. It pairs real-time, explainable pre-eclampsia risk detection powered by machine learning with gentle, low-stress pregnancy companionship.

 🔗 **Live Demo:** [Haven Web App](https://haven-ai-04.streamlit.app)

---

## 💡 The Problem & The Solution

Clinical prenatal monitoring tools are often sterile, cold, and anxiety-inducing, while most lifestyle pregnancy apps ignore critical maternal warning signs. 

**Haven** unites both worlds:
1. **Clinical Rigor:** Monitors dynamic biomarkers—Mean Arterial Pressure (MAP), weight velocity ($\Delta\text{Weight}$), and high-risk symptom patterns—to catch hypertensive complications early.
2. **Empathetic Companionship:** Offers a guilt-free craving sanctuary, guided 4-7-8 breathing pauses, ambient audio soundscapes, and gentle hydration tracking without cognitive overload.

---

## 🩺 Machine Learning Benchmark

At the heart of Haven's risk detection pipeline is an **XGBoost Classifier**, tuned to balance high sensitivity for early detection with clinical calibration.

| Metric | Score | Clinical Relevance |
| :--- | :--- | :--- |
| **ROC-AUC** | **0.970** | Strong discriminative ability between baseline and elevated risk profiles |
| **Accuracy** | **92.73%** | Multi-biomarker calibration across clinical features |
| **Primary Predictors** | 9 Biomarkers | SBP, DBP, MAP, $\Delta\text{MAP}$, Blood Glucose, Heart Rate, $\Delta\text{Weight}$, Headache, Visual Disturbances |

---

## ✨ Key Features

- **🩺 Smart Risk Check-in:** Instant, non-stigmatizing risk assessment computing Mean Arterial Pressure ($MAP = \frac{SBP + 2 \times DBP}{3}$) and multi-symptom telemetry.
- **🍓 Craving Corner:** A comforting companion space that pairs cravings with available Indian pantry staples across 3 effort tiers (Quick, Takes a Little Love, Exotic Twist).
- **🌿 Sanctuary:** Sensory regulation zone with an interactive visual breathing circle (4-7-8 technique) and high-quality ambient rain audio.
- **📖 Journey Timeline:** Longitudinal health diary recording vitals, mood logs, and entries synced to local time.
- **💧 Hydration Ring:** Gentle, tap-friendly daily water tracker that stays synchronized across tabs.

---

## 🛠️ Architecture & Tech Stack
Haven/
├── app.py                            # Multi-tab router & shared navigation
├── train.py                          # ML training & validation pipeline
├── haven_preeclampsia_model.joblib   # Serialized XGBoost artifact
├── haven_storage.db                  # SQLite database for vitals & logs
├── core/
│   ├── craving_engine.py             # Combinatorial Indian pantry recipe logic
│   └── storage.py                    # Database CRUD & session persistence
└── ui/
├── home.py                       # Daily summary & vital overview
├── checkin.py                    # Clinical telemetry & inference UI
├── cravings.py                   # Craving Corner interface
├── journey.py                    # Longitudinal timeline logs
└── sanctuary.py                  # Breathing coach & audio soundscapes

* **Frontend:** Streamlit, Custom CSS (Pastel / Low-Cognitive-Load Design)
* **Machine Learning:** XGBoost, Scikit-learn, Joblib
* **Data Handling:** Pandas, NumPy
* **Storage:** SQLite3, JSON persistence

---

## 🚀 Local Installation & Setup

To run Haven on your local machine:

```bash
# 1. Clone this repository
git clone [https://github.com/samruddhikhade/Haven-AI-.git](https://github.com/samruddhikhade/Haven-AI-.git)
cd Haven-AI-

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Launch the application
streamlit run app.py

⚠️ Clinical Disclaimer
Haven is an educational and supportive wellness tool. It does not provide medical diagnoses, clinical treatment plans, or replace direct prenatal care from an obstetrician or certified healthcare provider.
