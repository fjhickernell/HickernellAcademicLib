import os
from pathlib import Path
import subprocess
import sys
import textwrap


REPOSITORY = Path(__file__).resolve().parents[1]


def run_isolated(code: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(REPOSITORY)
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=REPOSITORY,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


def test_nbviz_import_does_not_load_generators_or_qmcpy():
    run_isolated(
        """
        import builtins
        import sys

        original_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "classlib.generators" or name.startswith("qmcpy"):
                raise AssertionError(f"unexpected optional import: {name}")
            return original_import(name, *args, **kwargs)

        builtins.__import__ = guarded_import

        from classlib.nbviz import show_augmented, show_mat

        assert callable(show_augmented)
        assert callable(show_mat)
        assert "classlib.generators" not in sys.modules
        assert not any(name == "qmcpy" or name.startswith("qmcpy.") for name in sys.modules)
        """
    )


def test_generator_namespace_is_lazy_and_public_names_are_preserved():
    run_isolated(
        """
        import sys
        import classlib

        assert "generators" in classlib.__all__
        assert "QPKronecker" in classlib.__all__
        assert "Kronecker" in classlib.__all__
        assert "TensorProductGrid" in classlib.__all__
        assert "classlib.generators" not in sys.modules

        generators = classlib.generators

        assert generators.__name__ == "classlib.generators"
        assert "classlib.generators.kronecker" not in sys.modules
        assert "classlib.generators.tensor_product_grid" not in sys.modules
        """
    )
