import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------------------------
# Load LMS Dataset
# -------------------------

df = pd.read_csv("lms_dataset.csv")

print(df.head())

# -------------------------
# Encode Target Column
# -------------------------

le = LabelEncoder()

df["Class"] = le.fit_transform(df["Class"])

joblib.dump(le, "label_encoder.pkl")

# -------------------------
# Features & Target
# -------------------------

X = df[[
    "visited_resources",
    "announcements_view",
    "discussion_count",
    "raised_hands",
    "login_count"
]]

y = df["Class"]

# -------------------------
# Train Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)

# -------------------------
# Random Forest
# -------------------------

model = RandomForestClassifier(

    n_estimators=100,
    random_state=42

)

model.fit(X_train, y_train)

# -------------------------
# Accuracy
# -------------------------

prediction = model.predict(X_test)

print("Accuracy :", accuracy_score(y_test, prediction))

# -------------------------
# Save Model
# -------------------------

joblib.dump(model, "model.pkl")

print("Model Saved Successfully")