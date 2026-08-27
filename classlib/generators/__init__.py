"""Legacy generators loaded on demand.

Importing this namespace must not require every historical QMCPy interface.
Each generator remains available at its established public name and imports
its implementation only when that name is used.
"""

from importlib import import_module

_EXPORT_MODULES = {
    "QPKronecker": ".kronecker_qp",
    "Kronecker": ".kronecker",
    "TensorProductGrid": ".tensor_product_grid",
}

__all__ = list(_EXPORT_MODULES)


def __getattr__(name):
    if name not in _EXPORT_MODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(_EXPORT_MODULES[name], __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
