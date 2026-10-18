import argparse
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="Set your real group and Student ID before committing.")
parser.add_argument("--group", required=True)
parser.add_argument("--student-id", required=True)
args = parser.parse_args()
for label, value in [("group", args.group), ("student-id", args.student_id)]:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value) or value.upper() in {"CHANGE_ME", "YOUR_ID", "REAL_ID"}:
        parser.error(f"Enter a real {label} using letters, digits, hyphens or underscores.")
student = json.loads((root / "config/student.json").read_text())
student.update(group=args.group, student_id=args.student_id)
(root / "config/student.json").write_text(json.dumps(student, indent=2) + "\n")
labels = {"name": "Name", "surname": "Surname", "group": "Group",
          "student_id": "Student ID", "course": "Course"}
(root / "Sembi_Amir_info.txt").write_text("".join(f"{label}: {student[key]}\n" for key, label in labels.items()))
mapping = {"STUDENT_NAME": "name", "STUDENT_SURNAME": "surname",
           "STUDENT_GROUP": "group", "STUDENT_ID": "student_id"}
env_text = "".join(f"{variable}={student[key]}\n" for variable, key in mapping.items())
(root / ".env").write_text(env_text)
(root / ".env").chmod(0o600)
(root / ".env.example").write_text("".join(f"{variable}={'CHANGE_ME' if key == 'student_id' else student[key]}\n" for variable, key in mapping.items()))
pipeline = (root / "Jenkinsfile").read_text()
for variable, key in mapping.items():
    pipeline = re.sub(rf"(        {variable} = )'[^']*'", rf"\g<1>'{student[key]}'", pipeline)
(root / "Jenkinsfile").write_text(pipeline)
print("Updated student.json, info.txt, .env, .env.example and Jenkinsfile.")
print("Now run: python3 scripts/validate_personalization.py")
