from flask import Flask, render_template, request
import csv
import math
from pathlib import Path
from collections import Counter

app = Flask(__name__)

# Load student dataset
DATA_FILE = Path(__file__).parent / "student_data.csv"

students = []

with open(DATA_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append({
            "marks": float(row["marks"]),
            "attendance": float(row["attendance"]),
            "study_hours": float(row["study_hours"]),
            "performance": row["performance"]
        })


# K-Nearest Neighbors prediction
def predict_performance(marks, attendance, hours):

    distances = []

    for student in students:
        distance = math.sqrt(
            ((marks - student["marks"]) / 100) ** 2 +
            ((attendance - student["attendance"]) / 100) ** 2 +
            ((hours - student["study_hours"]) / 24) ** 2
        )

        distances.append(
            (distance, student["performance"])
        )

    distances.sort(key=lambda item: item[0])

    nearest = distances[:3]

    votes = Counter(
        performance for distance, performance in nearest
    )

    return votes.most_common(1)[0][0]


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    advice = None
    student_name = ""
    marks = ""
    attendance = ""
    hours = ""

    if request.method == "POST":
        try:
            student_name = request.form["student_name"].strip()
            marks = float(request.form["marks"])
            attendance = float(request.form["attendance"])
            hours = float(request.form["hours"])

            if not student_name:
                raise ValueError("Please enter the student's name.")

            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100.")

            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")

            if not 0 <= hours <= 24:
                raise ValueError("Study hours must be between 0 and 24.")

            prediction = predict_performance(
                marks, attendance, hours
            )

            if prediction == "Good":
                result = "Good Performance"
                advice = "Maintain your study routine and keep practising."

            elif prediction == "Average":
                result = "Average Performance"
                advice = "Review difficult topics and practise regularly."

            else:
                result = "Needs Improvement"
                advice = "Try a study timetable and seek academic guidance."

        except ValueError as error:
            result = "Invalid Input"
            advice = str(error)

    return render_template(
        "index.html",
        result=result,
        advice=advice,
        student_name=student_name,
        marks=marks,
        attendance=attendance,
        hours=hours
    )


if __name__ == "__main__":
    app.run(debug=True)