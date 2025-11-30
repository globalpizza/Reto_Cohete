# 4. utils/euler.py (Numerical Integration Scheme)
# -----------------------------------------------------------------------------
import numpy as np
from utils.parameters import DT
from physics.derivatives import derivatives

def euler_step(Y_n, params=None):
    """Aplica el método de Euler para avanzar un paso de tiempo DT."""
    dY_dt_n = derivatives(Y_n, params)
    # Y_{n+1} = Y_n + (dY/dt)_n * DT
    Y_n1 = Y_n + dY_dt_n * DT
    return Y_n1
# -----------------------------------------------------------------------------
