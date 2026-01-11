import unittest
from unittest.mock import patch
import io
import os

from vizible._src._line_aware import _get_caller_context, _generate_color, dprint


class TestLineAware(unittest.TestCase):
    def test_get_caller_context(self):
        # depth=0 should get the caller of _get_caller_context, which is this line
        filename, lineno = _get_caller_context(depth=0)
        self.assertEqual(os.path.basename(filename), "_line_aware_test.py")
        self.assertEqual(lineno, 12)  # Line 12 is where _get_caller_context is called

    def test_generate_color_is_deterministic(self):
        c1 = _generate_color("test.py", 10)
        c2 = _generate_color("test.py", 10)
        c3 = _generate_color("test.py", 11)

        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

        for color in [c1, c2, c3]:
            for channel in color:
                self.assertGreaterEqual(channel, 0)
                self.assertLessEqual(channel, 255)

    def test_dprint_outputs_ansi_color(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            dprint("hello world")
            output = fake_out.getvalue()

            # Check for ANSI escape sequences
            self.assertTrue(output.startswith("\033[38;2;"))
            self.assertIn("hello world", output)
            self.assertTrue(output.endswith("\033[0m\n"))

    def test_dprint_multiple_args(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            dprint("hello", 123, True)
            output = fake_out.getvalue()
            self.assertIn("hello 123 True", output)

    def test_dprint_different_lines_different_colors(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out1:
            dprint("line A")

        with patch("sys.stdout", new=io.StringIO()) as fake_out2:
            dprint("line B")  # This is on a different line than the one above

        color1 = fake_out1.getvalue().split("m")[0]
        color2 = fake_out2.getvalue().split("m")[0]
        self.assertNotEqual(color1, color2)


if __name__ == "__main__":
    unittest.main()
