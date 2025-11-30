# 3. physics/derivatives.py (EDOs for Euler)
# -----------------------------------------------------------------------------
from utils.parameters import PARAMS, RHO_W, G, RHO_AIR
import physics.water_phase as water_phase
import numpy as np

# Variable global para parámetros actuales de la simulación
_current_params = PARAMS

def set_simulation_params(params):
    """Establece los parámetros para la simulación actual."""
    global _current_params
    _current_params = params

def get_current_params():
    """Obtiene los parámetros actuales de la simulación."""
    return _current_params

def calculate_drag(v_n, params=None):
    """Calcula la Fuerza de Arrastre Aerodinámico (FD)."""
    if params is None:
        params = _current_params
    C_D = params['C_D']
    A_ref = params['A_ref']
    # La fuerza de arrastre siempre se opone a la velocidad
    F_D = 0.5 * RHO_AIR * (v_n**2) * C_D * A_ref
    return F_D

def derivatives(Y_n, params=None):
    """
    Calcula el vector de derivadas [dy/dt, dv/dt, dMw/dt] en el tiempo t_n.
    Y_n = [y_n, v_n, M_w_n]
    """
    if params is None:
        params = _current_params
    
    y_n, v_n, M_w_n = Y_n
    
    # 1. Variables Acopladas (Fase 2: Agua)
    if M_w_n > 0:
        P_n = water_phase.calculate_pressure(M_w_n, params)
        u_e_n = water_phase.calculate_escape_velocity(P_n, M_w_n, params)
        
        # Tasa de flujo de masa dMw/dt [1]
        dMw_dt = -RHO_W * params['A_e'] * u_e_n
        
        # Empuje T(t) = - dMw/dt * u_e [1]
        Thrust_n = -dMw_dt * u_e_n
        
        # Masa Total (Variable)
        M_total_n = params['M_r'] + M_w_n
        
    # 2. Variables Fijas (Fase 3: Ballistic/Air Residual)
    else:
        # Transición: Masa de agua = 0. La masa total es solo la masa seca.
        M_w_n = 0.0 
        M_total_n = params['M_r']
        Thrust_n = 0.0 # Simplificación: ignoramos el pequeño empuje residual del aire para la Ballística Pura.
        dMw_dt = 0.0

    # 3. Fuerzas Externas (Aplican en todas las fases)
    F_D_n = calculate_drag(v_n, params)
    Gravity_n = M_total_n * G
    
    # 4. Derivadas del sistema EDO
    dy_dt = v_n
    
    # dv/dt = (Suma de Fuerzas) / M_total [1]
    dv_dt = (Thrust_n - Gravity_n - np.sign(v_n) * F_D_n) / M_total_n
    
    # El arrastre siempre se opone a la velocidad, por eso np.sign(v_n)

    return np.array([dy_dt, dv_dt, dMw_dt])
# -----------------------------------------------------------------------------
