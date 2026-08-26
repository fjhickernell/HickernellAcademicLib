import matplotlib.pyplot as plt
import numpy as np
import pytest

from classlib import nbviz


def test_plot_replication_band_summarizes_precomputed_values():
    x = np.array([1, 2, 4], dtype=float)
    values = np.array(
        [
            [1, 2, 4],
            [2, 4, 8],
            [3, 6, 12],
            [4, 8, 16],
        ],
        dtype=float,
    )
    expected = np.percentile(values, [25, 50, 75], axis=0)

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        color="tab:blue",
        label="Method",
        line_kwargs={"marker": "o"},
    )

    np.testing.assert_allclose(result["lower"], expected[0])
    np.testing.assert_allclose(result["median"], expected[1])
    np.testing.assert_allclose(result["upper"], expected[2])
    np.testing.assert_allclose(result["line"].get_xdata(), x)
    np.testing.assert_allclose(result["line"].get_ydata(), expected[1])
    assert result["line"].get_label() == "Method"
    assert result["band"] in ax.collections
    assert result["slope"] is None
    assert result["trend_line"] is None
    plt.close(fig)


def test_plot_replication_band_fits_trend_and_labels_slope():
    x = np.array([1, 2, 4, 8], dtype=float)
    center = x**-1
    values = np.vstack([0.8 * center, center, 1.2 * center])

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        label="Method",
        fit_trend=True,
        slope_in_label=True,
    )

    assert result["slope"] == pytest.approx(-1.0)
    assert result["coefficient"] == pytest.approx(1.0)
    assert result["line"].get_label() == r"Method (slope $-1.00$)"
    assert result["trend_line"] is ax.lines[-1]
    assert result["trend_line"].get_linestyle() == ":"
    assert ax.get_xscale() == "log"
    assert ax.get_yscale() == "log"
    plt.close(fig)


def test_plot_replication_band_accepts_one_shot_trend_weights():
    x = np.array([1, 2, 4, 8], dtype=float)
    center = x**-1
    values = np.vstack([0.8 * center, center, 1.2 * center])

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        fit_trend=True,
        trend_w=(weight for weight in np.ones_like(x)),
    )

    assert result["slope"] == pytest.approx(-1.0)
    plt.close(fig)


def test_plot_replication_band_uses_explicit_style_arguments_and_effective_label():
    x = np.array([1, 2, 4, 8], dtype=float)
    center = x**-1
    values = np.vstack([0.8 * center, center, 1.2 * center])

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        color="tab:blue",
        label="Explicit",
        line_kwargs={"color": "tab:red", "label": "Nested"},
        fit_trend=True,
        slope_in_label=True,
    )

    assert result["line"].get_color() == "tab:blue"
    assert result["line"].get_label() == r"Explicit (slope $-1.00$)"
    plt.close(fig)

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        line_kwargs={"label": "Nested only"},
        fit_trend=True,
        slope_in_label=True,
    )

    assert result["line"].get_label() == r"Nested only (slope $-1.00$)"
    plt.close(fig)


def test_plot_replication_band_supports_replications_on_second_axis():
    x = np.array([1, 2, 4], dtype=float)
    values = np.array(
        [
            [1, 2, 3, 4],
            [2, 4, 6, 8],
            [4, 8, 12, 16],
        ],
        dtype=float,
    )
    expected = np.percentile(values, [10, 50, 90], axis=1)

    fig, ax = plt.subplots()
    result = nbviz.plot_replication_band(
        ax,
        x,
        values,
        replication_axis=1,
        percentiles=(10, 50, 90),
    )

    np.testing.assert_allclose(result["lower"], expected[0])
    np.testing.assert_allclose(result["median"], expected[1])
    np.testing.assert_allclose(result["upper"], expected[2])
    plt.close(fig)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"percentiles": (25, 75)}, "exactly three"),
        ({"percentiles": (50, 25, 75)}, "strictly increasing"),
        ({"percentiles": (10, 40, 90)}, "center percentile must be 50"),
        ({"slope_in_label": True}, "requires fit_trend"),
    ],
)
def test_plot_replication_band_rejects_invalid_options(kwargs, message):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match=message):
        nbviz.plot_replication_band(
            ax,
            [1, 2, 3],
            np.ones((2, 3)),
            **kwargs,
        )
    plt.close(fig)


def test_plot_replication_band_requires_one_summary_per_x():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="same length"):
        nbviz.plot_replication_band(
            ax,
            [1, 2],
            np.ones((3, 4)),
        )
    plt.close(fig)
