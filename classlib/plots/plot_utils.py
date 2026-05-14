from __future__ import annotations

from typing import Sequence, Optional, List

import numpy as np


def annotate_axis_marks(
    ax,
    positions: Sequence[float],
    labels: Sequence[str],
    *,
    axis: str = "x",
    colors: Optional[Sequence[Optional[str]]] = None,
    tick_length: float = 0.05,
    tick_linewidth: float = 2.0,
    tick_kwargs: Optional[dict] = None,
    text_offset_pts: float = -18.0,
    fontsize: Optional[float] = None,
    ha: Optional[str] = None,
    va: Optional[str] = None,
):
    """
    Place math labels near an axis at specified positions, with small ticks.

    This is designed to work reliably in both:
      - Quarto revealjs slides (Matplotlib backend in render)
      - Jupyter notebooks

    Parameters
    ----------
    ax : matplotlib Axes
    positions, labels : same length
      Positions (data coords) and text (usually math strings like r"$\\mu_0$").
    axis : {"x","y"}
      Which axis to annotate.
    colors : optional list matching positions
      Color per mark; None means Matplotlib default.
    tick_length : float
      Tick extends from axis into the margin by this amount in axis-transform coords.
      For axis="x": from y=0 down to y=-tick_length in xaxis transform.
      For axis="y": from x=0 left to x=-tick_length in yaxis transform.
    text_offset_pts : float
      Offset for label in points (negative puts below x-axis / left of y-axis).
      For axis="x": (dx,dy)=(0,text_offset_pts).
      For axis="y": (dx,dy)=(text_offset_pts,0).
    """
    if axis not in {"x", "y"}:
        raise ValueError('axis must be "x" or "y"')

    pos = np.asarray(positions, dtype=float)
    if len(pos) != len(labels):
        raise ValueError("positions and labels must have the same length")

    if colors is None:
        colors = [None] * len(pos)
    if len(colors) != len(pos):
        raise ValueError("colors must be None or have the same length as positions")

    if tick_kwargs is None:
        tick_kwargs = {}

    if ha is None:
        ha = "center" if axis == "x" else "right"
    if va is None:
        va = "top" if axis == "x" else "center"

    artists: List[object] = []

    if axis == "x":
        tr = ax.get_xaxis_transform()
        for x, lab, col in zip(pos, labels, colors):
            line = ax.plot(
                [x, x],
                [0.0, -tick_length],
                transform=tr,
                clip_on=False,
                linewidth=tick_linewidth,
                color=col,
                **tick_kwargs,
            )[0]
            artists.append(line)

            ann = ax.annotate(
                lab,
                xy=(x, 0.0),
                xycoords=("data", "axes fraction"),
                xytext=(0.0, text_offset_pts),
                textcoords="offset points",
                ha=ha,
                va=va,
                fontsize=fontsize,
                color=col,
            )
            artists.append(ann)

    else:
        tr = ax.get_yaxis_transform()
        for y, lab, col in zip(pos, labels, colors):
            line = ax.plot(
                [0.0, -tick_length],
                [y, y],
                transform=tr,
                clip_on=False,
                linewidth=tick_linewidth,
                color=col,
                **tick_kwargs,
            )[0]
            artists.append(line)

            ann = ax.annotate(
                lab,
                xy=(0.0, y),
                xycoords=("axes fraction", "data"),
                xytext=(text_offset_pts, 0.0),
                textcoords="offset points",
                ha=ha,
                va=va,
                fontsize=fontsize,
                color=col,
            )
            artists.append(ann)

    return artists


def annotate_xaxis_marks(
    ax,
    xs: Sequence[float],
    labels: Sequence[str],
    *,
    colors: Optional[Sequence[Optional[str]]] = None,
    tick_height: float = 0.05,
    tick_linewidth: float = 2.0,
    tick_kwargs: Optional[dict] = None,
    text_offset_pts: float = -18.0,
    fontsize: Optional[float] = None,
    ha: str = "center",
    va: str = "top",
):
    """
    Backwards-compatible wrapper for x-axis marks.
    """
    return annotate_axis_marks(
        ax,
        xs,
        labels,
        axis="x",
        colors=colors,
        tick_length=tick_height,
        tick_linewidth=tick_linewidth,
        tick_kwargs=tick_kwargs,
        text_offset_pts=text_offset_pts,
        fontsize=fontsize,
        ha=ha,
        va=va,
    )


def annotate_yaxis_marks(
    ax,
    ys: Sequence[float],
    labels: Sequence[str],
    *,
    colors: Optional[Sequence[Optional[str]]] = None,
    tick_width: float = 0.05,
    tick_linewidth: float = 2.0,
    tick_kwargs: Optional[dict] = None,
    text_offset_pts: float = -10.0,
    fontsize: Optional[float] = None,
    ha: str = "right",
    va: str = "center",
):
    """
    Symmetric helper for y-axis marks.
    """
    return annotate_axis_marks(
        ax,
        ys,
        labels,
        axis="y",
        colors=colors,
        tick_length=tick_width,
        tick_linewidth=tick_linewidth,
        tick_kwargs=tick_kwargs,
        text_offset_pts=text_offset_pts,
        fontsize=fontsize,
        ha=ha,
        va=va,
    )


def shade_under_curve(ax, x, y, *, where=None, baseline=0.0, color=None, alpha=0.3, zorder=None):
    """
    Shade area between y(x) and 0 over a subset of x.

    where:
      - None: shade entire curve
      - callable: f(x) -> bool mask
      - array-like mask: same length as x
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    if where is None:
        mask = np.ones_like(x, dtype=bool)
    elif callable(where):
        mask = np.asarray(where(x), dtype=bool)
    else:
        mask = np.asarray(where, dtype=bool)

    if mask.shape != x.shape:
        raise ValueError("where mask must have the same shape as x")

    return ax.fill_between(
        x[mask],
        baseline,
        y[mask],
        alpha=alpha,
        color=color,
        zorder=zorder,
    )

