import io
import os
import unittest
from unittest.mock import patch

from vizible import blue, cyan, green, magenta, red, yellow


class TestViz(unittest.TestCase):
    def setUp(self):
        # Color assertions must not depend on the developer's own NO_COLOR.
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("NO_COLOR", None)

    def test_each_helper_uses_its_sgr_code(self):
        for helper, code in [
            (red, 31),
            (green, 32),
            (yellow, 33),
            (blue, 34),
            (magenta, 35),
            (cyan, 36),
        ]:
            out = io.StringIO()
            helper("text", file=out)
            self.assertEqual(out.getvalue(), f"\033[{code}mtext\033[0m\n", helper.__name__)

    def test_helpers_accept_print_arguments(self):
        out = io.StringIO()
        red("loss", 0.5, sep="=", end="", file=out)
        self.assertEqual(out.getvalue(), "\033[31mloss=0.5\033[0m")

    def test_helpers_accept_non_strings(self):
        out = io.StringIO()
        green({"a": 1}, file=out)
        self.assertIn("{'a': 1}", out.getvalue())

    def test_helpers_print_to_stdout_by_default(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            cyan("hello")
        self.assertEqual(fake_out.getvalue(), "\033[36mhello\033[0m\n")

    def test_no_color_disables_escape_codes(self):
        out = io.StringIO()
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            blue("plain", file=out)
        self.assertEqual(out.getvalue(), "plain\n")


if __name__ == "__main__":
    unittest.main()
