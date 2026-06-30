import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_recommendation(student_data, prediction, confidence):

    prompt = f"""
You are an experienced career counselor.

A student has the following profile:

IQ: {student_data['IQ']}
Previous Semester Result: {student_data['Previous Semester Result']}
CGPA: {student_data['CGPA']}
Academic Performance: {student_data['Academic Performance']}
Internship Experience: {student_data['Internship Experience']}
Extra Curricular Score: {student_data['Extra Curricular Score']}
Communication Skills: {student_data['Communication Skills']}
Projects Completed: {student_data['Projects Completed']}

Placement Prediction:
{prediction}

Confidence:
{confidence}%

Give:

1. A short career analysis.
2. 5 personalized recommendations.
3. Skills to improve.
4. Interview preparation tips.

Keep the response under 250 words.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Unable to generate AI recommendation.\n\nError: {str(e)}"