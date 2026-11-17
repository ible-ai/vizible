"""Line-aware deterministic colored print."""

import colorsys
import hashlib
import inspect
from typing import Any, Optional, TextIO

from ._ansi import emit


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


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG relative luminance of an sRGB color, from 0 (black) to 1 (white)."""

    def linear(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = map(linear, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _generate_color(filename: str, lineno: int) -> tuple[int, int, int]:
    """Generate a deterministic vivid RGB color from a filename and line number.

    The hash picks the hue, so call sites differ by color rather than by
    shade. Lightness is then solved for a relative luminance between 0.17 and
    0.25, which keeps every color at least 3:1 contrast against both a dark
    terminal background and a white one, and never grayish.
    """
    seed = f"{filename}:{lineno}".encode()
    hash_bytes = hashlib.md5(seed).digest()

    hue = int.from_bytes(hash_bytes[:2], "big") / 65536
    target = 0.17 + 0.08 * hash_bytes[2] / 255

    low, high = 0.0, 1.0
    rgb = (0, 0, 0)
    for _ in range(20):
        lightness = (low + high) / 2
        rgb = tuple(round(c * 255) for c in colorsys.hls_to_rgb(hue, lightness, 0.9))
        if _relative_luminance(rgb) < target:
            low = lightness
        else:
            high = lightness
    return rgb


def dprint(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
    stacklevel: int = 1,
) -> None:
    """Print in a deterministic color chosen by the call site's file and line.

    Takes the same arguments as ``print``, so any ``print`` can become a
    ``dprint``. ``stacklevel`` works like it does in ``warnings.warn``: the
    default colors by the line that calls ``dprint``; pass 2 from inside your
    own helper to color by the line that calls the helper instead.
    """
    if stacklevel < 1:
        raise ValueError(f"stacklevel must be at least 1, got {stacklevel}")
    filename, lineno = _get_caller_context(depth=stacklevel)
    r, g, b = _generate_color(filename, lineno)
    # 24-bit foreground color: ESC[38;2;R;G;Bm
    emit(f"38;2;{r};{g};{b}", args, sep, end, file, flush)
