r"""Make the README and a rendered preview from the real ANSI demo output.

> Usage:
python3 vizible/_tools/_make_readme.py

"""

import io
import os
import re
import sys
from html import escape
from contextlib import redirect_stdout
from types import FunctionType


# Support the documented command when run from a source checkout.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import vizible


_ANSI_PALETTE = {
    # The ANSI standard specifies these SGR codes, not their RGB values. This
    # preview intentionally uses xterm's default palette; users' terminals may
    # choose different values.
    "31": "#cd0000",
    "32": "#00cd00",
    "34": "#0000ee",
    "35": "#cd00cd",
    "36": "#00cdcd",
}


def _ansi_line_to_svg_text(text: str) -> tuple[str, str]:
    """Return the printable text and the color represented by one ANSI line."""
    text = text.replace("\r", "")
    rgb_match = re.search(r"\x1b\[38;2;(\d+);(\d+);(\d+)m", text)
    if rgb_match:
        color = f"rgb({rgb_match.group(1)}, {rgb_match.group(2)}, {rgb_match.group(3)})"
    else:
        basic_match = re.search(r"\x1b\[(\d+)m", text)
        color = _ANSI_PALETTE.get(basic_match.group(1), "#d4d4d4") if basic_match else "#d4d4d4"

    printable = re.sub(r"\x1b\[[0-9;]*m", "", text)
    return printable, color


def _render_svg(lines: list[str]) -> str:
    """Render captured output as an SVG GitHub can display without CSS sanitizing it."""
    line_height = 30
    top = 54
    width = 720
    height = top + len(lines) * line_height + 24
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">vizible ANSI output</title>",
        "<desc id=\"desc\">A dark terminal preview with color-coded log lines.</desc>",
        f'<rect width="{width}" height="{height}" rx="8" fill="#1e1e1e"/>',
        '<text x="24" y="31" fill="#9da5b4" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="15">Captured ANSI output</text>',
    ]
    for index, line in enumerate(lines):
        printable, color = _ansi_line_to_svg_text(line)
        y = top + index * line_height
        output.append(
            f'<text x="24" y="{y}" fill="{color}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="18">{escape(printable)}</text>'
        )
    output.append("</svg>")
    return "\n".join(output) + "\n"


def demo():
    print("Regular print")
    vizible.dprint("Line-aware color A")
    vizible.dprint("Line-aware color B")
    vizible.red("red print")
    vizible.green("green print")
    vizible.blue("blue print")
    vizible.magenta("magenta print")
    vizible.cyan("cyan print")


def _run_demo_with_stable_filename() -> None:
    """Run the real demo with a location-independent call-site filename.

    ``dprint`` intentionally incorporates its caller's filename in the color
    seed. A generated documentation asset should not change merely because a
    release runs from a different checkout directory, so only this demo uses a
    fixed filename in its frame metadata.
    """
    stable_code = demo.__code__.replace(co_filename="README demo")
    stable_demo = FunctionType(
        stable_code,
        demo.__globals__,
        name=demo.__name__,
        argdefs=demo.__defaults__,
        closure=demo.__closure__,
    )
    stable_demo()


def main():
    # Capture all sys out.
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        _run_demo_with_stable_filename()
    joined_content = buffer.getvalue()
    contents = [x for x in joined_content.split("\n") if x]
    # Get README template.
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, "README_TEMPLATE.md"), "r") as f:
        template = f.read()

    # Write the README and an image whose colors survive GitHub's HTML sanitizer.
    project_root = os.path.dirname(os.path.dirname(cur_dir))
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(assets_dir, "demo.svg"), "w") as f:
        f.write(_render_svg(contents))

    with open(os.path.join(project_root, "README.md"), "w") as f:
        f.write(template)
    vizible.green("Done")


if __name__ == "__main__":
    main()
