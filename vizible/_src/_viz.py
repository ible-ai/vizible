"""Fixed-color print helpers using the terminal's standard ANSI palette.

Each takes the same arguments as ``print``.
"""

from typing import Any, Optional, TextIO

from ._ansi import emit


def red(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print red text (ANSI SGR 31)."""
    emit("31", args, sep, end, file, flush)


def green(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print green text (ANSI SGR 32)."""
    emit("32", args, sep, end, file, flush)


def yellow(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print yellow text (ANSI SGR 33)."""
    emit("33", args, sep, end, file, flush)


def blue(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print blue text (ANSI SGR 34)."""
    emit("34", args, sep, end, file, flush)


def magenta(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print magenta text (ANSI SGR 35)."""
    emit("35", args, sep, end, file, flush)


def cyan(
    *args: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print cyan text (ANSI SGR 36)."""
    emit("36", args, sep, end, file, flush)
