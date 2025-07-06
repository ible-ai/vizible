"""Visualization helpers and tools."""


def _colorize(text: str, color_code: int) -> None:
    """Applies ANSI color codes to the text."""
    print(f"\033[{color_code}m{text}\033[m")


def red(text: str) -> None:
    """Print red text."""
    return _colorize(text, 31)


def green(text: str) -> None:
    """Print green text."""
    return _colorize(text, 32)


def blue(text: str) -> None:
    """Print blue text."""
    return _colorize(text, 34)


def magenta(text: str) -> None:
    """Print magenta text."""
    return _colorize(text, 35)


def cyan(text: str) -> None:
    """Print cyan text."""
    return _colorize(text, 36)
