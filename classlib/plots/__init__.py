"""Plotting utilities for MATH 565 classlib."""

from .colors import (
    TOL_BRIGHT,
    TOL_BRIGHT_ORDER,
    tol_bright_list,
    set_tol_bright_cycle,
    curve_color,
    tail_color,
    reject_color,
    accent_color,
    neutral_color,
)

from .diagnostics import (
    plot_middle_half_sample_mean,
    plot_multiple_middle_half_sample_means,
)

from .plot_utils import (
    annotate_axis_marks,
    annotate_xaxis_marks,
    annotate_yaxis_marks,
    shade_under_curve,
)

__all__ = [
    "plot_middle_half_sample_mean",
    "plot_multiple_middle_half_sample_means",
    "annotate_axis_marks",
    "annotate_xaxis_marks",
    "annotate_yaxis_marks",
    "shade_under_curve",

    "TOL_BRIGHT",
    "TOL_BRIGHT_ORDER",
    "tol_bright_list",
    "set_tol_bright_cycle",

    "curve_color",
    "tail_color",
    "reject_color",
    "accent_color",
    "neutral_color",
]



