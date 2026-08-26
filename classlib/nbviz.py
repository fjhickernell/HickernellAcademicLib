"""
nbviz.py — lightweight plotting & notebook init utilities
Author: ChatGPT (GPT-5 Thinking)

Features
--------
- One-call plotting style setup with optional LaTeX text (`init`).
- Paul Tol's Bright palette helpers + easy color cycle (`set_tol_color_cycle`).
- Session configuration for figure paths, save format, and epsilon (`configure`).
- Convenient `savefig("name")` that respects configured path/format.
- Log–log trend-line fit + overlay (`fit_log_trend`, `plot_log_trend_line`).
- Replication median/IQR bands with optional fitted trends
  (`plot_replication_band`).
- Textbook-style matrix display (`show_mat`, `show_augmented`, `show_blocks`).
- Simple notebook highlight CSS injection for tagged cells (id="nbviz-highlight").
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display, HTML, Latex, Math
from cycler import cycler
import pandas as pd
import sympy as sp
from sympy import Matrix

__all__ = [
    "init", "configure", "savefig",
    "set_tol_color_cycle", "set_highlight_color",
    "tol_colors",
    "fit_log_trend", "plot_log_trend_line", "plot_replication_band",
    "TOL_BRIGHT", "TOL_BRIGHT_ORDER", "TINY", 
    "note",  "note_md", "display_latex_df", "DEFAULT_MATH_RENAME",
    "show_mat", "show_augmented", "show_blocks"
]

# ---- Defaults / constants ----
DEFAULT_HIGHLIGHT_COLOR = "#e6f7ff"   # light blue (for markdown/cell adornment)

from classlib.plots.colors import (
    TOL_BRIGHT,
    TOL_BRIGHT_ORDER,
    tol_bright_list,
    set_tol_bright_cycle,
)

# ---- Session state (configured via configure()) ----
FIGPATH: Path | None = None
SAVEFIGS: bool = False            # default: don't save unless user asks
IMGFRMT: str = "pdf"
TINY: float = 1e-9                # small epsilon, exposed as public constant


# ---- Internal helpers ----

def _inject_css(color: str) -> None:
    """Insert a style tag that colors cells tagged 'highlight'. Scoped; no hiding."""
    css = f"""
    <style id="nbviz-highlight">
      .jp-Cell[data-tags~="highlight"] {{
        box-shadow: inset 4px 0 0 {color};
        background: rgba(230,247,255,0.35);
      }}
      .highlight-note {{
        padding: 0.75em 1em;
        background-color: #e6f7ff;  /* light blue background */
        border-radius: 6px;
        margin: 1em 0;
      }}      }}
      .highlight-note strong {{
        color: #224466;
      }}
      .highlight-note em {{
        color: #2c3e50;
      }}
    </style>
    """
    try:
        display(HTML(css))
    except Exception:
        # If display isn't available (e.g., non-notebook), just skip.
        pass

def _tol_list(order: Iterable[int | str] | None = None) -> list[str]:
    """Return Tol Bright hexes in requested order (names or 1-based indices)."""
    if order is None:
        keys = TOL_BRIGHT_ORDER
    else:
        keys = []
        for o in order:
            if isinstance(o, str):
                keys.append(o)
            else:
                i = int(o)
                if not (1 <= i <= len(TOL_BRIGHT_ORDER)):
                    raise IndexError(f"Tol index {i} out of range 1..{len(TOL_BRIGHT_ORDER)}")
                keys.append(TOL_BRIGHT_ORDER[i - 1])
    return [TOL_BRIGHT[k] for k in keys]


def _clean_xyw(
    x: Iterable[float],
    y: Iterable[float],
    n_which: slice | np.ndarray | None = None,
    w: float | Iterable[float] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Shared cleaner for log–log fitting: selects, weights, and filters finite/positive."""
    x_arr = np.asarray(list(x), dtype=float).ravel()
    y_arr = np.asarray(list(y), dtype=float).ravel()
    if n_which is not None:
        x_arr = x_arr[n_which].ravel()
        y_arr = y_arr[n_which].ravel()

    if w is None:
        w_arr = np.sqrt(1.0 / x_arr)  # good for linearly spaced x
    elif np.isscalar(w):
        w_arr = np.full_like(x_arr, float(w), dtype=float)
    else:
        w_arr = np.asarray(list(w), dtype=float).ravel()
        if n_which is not None:
            w_arr = w_arr[n_which].ravel()

    mask = np.isfinite(x_arr) & np.isfinite(y_arr) & (x_arr > 0) & (y_arr > 0)
    x_arr, y_arr, w_arr = x_arr[mask], y_arr[mask], w_arr[mask]

    if x_arr.size < 2:
        raise ValueError("Need at least two valid (x,y) points with x>0, y>0 for log–log fit.")
    return x_arr, y_arr, w_arr


