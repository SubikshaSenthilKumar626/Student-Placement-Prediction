import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_recommendation(student_data, prediction, confidence):

    prompt = f"""
You are an expert AI Career Advisor and Placement Mentor.

Analyze the student's profile carefully and generate a professional AI Placement Assessment Report.

Student Details

IQ: {student_data['IQ']}
Previous Semester Result: {student_data['Previous Semester Result']}
CGPA: {student_data['CGPA']}
Academic Performance: {student_data['Academic Performance']}/10
Internship Experience: {student_data['Internship Experience']}
Extra Curricular Score: {student_data['Extra Curricular Score']}/10
Communication Skills: {student_data['Communication Skills']}/10
Projects Completed: {student_data['Projects Completed']}

Machine Learning Prediction:
{prediction}

Prediction Confidence:
{confidence}%

Generate the report EXACTLY in the following format.

🤖 AI Placement Assessment

------------------------------

🎯 Placement Status

Mention whether the student is likely to be placed or has a lower chance of placement.

------------------------------

📈 Placement Confidence

Mention the confidence percentage.

------------------------------

💼 Student Profile Analysis

Evaluate

• Academic Performance

• Technical Readiness

• Communication Skills

• Internship Experience

Keep each point within one sentence.

------------------------------

💪 Key Strengths

Mention exactly FOUR strengths based ONLY on the student's profile.

------------------------------

📌 Improvement Areas

Mention exactly FOUR realistic improvements.

------------------------------

🛣 Recommended Career Roadmap

Month 1

✔ Recommendation

Month 2

✔ Recommendation

Month 3

✔ Recommendation

------------------------------

🎓 Recommended Skills to Learn

Suggest FIVE relevant technical or soft skills.

------------------------------

🌟 AI Career Insight

Write a motivational conclusion in 3-4 lines.

Rules

1. Never use Markdown like ** or ##.

2. Never use tables.

3. Use emojis exactly as given.

4. Keep the report under 350 words.

5. Make it look like a professional AI-generated placement report.

6. Recommendations should match the student's profile.

7. Do not repeat the same point.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Unable to generate AI recommendation.\n\nError: {str(e)}"