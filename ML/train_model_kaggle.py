import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# Load dataset
df = pd.read_csv("dataset.csv")

# Display first 5 rows
print(df.head())

# Dataset information
print("\nDataset Info:")
print(df.info())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Store label encoders
label_encoders = {}

# Encode all categorical columns
for column in df.columns:

    if df[column].dtype == "object":

        le = LabelEncoder()

        df[column] = le.fit_transform(df[column])

        label_encoders[column] = le

print("\nEncoded Dataset:")
print(df.head())

# Save encoders
joblib.dump(label_encoders, "label_encoders.pkl")

print("\nLabel Encoders Saved Successfully!")

# Target Column
X = df.drop("Class", axis=1)

y = df["Class"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)

# Random Forest Model
model = RandomForestClassifier(

    n_estimators=100,
    random_state=42

)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save Model
joblib.dump(model, "model.pkl")

print("\nModel Saved Successfully!")

print("\nFeatures Used For Training:")
print(X.columns.tolist())
print(df.columns.tolist())