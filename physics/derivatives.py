# 3. physics/derivatives.py (EDOs for Euler - 2D Motion)
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

def calculate_drag_2d(vx_n, vy_n, params=None):
    """
    Calcula la Fuerza de Arrastre Aerodinámico en 2D.
    Retorna (F_Dx, F_Dy) - componentes de la fuerza de arrastre.
    """
    if params is None:
        params = _current_params
    C_D = params['C_D']
    A_ref = params['A_ref']
    
    # Magnitud de la velocidad
    v_mag = np.sqrt(vx_n**2 + vy_n**2)
    
    if v_mag < 1e-6:
        return 0.0, 0.0
    
    # Magnitud de la fuerza de arrastre
    F_D_mag = 0.5 * RHO_AIR * v_mag**2 * C_D * A_ref
    
    # Componentes (opuestas a la dirección de la velocidad)
    F_Dx = -F_D_mag * (vx_n / v_mag)
    F_Dy = -F_D_mag * (vy_n / v_mag)
    
    return F_Dx, F_Dy

def derivatives(Y_n, params=None):
    """
    Calcula el vector de derivadas para movimiento 2D.
    Y_n = [x_n, y_n, vx_n, vy_n, M_w_n]
    Retorna: [dx/dt, dy/dt, dvx/dt, dvy/dt, dMw/dt]
    """
    if params is None:
        params = _current_params
    
    x_n, y_n, vx_n, vy_n, M_w_n = Y_n
    
    # Velocidad total (para cálculo de empuje y fase)
    v_total = np.sqrt(vx_n**2 + vy_n**2)
    
    # 1. Variables Acopladas (Fase 2: Agua)
    if M_w_n > 0:
        P_n = water_phase.calculate_pressure(M_w_n, params)
        u_e_n = water_phase.calculate_escape_velocity(P_n, M_w_n, params)
        
        # Tasa de flujo de masa dMw/dt
        dMw_dt = -RHO_W * params['A_e'] * u_e_n
        
        # Magnitud del empuje T(t) = - dMw/dt * u_e
        Thrust_mag = -dMw_dt * u_e_n
        
        # El empuje se aplica en la dirección de la velocidad actual del cohete
        if v_total > 1e-6:
            # Dirección del empuje = dirección de la velocidad
            Thrust_x = Thrust_mag * (vx_n / v_total)
            Thrust_y = Thrust_mag * (vy_n / v_total)
        else:
            # Al inicio (tubo de lanzamiento), usar ángulo de lanzamiento
            angle = params['launch_angle_rad']
            Thrust_x = Thrust_mag * np.cos(angle)
            Thrust_y = Thrust_mag * np.sin(angle)
        
        # Masa Total (Variable)
        M_total_n = params['M_r'] + M_w_n
        
    # 2. Variables Fijas (Fase 3: Ballistic/Air Residual)
    else:
        M_w_n = 0.0 
        M_total_n = params['M_r']
        Thrust_x = 0.0
        Thrust_y = 0.0
        dMw_dt = 0.0

    # 3. Fuerzas Externas
    F_Dx, F_Dy = calculate_drag_2d(vx_n, vy_n, params)
    Gravity_y = -M_total_n * G  # Gravedad solo en Y (negativa)
    
    # 4. Derivadas del sistema EDO
    dx_dt = vx_n
    dy_dt = vy_n
    
    # Aceleraciones (Segunda Ley de Newton en cada dirección)
    dvx_dt = (Thrust_x + F_Dx) / M_total_n
    dvy_dt = (Thrust_y + F_Dy + Gravity_y) / M_total_n

    return np.array([dx_dt, dy_dt, dvx_dt, dvy_dt, dMw_dt])
# -----------------------------------------------------------------------------
