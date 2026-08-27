"""Reusable academic helpers with compatibility-preserving lazy imports.

The legacy generators depend on QMCPy interfaces that are not required by
most consumers.  Keep their public names available, but do not import them
while a notebook is loading unrelated helpers such as :mod:`classlib.nbviz`.
"""

from importlib import import_module

from . import distributions as _distributions
from . import discrepancy as _discrepancy
from . import nbviz as _nbviz
from . import options as _options
from . import plots as _plots
from . import sampling as _sampling

from .distributions import *  # re-export what distributions.__all__ says
from .discrepancy   import *  # re-export what discrepancy.__all__ says

_GENERATOR_EXPORTS = ("QPKronecker", "Kronecker", "TensorProductGrid")

__all__ = []
__all__ += getattr(_distributions, "__all__", [])
__all__ += list(_GENERATOR_EXPORTS)
__all__ += getattr(_discrepancy, "__all__", [])
__all__ += [
    "distributions",
    "generators",
    "discrepancy",
    "nbviz",
    "options",
    "plots",
    "sampling",
]

# Expose submodules on the package for legacy code
distributions = _distributions
discrepancy   = _discrepancy
nbviz         = _nbviz
options       = _options
plots         = _plots
sampling      = _sampling


def __getattr__(name):
    """Load legacy generator APIs only when a consumer requests them."""
    if name == "generators":
        module = import_module(f"{__name__}.generators")
        globals()[name] = module
        return module

    if name in _GENERATOR_EXPORTS:
        module = __getattr__("generators")
        value = getattr(module, name)
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(__all__))
