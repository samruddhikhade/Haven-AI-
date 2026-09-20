# train.py
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix
from xgboost import XGBClassifier

np.random.seed(42)
n_samples = 2200

# 1. Realistic feature distributions
age = np.random.randint(18, 45, n_samples)
sbp = np.random.normal(118, 14, n_samples).clip(85, 175)
dbp = np.random.normal(76, 10, n_samples).clip(55, 115)
bs = np.random.normal(5.4, 1.4, n_samples).clip(3.5, 14.0)
hr = np.random.normal(76, 8, n_samples).clip(55, 115)
delta_weight = np.random.normal(0.4, 0.5, n_samples).clip(-1.0, 3.5)
symptoms_count = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.72, 0.20, 0.06, 0.02])

# 2. Engineered trajectory features
current_map = dbp + (sbp - dbp) / 3.0
delta_map = np.random.normal(0.5, 3.0, n_samples).clip(-10, 25)

df = pd.DataFrame({
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

# 3. Continuous risk score with realistic clinical variance
base_score = (
    ((df["systolic_bp"] - 120) / 14.0) * 1.2 +
    ((df["diastolic_bp"] - 80) / 9.0) * 1.1 +
    ((df["current_map"] - 93) / 10.0) * 0.9 +
    (df["delta_map"] / 4.5) * 0.8 +
    (df["delta_weight_7d"] / 1.4) * 0.6 +
    (df["symptoms_count"] * 1.1) +
    ((df["blood_sugar"] - 5.5) / 2.2) * 0.4
)

# Patient-level biological noise (borderline cases add karne ke liye)
noise = np.random.normal(0, 0.65, n_samples)
final_score = base_score + noise

# Probability conversion & balanced threshold (~14% positive incidence)
prob = 1 / (1 + np.exp(-final_score))
df["target"] = (prob >= 0.52).astype(int)

features = [
    "age", "systolic_bp", "diastolic_bp", "current_map",
    "delta_map", "blood_sugar", "heart_rate", "delta_weight_7d", "symptoms_count"
]

X = df[features]
y = df["target"]

# 4. Train-Test Split (80% Train, 20% Unseen Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5. Regularized XGBoost (overfitting rokne ke liye)
model = XGBClassifier(
    n_estimators=90,
    max_depth=3,            # Shallow depth se exact memorization rukti hai
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    eval_metric="logloss",
    random_state=42
)
model.fit(X_train, y_train)

# 6. Evaluation
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print("\n==========================================")
print("       🌸 HAVEN MODEL TRAINING RESULTS     ")
print("==========================================")
print(f"Overall Accuracy : {acc * 100:.2f}%")
print(f"ROC-AUC Score    : {auc:.4f}")
print("------------------------------------------")
print("Confusion Matrix:")
print(f"True Negatives  : {cm[0][0]}  |  False Positives : {cm[0][1]}")
print(f"False Negatives : {cm[1][0]}   |  True Positives  : {cm[1][1]}")
print("------------------------------------------")
print(classification_report(y_test, y_pred, target_names=["Low Risk", "Elevated Risk"]))
print("==========================================\n")

joblib.dump({"model": model, "features": features}, "haven_preeclampsia_model.joblib")
print("✅ Saved to haven_preeclampsia_model.joblib successfully!\n")