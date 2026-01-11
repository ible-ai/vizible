r"""Make README.md with real time demo.

> Usage:
python vizible/_tools/_make_readme.py

"""

import io
import os
import re
from contextlib import redirect_stdout


import vizible


def _format_html(text: str, black_background: bool = True) -> str:
    # Handle Reset
    text = re.sub(r"\x1b\[0?m", "</span>", text)

    # Remove carriage returns
    text = text.replace("\r", "")
    background_color = "#1e1e1e" if black_background else "#d4d4d4"
    color = "#d4d4d4" if black_background else "#1e1e1e"
    return f'<pre style="background: {background_color}; color: {color}; padding: 15px; border-radius: 5px; font-family: monospace;">{text}</pre>'


def _ansi_to_html(text):
    # Basic ANSI logic
    # \x1b[38;2;R;G;Bm -> <span style="color: rgb(R,G,B)">
    # \x1b[31m -> <span style="color: red">
    # \x1b[0m or \x1b[m -> </span>

    # Handle RGB
    rgb_substituted_text = re.sub(
        r"\x1b\[38;2;(\d+);(\d+);(\d+)m",
        r'<span style="color: rgb(\1,\2,\3)">',
        text,
    )
    if rgb_substituted_text != text:
        return _format_html(rgb_substituted_text)

    if re.search(r"\x1b\[(\d+)m", text):
        # Handle Basic 16 colors (just the ones we use)
        colors = {
            "31": "red",
            "32": "green",
            "34": "blue",
            "35": "magenta",
            "36": "cyan",
        }
        specified_color_text = text
        for code, name in colors.items():
            specified_color_text = specified_color_text.replace(
                f"\x1b[{code}m",
                f'<span style="color: {name}">',
            )
        return _format_html(specified_color_text)

    # Text without any ANSI codes.
    return _format_html(text, black_background=False)


def demo():
    print("Regular print")
    vizible.dprint("Line-aware color A")
    vizible.dprint("Line-aware color B")
    vizible.red("red print")
    vizible.green("green print")
    vizible.blue("blue print")
    vizible.magenta("magenta print")
    vizible.cyan("cyan print")


_SUBSTITUTION_TAG = "SUBSTITUTE_HERE"


def main():
    # Capture all sys out.
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        demo()
    joined_content = buffer.getvalue()
    contents = [x for x in joined_content.split("\n") if x]
    html_contents = []
    for content in contents:
        html_contents.append(_ansi_to_html(content))
    html_content = "\n".join(html_contents)
    vizible.magenta("HTML content generated.")

    # Get README template.
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, "README_TEMPLATE.md"), "r") as f:
        template = f.read()

    # Substitute formatted stdout into README.
    template = template.replace(_SUBSTITUTION_TAG, html_content)
    vizible.blue("Substitution completed.")

    # Write formatted README to disk.
    project_root = os.path.dirname(os.path.dirname(cur_dir))
    with open(os.path.join(project_root, "README.md"), "w") as f:
        f.write(template)
    vizible.green("Done")


if __name__ == "__main__":
    main()