# ---- Public: setup / configuration ----

def init(
    *,
    font_family: str = "serif",
    use_tex: bool = True,
    mathtext_fontset: str = "dejavuserif",
    axes_labelsize: int = 18,
    axes_titlesize: int = 18,
    tick_labelsize: int = 14,
    legend_fontsize: int = 14,
    legend_frameon: bool = False,
    highlight_color: str = DEFAULT_HIGHLIGHT_COLOR,
    set_tol_cycle: bool = True,
) -> None:
    """
    Set global plotting style and inject notebook CSS.

    Notes:
    - No stdout/display publisher manipulation here.
    - We enable interactive plotting (`plt.ion()`) for notebook friendliness.
    """
    np.seterr(divide="raise", invalid="raise")

    rc = {
        "font.family": font_family,
        "text.usetex": bool(use_tex),
        "axes.labelsize": axes_labelsize,
        "axes.titlesize": axes_titlesize,
        "xtick.labelsize": tick_labelsize,
        "ytick.labelsize": tick_labelsize,
        "legend.fontsize": legend_fontsize,
        "legend.frameon": legend_frameon,
    }
    
    if use_tex:
        rc["text.latex.preamble"] = r"\usepackage{amsmath}"

    if not use_tex:
        rc["mathtext.fontset"] = mathtext_fontset  # only relevant when not using TeX
    
    mpl.rcParams.update(rc)

    # Friendly defaults for saving and layout
    mpl.rcParams.setdefault("savefig.bbox", "tight")
    mpl.rcParams.setdefault("figure.autolayout", True)

    if set_tol_cycle:
        set_tol_color_cycle()

    _inject_css(highlight_color)

    # ---- Pandas display options ----
    try:
        pd.set_option("display.width", 200)
        pd.set_option("display.max_colwidth", 200)
        pd.set_option("display.expand_frame_repr", False)
    except Exception:
        pass


    # Make sure figures display inline without requiring explicit plt.show()
    try:
        plt.ion()
        try:
            import matplotlib_inline.backend_inline as be
            be.set_matplotlib_formats("png")
        except Exception:
            pass
    except Exception:
        pass


def configure(
    *,
    figpath: str | Path | None = None,
    savefigs: bool = False,
    imgfrmt: str = "pdf",
    tiny: float = 1e-9,
    make_dirs: bool = True,
    set_savefig_rc: bool = True,
    transparent: bool = False,
) -> None:
    """Set session-wide figure/output defaults for notebooks."""
    global FIGPATH, SAVEFIGS, IMGFRMT, TINY
    FIGPATH = Path(figpath) if figpath is not None else None
    SAVEFIGS = bool(savefigs)
    IMGFRMT = str(imgfrmt).lower()
    TINY = float(tiny)

    if make_dirs and FIGPATH is not None:
        try:
            FIGPATH.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    if set_savefig_rc:
        mpl.rcParams.update({
            "savefig.format": IMGFRMT,
            "savefig.bbox": "tight",
            "savefig.transparent": bool(transparent),
            # editable text in pdf/ps (so text stays text in Adobe/Keynote)
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        })


def savefig(name: str, *, ext: str | None = None, **kwargs) -> None:
    """Save the current figure if saving is enabled and a figpath is set.
    If saving is disabled or no figpath is configured, do nothing.
    """
    if not SAVEFIGS or FIGPATH is None:
        return
    suffix = (ext or IMGFRMT).lstrip(".")
    outfile = FIGPATH / f"{name}.{suffix}"
    plt.gcf().savefig(outfile, **kwargs)

# ---- Public: color utilities ----

def set_tol_color_cycle(
    *,
    order: Iterable[int | str] | None = None,
    axes: mpl.axes.Axes | None = None
) -> None:
    """Set the Tol Bright color cycle globally (rcParams) or for a single Axes."""
    cycle = cycler(color=_tol_list(order))
    if axes is None:
        mpl.rcParams["axes.prop_cycle"] = cycle
    else:
        axes.set_prop_cycle(cycle)


