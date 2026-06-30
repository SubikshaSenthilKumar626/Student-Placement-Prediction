from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib

from pdf_generator import generate_pdf
from database import create_database, save_prediction, get_history
from excel_generator import export_history_to_excel
from gemini_ai import generate_recommendation

app = Flask(__name__)

# Load ML model
model = joblib.load("placement_model.pkl")

# Create database if it doesn't exist
create_database()

# Store latest report information
latest_report = {}

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Predict Placement
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    new_student = pd.DataFrame([{
        "IQ": float(request.form["IQ"]),
        "Prev_Sem_Result": float(request.form["Prev_Sem_Result"]),
        "CGPA": float(request.form["CGPA"]),
        "Academic_Performance": float(request.form["Academic_Performance"]),
        "Internship_Experience": int(request.form["Internship_Experience"]),
        "Extra_Curricular_Score": float(request.form["Extra_Curricular_Score"]),
        "Communication_Skills": float(request.form["Communication_Skills"]),
        "Projects_Completed": float(request.form["Projects_Completed"])
    }])

    prediction = model.predict(new_student)
    probability = model.predict_proba(new_student)

    confidence = round(max(probability[0]) * 100, 2)

    if prediction[0] == 1:

        result = "🎉 Likely To Be Placed"

    else:

        result = "❌ Less Chance Of Placement"

    student_details = {
        "IQ": new_student.iloc[0]["IQ"],
        "Previous Semester Result": new_student.iloc[0]["Prev_Sem_Result"],
        "CGPA": new_student.iloc[0]["CGPA"],
        "Academic Performance": new_student.iloc[0]["Academic_Performance"],
        "Internship Experience": "Yes" if new_student.iloc[0]["Internship_Experience"] == 1 else "No",
        "Extra Curricular Score": new_student.iloc[0]["Extra_Curricular_Score"],
        "Communication Skills": new_student.iloc[0]["Communication_Skills"],
        "Projects Completed": new_student.iloc[0]["Projects_Completed"]
    }

    ai_recommendation = generate_recommendation(
        student_details,
        result,
        confidence
    )

    global latest_report

    latest_report = {
        "student": student_details,
        "prediction": result,
        "confidence": confidence,
        "recommendation": ai_recommendation
    }

    save_prediction(
        student_details["IQ"],
        student_details["Previous Semester Result"],
        student_details["CGPA"],
        student_details["Academic Performance"],
        student_details["Internship Experience"],
        student_details["Extra Curricular Score"],
        student_details["Communication Skills"],
        student_details["Projects Completed"],
        result,
        confidence
    )

    return render_template(
        "result.html",
        prediction=result,
        confidence=confidence,
        ai_recommendation=ai_recommendation
    )
# -----------------------------
# Download PDF
# -----------------------------
@app.route("/download")
def download():

    filename = generate_pdf(
        latest_report["student"],
        latest_report["prediction"],
        latest_report["confidence"],
        latest_report["recommendation"]
    )

    return send_file(filename, as_attachment=True)


# -----------------------------
# Prediction History
# -----------------------------
@app.route("/history")
def history():

    history_data = get_history()

    return render_template(
        "history.html",
        history=history_data
    )


# -----------------------------
# Export Excel
# -----------------------------
@app.route("/export")
def export():

    filename = export_history_to_excel()

    return send_file(
        filename,
        as_attachment=True
    )


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    data = pd.read_csv("dataset.csv")

    total_students = len(data)
    placed_students = len(data[data["Placement"] == "Yes"])
    not_placed_students = len(data[data["Placement"] == "No"])

    placement_rate = round(
        (placed_students / total_students) * 100,
        2
    )

    # Read prediction history from SQLite
    history = get_history()

    total_predictions = len(history)

    if total_predictions > 0:

        average_iq = round(
            sum(row[1] for row in history) / total_predictions,
            2
        )

        average_cgpa = round(
            sum(row[3] for row in history) / total_predictions,
            2
        )

        average_confidence = round(
            sum(row[10] for row in history) / total_predictions,
            2
        )

        internship_yes = len(
            [row for row in history if row[5] == "Yes"]
        )

        internship_percentage = round(
            (internship_yes / total_predictions) * 100,
            2
        )

    else:

        average_iq = 0
        average_cgpa = 0
        average_confidence = 0
        internship_percentage = 0

    accuracy = round(average_confidence, 2)

    return render_template(
        "dashboard.html",
        total_students=total_students,
        placed_students=placed_students,
        not_placed_students=not_placed_students,
        placement_rate=placement_rate,
        accuracy=accuracy,
        total_predictions=total_predictions,
        average_iq=average_iq,
        average_cgpa=average_cgpa,
        internship_percentage=internship_percentage,
        average_confidence=average_confidence
    )

# -----------------------------
# About Project
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# Developer
# -----------------------------
@app.route("/developer")
def developer():
    return render_template("developer.html")


# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)