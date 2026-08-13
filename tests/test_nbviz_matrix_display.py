import numpy as np
import pytest
import sympy as sp

from classlib import nbviz


@pytest.fixture
def displayed(monkeypatch):
    objects = []
    monkeypatch.setattr(nbviz, "display", objects.append)
    return objects


def test_show_mat_displays_each_object_as_a_matrix(displayed):
    nbviz.show_mat(np.array([1.0, 2.0]), sp.Matrix([[3, 4]]))

    assert displayed == [sp.Matrix([1.0, 2.0]), sp.Matrix([[3, 4]])]


def test_show_augmented_displays_visible_divider(displayed):
    nbviz.show_augmented([[1, 2], [3, 4]], [5, 6])

    assert len(displayed) == 1
    assert isinstance(displayed[0], nbviz.Math)
    assert r"\begin{array}{cc|c}" in displayed[0].data
    assert r"1 & 2 & 5 \\ 3 & 4 & 6" in displayed[0].data


def test_show_augmented_rejects_mismatched_rows(displayed):
    with pytest.raises(ValueError, match="same number of rows"):
        nbviz.show_augmented([[1, 2], [3, 4]], [5])

    assert displayed == []


def test_show_blocks_displays_block_matrix(displayed):
    nbviz.show_blocks(
        [sp.eye(2), sp.Matrix([1, 2])],
        [sp.Matrix([[3, 4]]), sp.Matrix([[5]])],
    )

    assert len(displayed) == 1
    assert isinstance(displayed[0], sp.BlockMatrix)
    assert displayed[0].as_explicit() == sp.Matrix(
        [[1, 0, 1], [0, 1, 2], [3, 4, 5]]
    )
