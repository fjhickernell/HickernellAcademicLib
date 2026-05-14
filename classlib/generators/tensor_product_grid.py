import numpy as np

# 👇 IMPORTANT: import the SAME base class you used for Kronecker.
# In your code this might be `DiscreteDistribution` or `AbstractDiscreteDistribution`.
# For example, if Kronecker has:
#   from qmcpy.discrete_distribution import AbstractDiscreteDistribution
# then do the same here.
from qmcpy.discrete_distribution.abstract_discrete_distribution import AbstractLDDiscreteDistribution  # adjust to match Kronecker


class TensorProductGrid(AbstractLDDiscreteDistribution):
    """
    Deterministic tensor-product grid on [0,1]^d, implemented as a
    QMCPy DiscreteDistribution-style object.

    Parameters
    ----------
    levels_per_dim : int or sequence of int
        If int L: use L equally spaced levels in each dimension.
        If sequence (L_1, ..., L_d): use L_j levels in dimension j.
    dimension : int, optional
        If levels_per_dim is a scalar, this is required and gives d.
        If levels_per_dim is a sequence, defaults to len(levels_per_dim).
    centered : bool, default True
        If True, use midpoints (k + 0.5)/L_j. If False, use linspace grid.
    endpoint : bool, default False
        Only used when centered=False; passed to np.linspace.
    """

    def __init__(
        self,
        levels_per_dim,
        dimension=None,
        *,
        centered=True,
        endpoint=False,
        replications=None, 
        randomize=True, 
        seed=None
    ):
        # ---- Normalize dimension & levels ---------------------------------
        if np.isscalar(levels_per_dim):
            if dimension is None:
                raise ValueError(
                    "If levels_per_dim is scalar, you must supply `dimension`."
                )
            L = int(levels_per_dim)
            if L <= 0:
                raise ValueError("levels_per_dim must be positive.")
            levels = np.full(int(dimension), L, dtype=int)
        else:
            levels = np.asarray(levels_per_dim, dtype=int)
            if levels.ndim != 1:
                raise ValueError("levels_per_dim must be a 1D sequence of ints.")
            if np.any(levels <= 0):
                raise ValueError("All entries of levels_per_dim must be positive.")
            if dimension is None:
                dimension = int(levels.size)
            elif int(dimension) != levels.size:
                raise ValueError(
                    f"dimension={dimension} does not match "
                    f"len(levels_per_dim)={levels.size}"
                )

        self.levels_per_dim = levels
        d = int(dimension)

        self.centered = bool(centered)
        self.endpoint = bool(endpoint)

        # ---- Call parent constructor just like Kronecker does ------------
        # 👉 VERY IMPORTANT: Make this line match your Kronecker __init__.
        # For example, if Kronecker has:
        #
        #   super().__init__(dimension=d, randomize=False, mimics="StdUniform", **kwargs)
        #
        # then do the same here. Copy & paste from Kronecker and just swap in d.
        super(TensorProductGrid,self).__init__(dimension,replications,seed,d_limit=dimension,n_limit=np.inf)

        # ---- Precompute the grid in [0,1]^d -------------------------------
        axes = []
        for L in self.levels_per_dim:
            if self.centered:
                k = np.arange(L, dtype=float)
                axis = (k + 0.5) / L        # midpoints in (0,1)
            else:
                axis = np.linspace(0.0, 1.0, num=L, endpoint=self.endpoint)
            axes.append(axis)

        mesh = np.meshgrid(*axes, indexing="ij")
        points = np.stack([m.ravel(order="C") for m in mesh], axis=1)

        self._points = points                 # shape (n_total, d)
        self.n_total = int(points.shape[0])

        # Optional: bounds in [0,1]^d for nice printing
        self.lower_bound = np.zeros(d, dtype=float)
        self.upper_bound = np.ones(d, dtype=float)

    # ---- QMCPy sampling interface ----------------------------------------

    def gen_samples(self, n):
        """
        Return the first n grid points (tiling if n > n_total).

        Parameters
        ----------
        n : int
            Number of samples requested.

        Returns
        -------
        x : ndarray, shape (n, dimension)
        """
        n = int(n)
        if n <= self.n_total:
            return self._points[:n, :].copy()

        # If more points requested than in the grid, tile deterministically.
        reps = (n + self.n_total - 1) // self.n_total
        tiled = np.tile(self._points, (reps, 1))
        return tiled[:n, :].copy()

    # QMCPy usually calls the sampler like sampler(n)
    def __call__(self, n, **kwargs):
        return self.gen_samples(n)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"dimension={self.dimension}, "
            f"levels_per_dim={self.levels_per_dim.tolist()}, "
            f"centered={self.centered}, "
            f"endpoint={self.endpoint}, "
            f"n_total={self.n_total})"
        )