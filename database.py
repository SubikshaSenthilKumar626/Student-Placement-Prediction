import sqlite3

DATABASE_NAME = "prediction_history.db"


# -----------------------------
# Create Database & Table
# -----------------------------
def create_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        iq REAL,

        prev_sem_result REAL,

        cgpa REAL,

        academic_performance REAL,

        internship_experience TEXT,

        extra_curricular_score REAL,

        communication_skills REAL,

        projects_completed REAL,

        prediction TEXT,

        confidence REAL

    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Save Prediction
# -----------------------------
def save_prediction(
        iq,
        prev_sem_result,
        cgpa,
        academic_performance,
        internship_experience,
        extra_curricular_score,
        communication_skills,
        projects_completed,
        prediction,
        confidence
):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prediction_history(

        iq,
        prev_sem_result,
        cgpa,
        academic_performance,
        internship_experience,
        extra_curricular_score,
        communication_skills,
        projects_completed,
        prediction,
        confidence

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        iq,
        prev_sem_result,
        cgpa,
        academic_performance,
        internship_experience,
        extra_curricular_score,
        communication_skills,
        projects_completed,
        prediction,
        confidence

    ))

    conn.commit()
    conn.close()


# -----------------------------
# Get All Predictions
# -----------------------------
def get_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM prediction_history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows