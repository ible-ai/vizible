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

<pre style="background: #d4d4d4; color: #1e1e1e; padding: 15px; border-radius: 5px; font-family: monospace;">Regular print</pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: rgb(222,71,144)">Line-aware color A</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: rgb(61,203,84)">Line-aware color B</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: red">red print</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: green">green print</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: blue">blue print</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: magenta">magenta print</span></pre>
<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; font-family: monospace;"><span style="color: cyan">cyan print</span></pre>

## Why?

When debugging loops or long log streams, visual pattern matching is faster than reading text. `vizible` allows you to "see" where your logs are coming from without reading file/line prefixes.
