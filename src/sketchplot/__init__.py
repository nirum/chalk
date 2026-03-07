from sketchplot.canvas import Canvas
from sketchplot.charset import ASCII, UNICODE, CharSet
from sketchplot.layout import assemble_bar_plot, assemble_hist_plot, assemble_line_plot
from sketchplot.rasterize import compute_bins, draw_bar_groups, draw_bars, draw_line_segment
from sketchplot.scale import Scale
from sketchplot.validate import (
    validate_bar_data,
    validate_bins,
    validate_charset,
    validate_dimensions,
    validate_numbers,
    validate_render,
    validate_xy,
)


def line(
    x_or_y: list[float] | list[int],
    y: list[float] | list[int] | None = None,
    *,
    title: str | None = None,
    width: int = 60,
    height: int = 20,
    charset: str = "unicode",
    render: str = "print",
) -> str | None:
    """Render a line plot.

    Usage:
        line(y)          — x inferred as 0..n-1
        line(x, y)       — explicit x and y
    """
    validate_dimensions(width, height)
    cs_name = validate_charset(charset)
    render_mode = validate_render(render)
    cs: CharSet = UNICODE if cs_name == "unicode" else ASCII

    if y is None:
        x_vals, y_vals = validate_xy(None, x_or_y)
    else:
        x_vals, y_vals = validate_xy(x_or_y, y)

    x_scale = Scale(min(x_vals), max(x_vals), 0, width - 1)
    y_scale = Scale(min(y_vals), max(y_vals), 0, height - 1)

    canvas = Canvas(width, height)

    # Map data to canvas coordinates
    cx = [x_scale.apply(v) for v in x_vals]
    cy = [y_scale.apply(v) for v in y_vals]

    # Draw line segments between consecutive points
    for i in range(len(cx) - 1):
        draw_line_segment(canvas, cx[i], cy[i], cx[i + 1], cy[i + 1], cs)
    # Draw single point if only one
    if len(cx) == 1:
        canvas.set(cx[0], cy[0], cs.horizontal)

    result = assemble_line_plot(canvas, x_scale, y_scale, cs, title, width)

    if render_mode == "string":
        return result
    print(result)
    return None


def hist(
    data: list[float] | list[int],
    *,
    bins: int = 10,
    title: str | None = None,
    width: int = 60,
    height: int = 20,
    charset: str = "unicode",
    render: str = "print",
) -> str | None:
    """Render a histogram."""
    validate_dimensions(width, height)
    cs_name = validate_charset(charset)
    render_mode = validate_render(render)
    validated_bins = validate_bins(bins)
    cs: CharSet = UNICODE if cs_name == "unicode" else ASCII

    values = validate_numbers(data)

    edges, counts = compute_bins(values, validated_bins)
    max_count = max(counts) if counts else 0

    bar_width = 2
    gap = 1
    # Compute canvas width needed for bars
    canvas_width = len(counts) * (bar_width + gap) - gap
    canvas_width = max(canvas_width, 10)

    canvas = Canvas(canvas_width, height)
    y_scale = Scale(0, max_count, 0, height - 1)

    draw_bars(canvas, counts, max_count, cs, bar_width, gap)

    result = assemble_hist_plot(
        canvas, counts, edges, y_scale, cs, title, bar_width, gap
    )

    if render_mode == "string":
        return result
    print(result)
    return None


def bar(
    data: list[float] | list[int] | list[list[float]] | list[list[int]],
    *,
    title: str | None = None,
    width: int = 60,
    height: int = 20,
    charset: str = "unicode",
    render: str = "print",
) -> str | None:
    """Render a bar plot.

    Usage:
        bar([3, 5, 2, 8])               — single series, one bar per value
        bar([[1, 3, 5], [2, 4, 6]])     — multiple series, grouped bars
    """
    validate_dimensions(width, height)
    cs_name = validate_charset(charset)
    render_mode = validate_render(render)
    cs: CharSet = UNICODE if cs_name == "unicode" else ASCII

    series = validate_bar_data(data)
    n_series = len(series)
    n_groups = len(series[0])

    bar_width = 2
    inner_gap = 0
    outer_gap = 1
    group_width = n_series * bar_width
    canvas_width = n_groups * (group_width + outer_gap) - outer_gap
    canvas_width = max(canvas_width, 10)

    all_vals = [v for s in series for v in s]
    max_val = max(all_vals) if max(all_vals) > 0 else 1.0

    canvas = Canvas(canvas_width, height)
    y_scale = Scale(0, max_val, 0, height - 1)

    draw_bar_groups(canvas, series, max_val, cs, bar_width, inner_gap, outer_gap)

    result = assemble_bar_plot(
        canvas, n_groups, n_series, y_scale, cs, title, bar_width, inner_gap, outer_gap
    )

    if render_mode == "string":
        return result
    print(result)
    return None
