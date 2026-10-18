import json
import os
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

from app.main import ROOT, StudentHandler, get_config, get_student, render_page


class StudentTests(unittest.TestCase):
    def test_file_defaults(self):
        expected = json.loads((ROOT / "config/student.json").read_text())
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_student(), expected)

    def test_environment_overrides_all_fields(self):
        variables = {"STUDENT_NAME": "Dana", "STUDENT_SURNAME": "Test",
                     "STUDENT_GROUP": "TEST-1", "STUDENT_ID": "987654"}
        with patch.dict(os.environ, variables, clear=True):
            student = get_student()
        self.assertEqual([student[k] for k in ["name", "surname", "group", "student_id"]],
                         ["Dana", "Test", "TEST-1", "987654"])

    def test_partial_override_keeps_other_fields(self):
        expected = json.loads((ROOT / "config/student.json").read_text())
        with patch.dict(os.environ, {"STUDENT_GROUP": "NEW-GROUP"}, clear=True):
            student = get_student()
        expected["group"] = "NEW-GROUP"
        self.assertEqual(student, expected)

    def test_html_escapes_student_data(self):
        student = get_student()
        student["name"] = '<script>alert("x")</script>'
        page = render_page(student)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_configuration_port(self):
        self.assertEqual(int(get_config()["port"]), 8080)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), StudentHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_endpoint(self):
        with urlopen(self.base + "/health", timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.load(response), {"status": "ok"})

    def test_student_json_endpoint(self):
        with patch.dict(os.environ, {"STUDENT_ID": "HTTP-CHECK"}):
            with urlopen(self.base + "/api/student", timeout=3) as response:
                self.assertIn("application/json", response.headers["Content-Type"])
                self.assertEqual(json.load(response)["student_id"], "HTTP-CHECK")

    def test_homepage_contains_personal_information(self):
        with urlopen(self.base + "/", timeout=3) as response:
            page = response.read().decode()
            self.assertIn("Student ID", page)
            self.assertIn("Application is running successfully!", page)

    def test_unknown_path_returns_404(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base + "/missing", timeout=3)
        self.assertEqual(error.exception.code, 404)
        error.exception.close()

    def test_health_with_query_string(self):
        with urlopen(self.base + "/health?check=1", timeout=3) as response:
            self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
