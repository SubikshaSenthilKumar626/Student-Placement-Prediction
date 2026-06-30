import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------
# Read Dataset
# -----------------------------
data = pd.read_csv("dataset.csv")

# -----------------------------
# Convert Yes/No to 1/0
# -----------------------------
data["Placement"] = data["Placement"].map({"Yes": 1, "No": 0})
data["Internship_Experience"] = data["Internship_Experience"].map({"Yes": 1, "No": 0})

# -----------------------------
# Remove College_ID
# -----------------------------
data = data.drop("College_ID", axis=1)

print("First 5 Rows:\n")
print(data.head())

# -----------------------------
# Input Features and Target
# -----------------------------
X = data.drop("Placement", axis=1)
y = data["Placement"]

print("\nFeatures Used:")
print(X.columns)

# -----------------------------
# Split Dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Random Forest Model
# -----------------------------
model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

# -----------------------------
# Test Accuracy
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "placement_model.pkl")

print("\nModel saved successfully as placement_model.pkl")

# -----------------------------
# Predict New Student
# -----------------------------
new_student = pd.DataFrame([{
    "IQ": 110,
    "Prev_Sem_Result": 8.2,
    "CGPA": 8.0,
    "Academic_Performance": 9,
    "Internship_Experience": 1,
    "Extra_Curricular_Score": 7,
    "Communication_Skills": 9,
    "Projects_Completed": 4
}])

prediction = model.predict(new_student)

probability = model.predict_proba(new_student)

confidence = max(probability[0]) * 100

print("\nPrediction Confidence: {:.2f}%".format(confidence))

if prediction[0] == 1:
    print("🎉 Placement Prediction: YES")
else:
    print("❌ Placement Prediction: NO")

# -----------------------------
# Feature Importance Chart
# -----------------------------
importance = model.feature_importances_
feature_names = X.columns

plt.figure(figsize=(10, 6))
plt.bar(feature_names, importance)

plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig("static/charts/feature_importance.png")

print("\nFeature Importance Chart Saved Successfully!")

plt.close()

# -----------------------------
# Placement Distribution Chart
# -----------------------------
placement_counts = data["Placement"].value_counts()

labels = ["Not Placed", "Placed"]
sizes = [
    placement_counts.get(0, 0),
    placement_counts.get(1, 0)
]

plt.figure(figsize=(6, 6))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Placement Distribution")

plt.savefig("static/charts/placement_distribution.png")

print("Placement Distribution Chart Saved Successfully!")

plt.close()