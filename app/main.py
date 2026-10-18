import configparser
import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "name": "STUDENT_NAME",
    "surname": "STUDENT_SURNAME",
    "group": "STUDENT_GROUP",
    "student_id": "STUDENT_ID",
}


def get_student():
    student = json.loads((ROOT / "config/student.json").read_text())
    for key, variable in FIELDS.items():
        student[key] = os.environ.get(variable, student[key])
    return student


def get_config():
    config = configparser.ConfigParser()
    config.read(ROOT / "config/app.conf")
    return config["app"]


def render_page(student):
    config = get_config()
    labels = {"name": "Name", "surname": "Surname", "group": "Group",
              "student_id": "Student ID", "course": "Course"}
    rows = "".join(
        f"<dt>{label}</dt><dd>{html.escape(str(student[key]))}</dd>"
        for key, label in labels.items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(config['name'])}</title>
<style>
body{{margin:0;background:#f2f5f9;color:#152337;font:18px system-ui,sans-serif}}
main{{max-width:720px;margin:9vh auto;padding:32px}}
small{{color:#466181;letter-spacing:.12em}}h1{{font-size:42px;line-height:1.15}}
article{{background:white;padding:28px;border-radius:16px;border:1px solid #dce4ed}}
dl{{display:grid;grid-template-columns:130px 1fr;gap:18px;margin:0}}
dt{{color:#526377}}dd{{margin:0;font-weight:600;overflow-wrap:anywhere}}
.status{{color:#14613d;margin-top:28px}}a{{color:#265bac}}
footer{{margin-top:25px;color:#526377;font-size:15px}}
@media(max-width:480px){{main{{padding:18px}}h1{{font-size:32px}}}}
</style></head><body><main><small>DEVOPS LABORATORY 1</small>
<h1>{html.escape(config['name'])}</h1><article><dl>{rows}</dl></article>
<p class="status">{html.escape(config['message'])}</p>
<p><a href="/api/student">Student JSON</a> · <a href="/health">Health check</a></p>
<footer>Linux → Git → GitHub → Jenkins → Docker</footer>
</main></body></html>"""


class StudentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/":
            self.respond(200, render_page(get_student()), "text/html; charset=utf-8")
        elif path == "/api/student":
            self.respond(200, json.dumps(get_student()), "application/json")
        elif path == "/health":
            self.respond(200, json.dumps({"status": "ok"}), "application/json")
        else:
            self.respond(404, json.dumps({"error": "Not found"}), "application/json")

    def respond(self, status, content, content_type):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    student = get_student()
    print("=" * 32)
    print("DevOps Student Application")
    print("=" * 32)
    for key, label in [("name", "Name"), ("surname", "Surname"),
                       ("group", "Group"), ("student_id", "Student ID")]:
        print(f"{label}: {student[key]}")
    print(get_config()["message"], flush=True)
    port = int(os.environ.get("PORT", get_config()["port"]))
    server = ThreadingHTTPServer(("0.0.0.0", port), StudentHandler)
    print(f"Listening on port {port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
