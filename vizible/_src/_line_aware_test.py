import unittest
from unittest.mock import patch
import inspect
import io
import os

from vizible._src._line_aware import (
    _generate_color,
    _get_caller_context,
    _relative_luminance,
    dprint,
)


class TestLineAware(unittest.TestCase):
    def setUp(self):
        # Color assertions must not depend on the developer's own NO_COLOR.
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("NO_COLOR", None)

    def test_get_caller_context(self):
        # depth=0 should get the caller of _get_caller_context, which is this line
        expected_line = inspect.currentframe().f_lineno + 1
        filename, lineno = _get_caller_context(depth=0)
        self.assertEqual(os.path.basename(filename), "_line_aware_test.py")
        self.assertEqual(lineno, expected_line)

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


    def test_colors_are_vivid_and_readable_on_dark_and_light(self):
        def contrast(a, b):
            la, lb = sorted([_relative_luminance(a), _relative_luminance(b)], reverse=True)
            return (la + 0.05) / (lb + 0.05)

        for lineno in range(1, 1001):
            rgb = _generate_color("/some/project/app.py", lineno)
            self.assertGreaterEqual(contrast(rgb, (30, 30, 30)), 3.0, rgb)
            self.assertGreaterEqual(contrast(rgb, (255, 255, 255)), 3.0, rgb)
            # Not grayish: the strongest and weakest channels are far apart.
            self.assertGreaterEqual(max(rgb) - min(rgb), 100, rgb)

    def test_dprint_accepts_print_arguments(self):
        out = io.StringIO()
        dprint("a", "b", sep="-", end="!", file=out, flush=True)
        value = out.getvalue()
        self.assertIn("a-b", value)
        self.assertTrue(value.endswith("\033[0m!"))

    def test_dprint_none_sep_and_end_mean_defaults_like_print(self):
        out = io.StringIO()
        dprint("a", "b", sep=None, end=None, file=out)
        self.assertIn("a b", out.getvalue())
        self.assertTrue(out.getvalue().endswith("\n"))

    def test_dprint_colors_each_line_of_multiline_text(self):
        out = io.StringIO()
        dprint("one\ntwo", file=out)
        lines = out.getvalue().split("\n")
        self.assertTrue(lines[0].startswith("\033[38;2;") and lines[0].endswith("\033[0m"))
        self.assertTrue(lines[1].startswith("\033[38;2;") and lines[1].endswith("\033[0m"))
        self.assertEqual(lines[0].split("m")[0], lines[1].split("m")[0])

    def test_stacklevel_colors_by_the_helpers_caller(self):
        def helper(text, out):
            dprint(text, file=out, stacklevel=2)

        def color(out):
            return out.getvalue().split("m")[0]

        a, b = io.StringIO(), io.StringIO()
        calling_line = inspect.currentframe().f_lineno + 1
        helper("first", a)
        helper("second", b)

        r, g, bl = _generate_color(__file__, calling_line)
        self.assertEqual(color(a), f"\033[38;2;{r};{g};{bl}")
        # Different calling lines, so different colors despite one dprint line.
        self.assertNotEqual(color(a), color(b))

    def test_stacklevel_must_be_positive(self):
        with self.assertRaises(ValueError):
            dprint("x", stacklevel=0)

    def test_no_color_disables_escape_codes(self):
        out = io.StringIO()
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            dprint("plain", 1, file=out)
        self.assertEqual(out.getvalue(), "plain 1\n")

    def test_empty_no_color_keeps_color(self):
        out = io.StringIO()
        with patch.dict(os.environ, {"NO_COLOR": ""}):
            dprint("x", file=out)
        self.assertTrue(out.getvalue().startswith("\033[38;2;"))


if __name__ == "__main__":
    unittest.main()
