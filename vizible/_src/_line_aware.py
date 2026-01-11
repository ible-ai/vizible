"""Line-aware deterministic colored print."""

import hashlib
import inspect
from typing import Any


def _get_caller_context(depth: int = 1) -> tuple[str, int]:
    """Fetch the filename and line number at the call site.

    Args:
        depth: How many frames to go back.
               0: caller of this function
               1: caller of the caller of this function
               etc.
    """
    frame = inspect.currentframe()
    # Go back depth + 1 levels to account for _get_caller_context itself
    for _ in range(depth + 1):
        if frame is None:
            break
        frame = frame.f_back

    if frame is None:
        return "unknown", 0

    return frame.f_code.co_filename, frame.f_lineno


def _generate_color(filename: str, lineno: int) -> tuple[int, int, int]:
    """Generate a deterministic vibrant RGB color based on filename and line number."""
    seed = f"{filename}:{lineno}".encode()
    hash_bytes = hashlib.md5(seed).digest()

    r = hash_bytes[0]
    g = hash_bytes[1]
    b = hash_bytes[2]

    # Ensure visibility by boosting brightness if too dark
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    if brightness < 100:
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)

    return r, g, b


def dprint(*args: Any, sep: str = " ") -> None:
    """Print with a deterministic color based on the call site's line number."""
    # depth=1 to get the caller of dprint
    filename, lineno = _get_caller_context(depth=1)
    r, g, b = _generate_color(filename, lineno)

    text = sep.join(map(str, args))
    # ANSI escape code for 24-bit color: \033[38;2;R;G;Bm
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")