def set_highlight_color(color: str = DEFAULT_HIGHLIGHT_COLOR) -> None:
    """Update the highlight color mid-notebook (replaces style block)."""
    _inject_css(color)

def tol_colors(n: int, *, order: Iterable[int | str] | None = None) -> list[str]:
    """Return n Tol Bright colors (hex). Repeats/cycles if n exceeds palette size."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    base = _tol_list(order)
    if n <= len(base):
        return base[:n]
    return [base[i % len(base)] for i in range(n)]
    
# ---- Public: log–log trend fitting and plotting ----

def fit_log_trend(
    x: Iterable[float],
    y: Iterable[float],
    n_which: slice | np.ndarray | None = None,
    w: float | Iterable[float] | None = None,
) -> tuple[float, float]:
    """
    Fit log(y) ~ slope * log(x) + intercept on the selected data.

    Returns
    -------
    power : float
        The slope in log–log space (often negative for decays).
    coef : float
        exp(intercept), so the fitted model is y ≈ coef * x**power.
    """
    x_arr, y_arr, w_arr = _clean_xyw(x, y, n_which, w)
    slope, intercept = np.polyfit(np.log(x_arr), np.log(y_arr), deg=1, w=w_arr)
    power = float(slope)
    coef = float(np.exp(intercept))
    return power, coef


def plot_log_trend_line(
    ax: plt.Axes,
    x: Iterable[float],
    y: Iterable[float],
    *,
    n_which: slice | np.ndarray | None = None,
    w: float | Iterable[float] | None = None,
    endpoints: str | tuple[float, float] = "data",
    color: str | None = None,
    ls: str = "--",
    label: str | None = None,
    show_as_rate: bool = True,
    decimals: int = 2,
) -> tuple[float, float]:
    """
    Fit y ≈ coef * x**power on log–log, then plot a guide line through chosen endpoints.

    Parameters
    ----------
    endpoints : "data" | "ends" | (x0, x1)
        - "data": from min(x_sel) to max(x_sel) after cleaning
        - "ends": from first to last in the (cleaned) order
        - (x0, x1): explicit numeric endpoints
    """
    x_sel, y_sel, w_sel = _clean_xyw(x, y, n_which, w)
    power, coef = fit_log_trend(x_sel, y_sel, w=w_sel)

    if isinstance(endpoints, tuple) and len(endpoints) == 2:
        x0, x1 = map(float, endpoints)
    elif endpoints == "ends":
        x0, x1 = float(x_sel[0]), float(x_sel[-1])
    else:  # "data"
        x0, x1 = float(np.min(x_sel)), float(np.max(x_sel))

    y0 = coef * (x0 ** power)
    y1 = coef * (x1 ** power)

    if label is None:
        if show_as_rate:
            rate = -power
            label = rf"$\mathcal{{O}}(n^{{-{rate:.{decimals}f}}})$"
        else:
            label = rf"$\mathcal{{O}}(n^{{{power:.{decimals}f}}})$"

    ax.loglog([x0, x1], [y0, y1], color=color, linestyle=ls, label=label)
    return power, coef


def plot_replication_band(
    ax: plt.Axes,
    x: Iterable[float],
    values: np.ndarray,
    *,
    replication_axis: int = 0,
    percentiles: tuple[float, float, float] = (25, 50, 75),
    color: str | None = None,
    label: str | None = None,
    line_kwargs: Mapping[str, Any] | None = None,
    band_alpha: float = 0.15,
    band_kwargs: Mapping[str, Any] | None = None,
    fit_trend: bool = False,
    trend_n_which: slice | np.ndarray | None = None,
    trend_w: float | Iterable[float] | None = 1.0,
    trend_kwargs: Mapping[str, Any] | None = None,
    slope_in_label: bool = False,
    slope_decimals: int = 2,
) -> dict[str, Any]:
    """Plot a median curve and middle replication band from computed values.

    ``values`` must contain one axis of independent replications. Collapsing
    that axis must leave a one-dimensional sequence aligned with ``x``. The
    default percentiles plot the median and middle 50% of the replications.

    When ``fit_trend`` is true, a log--log least-squares trend is overlaid.
    Each displayed point has equal weight by default; use ``trend_w`` to
    choose another weighting. Set ``slope_in_label`` to append the fitted
    power to the median-curve legend label. The caller remains responsible
    for axis labels and scales; fitting a trend sets both axes to logarithmic
    scales through :func:`plot_log_trend_line`.

    Returns the summary arrays, Matplotlib artists, and fitted trend
    parameters so callers can reuse them without recomputing percentiles.
    """
    x_arr = np.asarray(list(x), dtype=float).ravel()
    values_arr = np.asarray(values, dtype=float)
    percentile_arr = np.asarray(percentiles, dtype=float)

    if values_arr.ndim == 0:
        raise ValueError("values must have a replication axis")
    if percentile_arr.shape != (3,):
        raise ValueError("percentiles must contain exactly three values")
    if (
        np.any(percentile_arr < 0)
        or np.any(percentile_arr > 100)
        or np.any(np.diff(percentile_arr) <= 0)
    ):
        raise ValueError(
            "percentiles must be strictly increasing values between 0 and 100"
        )
    if percentile_arr[1] != 50:
        raise ValueError("the center percentile must be 50 (the median)")
    if slope_in_label and not fit_trend:
        raise ValueError("slope_in_label requires fit_trend=True")

    summary = np.percentile(
        values_arr, percentile_arr, axis=replication_axis
    )
    lower, median, upper = (np.asarray(row) for row in summary)
    if lower.ndim != 1:
        raise ValueError(
            "collapsing replication_axis must leave one value for each x"
        )
    if len(x_arr) != len(median):
        raise ValueError("x and the summarized values must have the same length")

    line_options = dict(line_kwargs or {})
    if color is not None:
        line_options["color"] = color
    if label is not None:
        line_options["label"] = label
    (line,) = ax.plot(x_arr, median, **line_options)
    effective_label = line.get_label()

    band_options = dict(band_kwargs or {})
    band_options.setdefault("color", line.get_color())
    band_options.setdefault("alpha", band_alpha)
    band_options.setdefault("linewidth", 0)
    band = ax.fill_between(x_arr, lower, upper, **band_options)

    slope = coefficient = trend_line = None
    if fit_trend:
        trend_options = {
            "color": line.get_color(),
            "ls": ":",
            "label": "_nolegend_",
        }
        trend_options.update(trend_kwargs or {})
        slope, coefficient = plot_log_trend_line(
            ax,
            x_arr,
            median,
            n_which=trend_n_which,
            w=trend_w,
            **trend_options,
        )
        trend_line = ax.lines[-1]
        if slope_in_label and not effective_label.startswith("_"):
            line.set_label(
                rf"{effective_label} (slope ${slope:.{slope_decimals}f}$)"
            )

    return {
        "lower": lower,
        "median": median,
        "upper": upper,
        "line": line,
        "band": band,
        "slope": slope,
        "coefficient": coefficient,
        "trend_line": trend_line,
    }


def plot_power_line(
    ax: plt.Axes,
    x: Iterable[float] | tuple[float, float],
    *,
    power: float,
    coef: float | None = None,
    anchor: tuple[float, float] | None = None,  # (x_ref, y_ref) to infer coef if coef is None
    endpoints: str | tuple[float, float] | None = None,
    color: str | None = None,
    ls: str = "--",
    label: str | None = None,
    show_as_rate: bool = True,
    decimals: int = 2,
):
    """
    Plot y = coef * x**power on log–log between chosen endpoints.

    Parameters
    ----------
    x : array-like or (x0, x1)
        If array-like, we use first→last unless `endpoints` overrides.
        If a 2-tuple, it's treated as explicit (x0, x1).
    power : float
        The log–log slope (decays typically have negative power).
    coef : float, optional
        Coefficient in y = coef * x**power. If omitted, `anchor` must be given.
    anchor : (x_ref, y_ref), optional
        If provided (and `coef` is None), we set coef = y_ref / x_ref**power.
    endpoints : "data" | "ends" | (x0, x1) | None
        - "data": span min(x)→max(x) if x is array-like
        - "ends": span first→last of x (after flattening)
        - (x0, x1): explicit endpoints
        - None: if x is a 2-tuple, use it; else use "ends".
    color, ls, label : styling
    show_as_rate : bool
        If True, label as O(n^{-alpha}) with alpha = -power; else O(n^{power}).
    decimals : int
        Digits in the default label.

    Returns
    -------
    power, coef : tuple[float, float]
        The (power, coef) actually used to draw the line.
    """
    # Resolve endpoints
    if isinstance(x, tuple) and len(x) == 2 and endpoints is None:
        x0, x1 = float(x[0]), float(x[1])
    else:
        xs = np.asarray(list(x), float).ravel()
        if endpoints is None or endpoints == "ends":
            if xs.size < 2:
                raise ValueError("Need at least two x values or a 2-tuple for endpoints.")
            x0, x1 = float(xs[0]), float(xs[-1])
        elif endpoints == "data":
            x0, x1 = float(np.min(xs)), float(np.max(xs))
        elif isinstance(endpoints, tuple) and len(endpoints) == 2:
            x0, x1 = map(float, endpoints)
        else:
            raise ValueError("Invalid `endpoints`. Use 'data', 'ends', a 2-tuple, or None.")

    if x0 <= 0 or x1 <= 0:
        raise ValueError("Endpoints must be positive for log–log plotting.")

    # Determine coefficient
    if coef is None:
        if anchor is None:
            raise ValueError("Provide either `coef` or `anchor=(x_ref, y_ref)`.")
        x_ref, y_ref = map(float, anchor)
        if x_ref <= 0 or y_ref <= 0:
            raise ValueError("Anchor must have positive x_ref and y_ref.")
        coef = float(y_ref / (x_ref ** power))
    else:
        coef = float(coef)

    # Build points
    y0 = coef * (x0 ** power)
    y1 = coef * (x1 ** power)

    # Default label
    if label is None:
        if show_as_rate:
            alpha = -power
            label = rf"$\mathcal{{O}}(n^{{-{alpha:.{decimals}f}}})$"
        else:
            label = rf"$\mathcal{{O}}(n^{{{power:.{decimals}f}}})$"

    ax.loglog([x0, x1], [y0, y1], color=color, linestyle=ls, label=label)
    return float(power), float(coef)

# ---- Highlight note ----
def note(html: str):
    """
    Render a blue callout box in a Jupyter notebook using the
    CSS class `.highlight-note` injected by `_inject_css`.

    Example
    -------
    cl.nbviz.note("<strong>Reminder:</strong> Tune tolerance before running.")
    """
    return HTML(f'<div class="highlight-note">{html}</div>')

try:
    import markdown as _markdown_lib
except Exception:
    _markdown_lib = None


def note_md(text: str):
    """
    Render a blue callout box whose contents are written in Markdown.
    Requires the 'markdown' package; falls back to raw text if missing.
    """
    if _markdown_lib is not None:
        inner_html = _markdown_lib.markdown(text)
    else:
        # Fallback: minimal escaping, still boxed
        inner_html = text.replace("<", "&lt;").replace(">", "&gt;")
    return HTML(f'<div class="highlight-note">{inner_html}</div>')


# ---- Matrix display helpers (JupyterLab-friendly) ----

def show_mat(*objects) -> None:
    """Display arrays or SymPy matrices as separate typeset matrices."""
    for obj in objects:
        display(Matrix(obj))


def show_augmented(A, b) -> None:
    """Display the augmented matrix [A | b] with a visible divider."""
    A_display = Matrix(A)
    b_display = Matrix(b)
    if A_display.rows != b_display.rows:
        raise ValueError("A and b must have the same number of rows")

    entries = [
        list(A_display.row(i)) + list(b_display.row(i))
        for i in range(A_display.rows)
    ]
    body = r" \\ ".join(
        " & ".join(sp.latex(entry) for entry in row) for row in entries
    )
    columns = "c" * A_display.cols + "|" + "c" * b_display.cols
    display(Math(rf"\left[\begin{{array}}{{{columns}}}{body}\end{{array}}\right]"))


def show_blocks(*block_rows) -> None:
    """Display a block matrix; pass one list of blocks per block row."""
    display(sp.BlockMatrix([[Matrix(block) for block in row] for row in block_rows]))


# ---- DataFrame display helper (JupyterLab-friendly) ----

DEFAULT_MATH_RENAME = {
    "n": r"$n$",
    "p": r"$p$",
    "alpha": r"$\alpha$",
    "lambda": r"$\lambda$",
    "lam": r"$\lambda$",
    "mu": r"$\mu$",
    "nu": r"$\nu$",
}

def display_latex_df(
    df: pd.DataFrame,
    *,
    rename: dict[str, str] | None = None,
    float_format: str = "{:.3f}",
) -> None:
    """
    Display a DataFrame in JupyterLab as an HTML table, while allowing MathJax
    to typeset $...$ in column headers.
    """
    out = df.copy()

    mapping = dict(DEFAULT_MATH_RENAME)
    if rename:
        mapping.update(rename)

    out = out.rename(columns=mapping)

    styler = (
        out.style
        .format(float_format)
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "right")]},
        ])
    )

    display(styler)
