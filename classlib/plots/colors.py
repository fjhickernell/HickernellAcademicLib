"""
Color palettes and semantic color roles for classlib plots.
Designed to be backend-agnostic (slides + notebooks).
"""

# --- Paul Tol Bright palette ---

TOL_BRIGHT = {
    "blue":   "#4477AA",
    "cyan":   "#66CCEE",
    "green":  "#228833",
    "yellow": "#CCBB44",
    "red":    "#EE6677",
    "purple": "#AA3377",
    "grey":   "#BBBBBB",
}

TOL_BRIGHT_ORDER = ["blue", "cyan", "green", "yellow", "red", "purple", "grey"]


def tol_bright_list(order=TOL_BRIGHT_ORDER):
    return [TOL_BRIGHT[k] for k in order]


def set_tol_bright_cycle(ax, order=TOL_BRIGHT_ORDER):
    ax.set_prop_cycle(color=tol_bright_list(order))


# --- Semantic roles (recommended usage) ---

curve_color  = TOL_BRIGHT["blue"]
tail_color   = TOL_BRIGHT["green"]      # use for α tail regions
reject_color = TOL_BRIGHT["red"]        # use for rejection regions (later slides)
accent_color = TOL_BRIGHT["purple"]
neutral_color = TOL_BRIGHT["grey"]