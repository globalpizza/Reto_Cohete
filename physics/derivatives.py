# 3. physics/derivatives.py (EDOs for Euler)
# -----------------------------------------------------------------------------
from utils.parameters import PARAMS, RHO_W, G, RHO_AIR
from physics.water_phase import calculate_pressure, calculate_escape_velocity
import numpy as np

def calculate_drag(v_n):
    """Calcula la Fuerza de Arrastre Aerodinámico (FD)."""
    C_D = PARAMS['C_D']
    A_ref = PARAMS['A_ref']
    # La fuerza de arrastre siempre se opone a la velocidad
    F_D = 0.5 * RHO_AIR * (v_n**2) * C_D * A_ref
    return F_D

def derivatives(Y_n):
    """
    Calcula el vector de derivadas [dy/dt, dv/dt, dMw/dt] en el tiempo t_n.
    Y_n = [y_n, v_n, M_w_n]
    """
    y_n, v_n, M_w_n = Y_n
    
    # 1. Variables Acopladas (Fase 2: Agua)
    if M_w_n > 0:
        P_n = calculate_pressure(M_w_n)
        u_e_n = calculate_escape_velocity(P_n, M_w_n)
        
        # Tasa de flujo de masa dMw/dt [1]
        dMw_dt = -RHO_W * PARAMS['A_e'] * u_e_n
        
        # Empuje T(t) = - dMw/dt * u_e [1]
        Thrust_n = -dMw_dt * u_e_n
        
        # Masa Total (Variable)
        M_total_n = PARAMS['M_r'] + M_w_n
        
    # 2. Variables Fijas (Fase 3: Ballistic/Air Residual)
    else:
        # Transición: Masa de agua = 0. La masa total es solo la masa seca.
        M_w_n = 0.0 
        M_total_n = PARAMS['M_r']
        Thrust_n = 0.0 # Simplificación: ignoramos el pequeño empuje residual del aire para la Ballística Pura.
        dMw_dt = 0.0

    # 3. Fuerzas Externas (Aplican en todas las fases)
    F_D_n = calculate_drag(v_n)
    Gravity_n = M_total_n * G
    
    # 4. Derivadas del sistema EDO
    dy_dt = v_n
    
    # dv/dt = (Suma de Fuerzas) / M_total [1]
    dv_dt = (Thrust_n - Gravity_n - np.sign(v_n) * F_D_n) / M_total_n
    
    # El arrastre siempre se opone a la velocidad, por eso np.sign(v_n)

    return np.array([dy_dt, dv_dt, dMw_dt])
# -----------------------------------------------------------------------------
