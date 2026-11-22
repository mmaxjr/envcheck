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


if __name__ == "__main__":
    unittest.main()
