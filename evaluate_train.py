# evaluate_model.py
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

# 1. Model & Features Load karein
bundle = joblib.load("haven_preeclampsia_model.joblib")
model = bundle["model"]
features = bundle["features"]

# 2. Independent Test Cohort Generate karein (Unseen Data)
np.random.seed(99)  # Alag random seed taaki training data se alag ho
n_test = 500

age = np.random.randint(18, 45, n_test)
sbp = np.random.normal(120, 15, n_test).clip(90, 180)
dbp = np.random.normal(80, 10, n_test).clip(60, 120)
bs = np.random.normal(6.5, 1.8, n_test).clip(4.0, 15.0)
hr = np.random.normal(76, 8, n_test).clip(55, 115)
delta_weight = np.random.normal(0.4, 0.6, n_test)
symptoms_count = np.random.choice([0, 1, 2, 3], size=n_test, p=[0.7, 0.2, 0.07, 0.03])

current_map = dbp + (sbp - dbp) / 3.0
delta_map = np.random.normal(0.5, 3.0, n_test)

df_test = pd.DataFrame({
    "age": age,
    "systolic_bp": sbp,
    "diastolic_bp": dbp,
    "current_map": current_map,
    "delta_map": delta_map,
    "blood_sugar": bs,
    "heart_rate": hr,
    "delta_weight_7d": delta_weight,
    "symptoms_count": symptoms_count
})

# Ground Truth Rule
risk_score = (
    (df_test["systolic_bp"] >= 140).astype(int) * 3.0 +
    (df_test["diastolic_bp"] >= 90).astype(int) * 3.0 +
    (df_test["current_map"] >= 102).astype(int) * 2.0 +
    (df_test["symptoms_count"] >= 1).astype(int) * 2.5 +
    (df_test["blood_sugar"] >= 8.0).astype(int) * 1.5
)
y_true = (risk_score >= 3.0).astype(int)

# 3. Model Predictions Run karein
X_test = df_test[features]
y_pred = model.predict(X_test)
y_probs = model.predict_proba(X_test)[:, 1]

# 4. Results Print karein
acc = accuracy_score(y_true, y_pred)
auc = roc_auc_score(y_true, y_probs)
cm = confusion_matrix(y_true, y_pred)

print("\n==========================================")
print("       🌸 HAVEN ML ACCURACY REPORT        ")
print("==========================================")
print(f"Overall Accuracy : {acc * 100:.2f}%")
print(f"ROC-AUC Score    : {auc:.4f}")
print("------------------------------------------")
print("Confusion Matrix:")
print(f"True Negatives  : {cm[0][0]}  |  False Positives : {cm[0][1]}")
print(f"False Negatives : {cm[1][0]}   |  True Positives  : {cm[1][1]}")
print("------------------------------------------")
print("Detailed Classification Breakdown:")
print(classification_report(y_true, y_pred, target_names=["Low Risk", "Preeclampsia Risk"]))
print("==========================================\n")