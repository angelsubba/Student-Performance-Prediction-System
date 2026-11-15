import csv
import joblib
from sklearn.tree import DecisionTreeClassifier

# Load student data from CSV
X = []
y = []

with open("student_data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        X.append([
            float(row["marks"]),
            float(row["attendance"]),
            float(row["study_hours"])
        ])
        y.append(row["performance"])

# Train the machine learning model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, "student_model.joblib")

print("Model trained and saved successfully!")