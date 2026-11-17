"""Shared ANSI output for every vizible print function."""

import os
from typing import Optional, TextIO

_RESET = "\033[0m"


def color_enabled() -> bool:
    """Return False when the user has opted out of color (https://no-color.org)."""
    return not os.environ.get("NO_COLOR")


def emit(
    sgr: str,
    args: tuple,
    sep: Optional[str],
    end: Optional[str],
    file: Optional[TextIO],
    flush: bool,
) -> None:
    """Print ``args`` like ``print`` does, wrapped in the SGR color ``sgr``.

    Each line is colored separately, so multi-line values stay colored in
    viewers that reset styling at line breaks (``less -R``, CI log pages).
    """
    text = (" " if sep is None else sep).join(map(str, args))
    if color_enabled():
        start = f"\033[{sgr}m"
        text = "\n".join(
            f"{start}{line}{_RESET}" if line else line for line in text.split("\n")
        )
    print(text, end="\n" if end is None else end, file=file, flush=flush)
