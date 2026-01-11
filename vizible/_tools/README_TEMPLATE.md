# vizible

Minimal, deterministic color-coded debugging for Python.

`vizible` provides a unique way to track execution flow by assigning a stable, deterministic color to every line of code where documentation is printed.

## Features

- **`dprint(*args)`**: Prints text in a color derived from the calling file name and line number. These colors are stable across executions.
- **Classic ANSI Colors**: Quick access to `red`, `green`, `blue`, `magenta`, and `cyan`.
- **Zero Configuration**: Works out of the box in most modern terminals.

## Usage

```python
from vizible import dprint, red, green

# Every unique line gets a unique, stable color
dprint("This is always the same blue-ish color")
dprint("This is always the same orange-ish color")

# High-contrast status helpers
red("Something went wrong")
green("Process complete")
```

## Example Output

SUBSTITUTE_HERE

## Why?

When debugging loops or long log streams, visual pattern matching is faster than reading text. `vizible` allows you to "see" where your logs are coming from without reading file/line prefixes.
