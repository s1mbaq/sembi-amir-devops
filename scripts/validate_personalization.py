import json
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
student = json.loads((root / "config/student.json").read_text())
for key in ["name", "surname", "group", "student_id"]:
    value = student.get(key, "")
    if not value or value.upper() in {"CHANGE_ME", "YOUR_ID", "REAL_ID"}:
        raise SystemExit("Personalization is incomplete. Run scripts/personalize.py with your real data.")
pipeline = (root / "Jenkinsfile").read_text()
info = (root / "Sembi_Amir_info.txt").read_text()
for variable, key, label in [("STUDENT_NAME", "name", "Name"),
                             ("STUDENT_SURNAME", "surname", "Surname"),
                             ("STUDENT_GROUP", "group", "Group"),
                             ("STUDENT_ID", "student_id", "Student ID")]:
    value = student[key]
    if f"{variable} = '{value}'" not in pipeline or f"{label}: {value}\n" not in info:
        raise SystemExit(f"Inconsistent {key}. Run scripts/personalize.py again.")
    if variable in os.environ and os.environ[variable] != value:
        raise SystemExit(f"{variable} differs from committed student data.")
print("Personalization is complete and consistent.")
