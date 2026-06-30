from openpyxl import Workbook
from database import get_history


def export_history_to_excel():

    history = get_history()

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Prediction History"

    headers = [
        "ID",
        "IQ",
        "Previous Semester Result",
        "CGPA",
        "Academic Performance",
        "Internship Experience",
        "Extra Curricular Score",
        "Communication Skills",
        "Projects Completed",
        "Prediction",
        "Confidence"
    ]

    sheet.append(headers)

    for row in history:
        sheet.append(row)

    filename = "Prediction_History.xlsx"

    workbook.save(filename)

    return filename