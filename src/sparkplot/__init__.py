from sparkplot.canvas import Canvas
from sparkplot.charset import ASCII, UNICODE, CharSet
from sparkplot.layout import assemble_line_plot
from sparkplot.rasterize import draw_line_segment
from sparkplot.scale import Scale
from sparkplot.validate import (
    validate_charset,
    validate_dimensions,
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
