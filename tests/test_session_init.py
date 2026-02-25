import unittest
from unittest.mock import patch, MagicMock
import sys
import json
import io
import os

# Add the directory containing the module to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../.cursor/hooks')))

# Import the module to test
import session_init

class TestSessionInit(unittest.TestCase):
    def setUp(self):
        # Redirect stdout and stderr to capture output
        self.held_stdout = io.StringIO()
        self.held_stderr = io.StringIO()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def test_valid_json(self):
        # Simulate valid JSON input
        # Mocking json.load because reading from sys.stdin directly in test might be tricky if not patched correctly
        # But actually let's try to just patch sys.stdin and let json.load read from it.
        # However, json.load(sys.stdin) reads from the file object.
        with patch('sys.stdin', io.StringIO('{"test": "data"}')):
             # We need to make sure we don't accidentally catch the SystemExit inside assertRaises if we want to check output
             # But main() calls sys.exit(0), so we expect SystemExit
            with self.assertRaises(SystemExit) as cm:
                session_init.main()
            self.assertEqual(cm.exception.code, 0)

            # Check output
            output_str = self.held_stdout.getvalue()
            # The output should be valid JSON
            try:
                output = json.loads(output_str)
            except json.JSONDecodeError:
                self.fail(f"Output is not valid JSON: {output_str}")

            self.assertTrue(output.get("continue"))
            # "CONDUCTOR_ACTIVE" depends on env var or directory existence.
            # In test environment, conductor dir probably doesn't exist, so CONDUCTOR_ACTIVE should be "false"
            # unless we mock os.path.exists or create the dir.
            # But the key point is it runs.

    def test_invalid_json(self):
        # Simulate invalid JSON input - this should raise JSONDecodeError inside json.load
        # which should be CAUGHT by the script.
        with patch('sys.stdin', io.StringIO('{invalid json}')):
            with self.assertRaises(SystemExit) as cm:
                session_init.main()
            self.assertEqual(cm.exception.code, 0)

            output_str = self.held_stdout.getvalue()
            try:
                output = json.loads(output_str)
            except json.JSONDecodeError:
                self.fail(f"Output is not valid JSON: {output_str}")

            self.assertTrue(output.get("continue"))
            self.assertIn("Failed to parse input", self.held_stderr.getvalue())

    def test_unexpected_exception_not_caught(self):
        # Simulate an unexpected exception during json.load
        # This should NOT be caught, so it should propagate as RuntimeError.
        with patch('json.load', side_effect=RuntimeError("Unexpected error")):
            with patch('sys.stdin', io.StringIO('{}')):
                with self.assertRaises(RuntimeError):
                    session_init.main()

if __name__ == '__main__':
    unittest.main()
