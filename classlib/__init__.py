from . import distributions as _distributions
from . import generators as _generators
from . import discrepancy as _discrepancy
from . import nbviz as _nbviz
from . import options as _options
from . import plots as _plots
from . import sampling as _sampling

from .distributions import *  # re-export what distributions.__all__ says
from .generators    import *  # re-export what generators.__all__ says
from .discrepancy   import *  # re-export what discrepancy.__all__ says

__all__ = []
__all__ += getattr(_distributions, "__all__", [])
__all__ += getattr(_generators, "__all__", [])
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
generators    = _generators
discrepancy   = _discrepancy
nbviz         = _nbviz
options       = _options
plots         = _plots
sampling      = _sampling