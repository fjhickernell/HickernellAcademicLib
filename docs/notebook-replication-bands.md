# Notebook Replication-Band Plots

`classlib.nbviz.plot_replication_band` plots a median curve and a percentile
band from values that have already been computed across independent
replications. It optionally adds a fitted log--log trend and appends its slope
to the legend label.

This helper separates simulation from presentation. It is suitable for
sample-mean errors, density errors, quantile estimates, runtimes, or any other
diagnostic arranged as one replication axis and one plotted axis.

```python
import matplotlib.pyplot as plt
import classlib as cl

# absolute_errors has shape (number_of_replications, number_of_sample_sizes)
fig, ax = plt.subplots()
summary = cl.nbviz.plot_replication_band(
    ax,
    sample_sizes,
    absolute_errors,
    replication_axis=0,
    color=cl.nbviz.TOL_BRIGHT["blue"],
    label="IID",
    line_kwargs={"marker": "o"},
    band_alpha=0.12,
    fit_trend=True,
    slope_in_label=True,
)
ax.set_xlabel(r"Number of samples, $n$")
ax.set_ylabel("Absolute error")
ax.legend(frameon=False)
```

By default, the curve is the median and the band spans the 25th through 75th
percentiles. Supply another strictly increasing three-value `percentiles`
tuple when different lower and upper percentiles are needed; its center must
remain 50 so the plotted curve and returned `median` keep their stated
meaning.

When `fit_trend=True`, the helper fits

$$
y \approx c n^p
$$

to the plotted median curve and overlays a dotted guide. Each displayed point
has equal weight by default; pass `trend_w` to choose another weighting. The
returned dictionary contains `lower`, `median`, `upper`, `slope`, and
`coefficient`, as well as the Matplotlib `line`, `band`, and `trend_line`
artists. Fitted slopes describe the displayed data range; they are not
universal convergence guarantees.

The helper does not generate samples or compute errors. Keep model-specific
simulation and diagnostics in the consuming notebook, then pass the resulting
replication array here for consistent presentation. When the same style is
given both directly and in `line_kwargs`, the direct `color` and `label`
arguments take precedence.
