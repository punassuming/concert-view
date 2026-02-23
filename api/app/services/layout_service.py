import math

from app.models.layout import Layout, LayoutSlot


def generate_grid_layout(feed_count: int, name: str = "Grid Layout") -> Layout:
    """Create an evenly-spaced grid layout for the given number of feeds."""
    cols = math.ceil(math.sqrt(feed_count))
    rows = math.ceil(feed_count / cols) if cols else 1
    cell_w = 1.0 / cols
    cell_h = 1.0 / rows
    slots: list[LayoutSlot] = []
    for i in range(feed_count):
        r, c = divmod(i, cols)
        slots.append(
            LayoutSlot(
                feed_id=f"feed_{i}",
                x=round(c * cell_w, 4),
                y=round(r * cell_h, 4),
                width=round(cell_w, 4),
                height=round(cell_h, 4),
            )
        )
    return Layout(name=name, slots=slots)


def generate_pip_layout(feed_count: int, name: str = "PiP Layout") -> Layout:
    """Create a picture-in-picture layout: one main view with small overlays."""
    slots: list[LayoutSlot] = [
        LayoutSlot(feed_id="feed_0", x=0.0, y=0.0, width=1.0, height=1.0, z_index=0)
    ]
    pip_size = 0.25
    margin = 0.02
    for i in range(1, feed_count):
        idx = i - 1
        slots.append(
            LayoutSlot(
                feed_id=f"feed_{i}",
                x=round(1.0 - pip_size - margin, 4),
                y=round(margin + idx * (pip_size + margin), 4),
                width=pip_size,
                height=pip_size,
                z_index=i,
            )
        )
    return Layout(name=name, slots=slots)
