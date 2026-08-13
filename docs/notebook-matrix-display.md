# Notebook Matrix Display Helpers

`classlib.nbviz` provides three SymPy-backed helpers for textbook-style matrix
output in JupyterLab. They accept NumPy arrays or SymPy matrices and affect
only presentation, not the underlying calculation.

```python
import numpy as np
import sympy as sp
import classlib as cl

A = np.array([[1.0, 2.0], [3.0, 4.0]])
b = np.array([5.0, 6.0])

cl.nbviz.show_mat(A, b)
cl.nbviz.show_augmented(A, b)
cl.nbviz.show_blocks(
    [sp.eye(2), sp.Matrix([1, 2])],
    [sp.Matrix([[3, 4]]), sp.Matrix([[5]])],
)
```

- `show_mat(*objects)` displays each object as a separate typeset matrix.
- `show_augmented(A, b)` displays $[A\mid b]$ with a visible divider and
  requires `A` and `b` to have the same number of rows.
- `show_blocks(*block_rows)` displays a symbolic block matrix, with one list of
  blocks supplied for each block row.

Converting a floating-point NumPy array to a SymPy matrix improves its display;
it does not restore exactness lost in the numerical calculation.
