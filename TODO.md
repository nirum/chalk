# sparkplot — TODO

## Milestone 1: Canvas and Scale Primitives

- [x] Create `sparkplot/` package directory
- [x] Implement `Canvas` class in `canvas.py`
  - [x] `__init__(width, height)` — pre-allocate 2D grid filled with spaces
  - [x] `set(x, y, char)` — write character at position (origin bottom-left)
  - [x] `get(x, y)` — read character at position
  - [x] `to_string()` — render grid to string (flip rows so y=0 is bottom)
- [x] Implement `Scale` class in `scale.py`
  - [x] `__init__(data_min, data_max, pixel_min, pixel_max)`
  - [x] `apply(value)` — map data value to integer pixel coordinate
  - [x] `ticks(n)` — return `n` evenly spaced values in data range
  - [x] Handle zero-range case (constant data)
- [x] Define `CharSet` in `charset.py`
  - [x] `UNICODE` instance (box-drawing, block chars, line segments)
  - [x] `ASCII` instance (dashes, pipes, slashes, `#`)
- [x] Write unit tests
  - [x] `tests/test_canvas.py` — init, set/get, bounds, to_string
  - [x] `tests/test_scale.py` — linear mapping, edge values, zero range, ticks

## Milestone 2: Line Plot

- [x] Implement input validation in `validate.py`
  - [x] Validate iterables of int/float, convert to `list[float]`
  - [x] Reject empty data, NaN, inf
  - [x] Enforce `len(x) == len(y)` when both provided
  - [x] Validate `width >= 10`, `height >= 10`
  - [x] Validate `charset` and `render` parameter values
- [x] Implement Bresenham line rasterizer in `rasterize.py`
  - [x] `draw_line_segment(canvas, x0, y0, x1, y1, charset)`
  - [x] Character selection based on segment direction
- [x] Implement layout engine in `layout.py`
  - [x] Y-axis: 3 right-aligned numeric labels + vertical line with tick marks
  - [x] X-axis: horizontal line with tick marks + 3–5 bottom labels
  - [x] Title: centered, truncated with `…` if too wide
  - [x] Assemble full frame: title + y-axis + canvas + x-axis
- [x] Implement `line()` in `__init__.py`
  - [x] `line(y)` — infer x as `0..n-1`
  - [x] `line(x, y)` — explicit x and y
  - [x] Support `title`, `width`, `height`, `charset`, `render` params
  - [x] `render="print"` prints to stdout, `render="string"` returns string
- [x] Write tests
  - [x] `tests/test_validate.py` — bad inputs raise `ValueError`
  - [x] `tests/test_line.py` — snapshot tests (unicode + ascii)
  - [x] Create `tests/fixtures/` directory for snapshot `.txt` files

## Milestone 3: Histogram

- [x] Implement bin computation in `rasterize.py`
  - [x] Compute linear bin edges from data range and `bins` count
  - [x] Count values per bin (single pass)
- [x] Implement bar rasterizer in `rasterize.py`
  - [x] Draw vertical bars with `█` and half-block `▄` (unicode) / `#` (ascii)
  - [x] Configurable bar width (default 2 chars) with 1 char gap
- [x] Implement `hist()` in `__init__.py`
  - [x] `hist(data, bins=10)`
  - [x] Support `title`, `width`, `height`, `charset`, `render` params
  - [x] Validate `bins` is a positive integer
- [x] Write tests
  - [x] `tests/test_hist.py` — snapshot tests (unicode + ascii)
  - [x] Edge cases: single bin, all same value, one data point

## Milestone 4: Polish and Packaging

- [x] Handle edge cases across both plot types
  - [x] Single data point (line plot)
  - [x] Constant data / zero range
  - [x] Very small canvas (minimum 10x10)
  - [x] Large number of points (verify no performance cliff at ~10k)
- [x] Create `pyproject.toml`
  - [x] Package metadata (name, version, description, author, license)
  - [x] Python version requirement
  - [x] pytest as dev dependency
- [x] Write `README.md` with usage examples and sample output
- [x] Verify all snapshot tests pass on both unicode and ascii
- [x] Final review: confirm zero external dependencies
