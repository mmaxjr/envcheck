import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from envcheck import validate


class ValidateTests(unittest.TestCase):
    def test_accepts_present_variable_and_file(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "app.env"
            config.touch()
            with patch.dict(os.environ, {"API_KEY": "secret"}):
                self.assertEqual(validate(["API_KEY"], [config]), [])

    def test_reports_missing_variable_and_file(self):
        with patch.dict(os.environ, {}, clear=True):
            errors = validate(["API_KEY"], [Path("missing.env")])
        self.assertEqual(len(errors), 2)
        self.assertIn("API_KEY", errors[0])
        self.assertIn("missing.env", errors[1])

    def test_profile_adds_required_variables(self):
        with patch.dict(os.environ, {}, clear=True):
            errors = validate([], [], "production")
        self.assertEqual(errors, [
            "Missing environment variable: DATABASE_URL",
            "Missing environment variable: SECRET_KEY",
        ])

    def test_profile_and_manual_requirements_can_pass(self):
        with patch.dict(os.environ, {"CI": "true", "API_KEY": "secret"}, clear=True):
            self.assertEqual(validate(["API_KEY"], [], "ci"), [])


if __name__ == "__main__":
    unittest.main()
