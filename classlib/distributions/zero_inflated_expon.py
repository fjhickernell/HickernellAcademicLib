"""
zero_inflated_expon distribution
--------------------------------


Zero-inflated exponential:
P(X=0) = p_zero;  for x>0, X|X>0 ~ Exponential(rate) with mean = 1/rate.
"""


import numpy as np
from scipy import stats




class zero_inflated_expon:
    """
    Zero-inflated exponential distribution.


    Parameters
    ----------
    p_zero : float in [0,1)
        P(X=0) = p_zero
    rate : float > 0
        Exponential rate for the positive part
    """


    def __init__(self, p_zero=0.2, rate=0.1):
        if not (0.0 <= p_zero < 1.0):
            raise ValueError("p_zero must be in [0,1).")
        if rate <= 0:
            raise ValueError("rate must be > 0.")
        self.p_zero = float(p_zero)
        self.rate = float(rate)


    # Public CDF (right-continuous): F(0) = p_zero
    def cdf(self, x, *args, **kwargs):
        p0, lam = self.p_zero, self.rate
        x = np.asarray(x, dtype=float)
        # For x < 0: 0; for x >= 0: p0 + (1-p0)*(1 - e^{-lam x})
        return np.where(x < 0.0, 0.0, p0 + (1.0 - p0) * (1.0 - np.exp(-lam * x)))


    # Closed-form PPF (quantile)
    def ppf(self, q):
        p0, lam = self.p_zero, self.rate
        q = np.asarray(q, dtype=float)
        out = np.zeros_like(q, dtype=float)
        mask = (q > p0) & (q < 1.0)
        t = (q[mask] - p0) / (1.0 - p0)
        out[mask] = -np.log1p(-t) / lam
        out = np.where(q >= 1.0, np.inf, out)
        out = np.where(q < 0.0, np.nan, out)
        return out
   
    def mean(self):
        p0, lam = self.p_zero, self.rate
        return (1.0 - p0) / lam
   
    def var(self):
        p0, lam = self.p_zero, self.rate
        return (1.0 - p0**2) / lam**2
   
    def std(self):
        return np.sqrt(self.var())