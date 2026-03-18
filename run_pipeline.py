import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb

# =========================
# LOAD DATA
# =========================
train_path = "data/Sample_arvyax_reflective_dataset.xlsx"
test_path = "data/arvyax_test_inputs_120.xlsx"

train = pd.read_excel(train_path)
test = pd.read_excel(test_path)

print("Train shape:", train.shape)
print("Test shape:", test.shape)

# =========================
# PREPROCESSING
# =========================
def preprocess(df):
    df = df.copy()

    # Text cleaning
    df["journal_text"] = df["journal_text"].fillna("").astype(str)

    # Numeric features
    num_cols = ["sleep_hours", "energy_level", "stress_level", "duration_min"]

    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Categorical fallback
    if "time_of_day" in df.columns:
        df["time_of_day"] = df["time_of_day"].fillna("morning")

    return df

train = preprocess(train)
test = preprocess(test)

# =========================
# TEXT FEATURES
# =========================
vectorizer = TfidfVectorizer(max_features=150)

X_text_train = vectorizer.fit_transform(train["journal_text"]).toarray()
X_text_test = vectorizer.transform(test["journal_text"]).toarray()

# =========================
# METADATA FEATURES
# =========================
meta_cols = ["sleep_hours", "energy_level", "stress_level", "duration_min"]

X_meta_train = train[meta_cols].values
X_meta_test = test[meta_cols].values

# Combine
X_train = np.hstack([X_text_train, X_meta_train])
X_test = np.hstack([X_text_test, X_meta_test])

# =========================
# LABELS
# =========================
le = LabelEncoder()
y_train = le.fit_transform(train["emotional_state"])

# =========================
# MODEL (Ensemble)
# =========================
clf_rf = RandomForestClassifier(n_estimators=200, random_state=42)
clf_xgb = xgb.XGBClassifier(n_estimators=200, eval_metric="mlogloss")

clf_rf.fit(X_train, y_train)
clf_xgb.fit(X_train, y_train)

# =========================
# PREDICTIONS
# =========================
probs_rf = clf_rf.predict_proba(X_test)
probs_xgb = clf_xgb.predict_proba(X_test)

probs = (probs_rf + probs_xgb) / 2

pred_idx = np.argmax(probs, axis=1)
pred_labels = le.inverse_transform(pred_idx)

# =========================
# INTENSITY (Regression)
# =========================
reg = xgb.XGBRegressor(n_estimators=200)
reg.fit(X_train, train["intensity"])

intensity_preds = reg.predict(X_test)
intensity_preds = np.clip(intensity_preds, 1, 5)

# =========================
# UNCERTAINTY
# =========================
confidence = np.max(probs, axis=1)

entropy = -np.sum(probs * np.log(probs + 1e-9), axis=1)
uncertain_flag = (entropy > 1.0).astype(int)

# =========================
# DECISION ENGINE
# =========================
def decide(state, intensity, stress, energy, time_of_day):

    # Normalize missing
    stress = stress if not np.isnan(stress) else 3
    energy = energy if not np.isnan(energy) else 3

    # HIGH STRESS → calm immediately
    if stress >= 4:
        return "box_breathing", "now"

    # LOW ENERGY
    if energy <= 2:
        if time_of_day in ["night", "evening"]:
            return "rest", "tonight"
        return "movement", "within_15_min"

    # HIGH ENERGY + LOW STRESS
    if energy >= 4 and stress <= 2:
        return "deep_work", "now"

    # HIGH INTENSITY emotion
    if intensity >= 4:
        return "journaling", "within_15_min"

    # DEFAULT
    return "light_planning", "later_today"

# =========================
# BUILD OUTPUT
# =========================
results = []

for i, row in test.iterrows():

    action, timing = decide(
        pred_labels[i],
        intensity_preds[i],
        row.get("stress_level", 3),
        row.get("energy_level", 3),
        row.get("time_of_day", "morning")
    )

    results.append({
        "id": row["id"],
        "predicted_state": pred_labels[i],
        "predicted_intensity": round(float(intensity_preds[i]), 2),
        "confidence": round(float(confidence[i]), 3),
        "uncertain_flag": int(uncertain_flag[i]),
        "what_to_do": action,
        "when_to_do": timing
    })

df_out = pd.DataFrame(results)

print("Final output rows:", len(df_out))

# =========================
# SAVE OUTPUT
# =========================
output_path = "outputs/predictions.csv"
df_out.to_csv(output_path, index=False)

print("✅ predictions.csv created successfully!")