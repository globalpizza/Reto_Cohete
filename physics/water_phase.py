# 2. physics/water_phase.py (Core Functions: P(t) and u_e(t))
# -----------------------------------------------------------------------------
from utils.parameters import PARAMS, GAMMA, P_ATM, RHO_W, G
import numpy as np

def calculate_pressure(M_w_n, params=None):
    """Calcula la presión absoluta instantánea P(t) usando la Ley Adiabática."""
    if params is None:
        params = PARAMS
    P_i = params['P_i_abs']
    V_r = params['V_r']
    V_0w = params['V_0w']
    
    # 1. Volumen de agua instantáneo
    V_w_n = M_w_n / RHO_W
    
    # 2. Volumen de aire instantáneo y volumen inicial de aire
    V_air_n = V_r - V_w_n
    V_air_0 = V_r - V_0w
    
    # 3. Cálculo de la presión P(t)
    if V_air_n <= 0:
        return P_ATM  # El cohete está completamente lleno de agua o error
    
    P_n = P_i * (V_air_0 / V_air_n)**GAMMA
    return P_n

def calculate_escape_velocity(P_n, M_w_n, params=None):
    """
    Calcula la velocidad de escape instantánea u_e(t) usando la fórmula completa de Bernoulli.
    Esta es la 'solución exacta' pedida, incluyendo el término hidrostático dinámico. [1]
    """
    if params is None:
        params = PARAMS
    A_r = params['A_r']
    A_e = params['A_e']
    
    V_w_n = M_w_n / RHO_W
    
    # 1. Diferencia de altura dinámica (h1 - h2)
    # Asumiendo que V_w(t) está distribuido en el área A_r: h_diff = V_w(t) / A_r
    H_diff_n = V_w_n / A_r 

    # 2. Factor geométrico de área
    Area_Factor = A_r**2 / (A_r**2 - A_e**2)
    
    # 3. Término de Presión (dominante)
    Term_Pressure = 2.0 * Area_Factor * (P_n - P_ATM) / RHO_W
    
    # 4. Término de Gravedad/Hidrostático (pequeño, pero incluido para exactitud)
    Term_Gravity = 2.0 * G * Area_Factor * H_diff_n
    
    # 5. u_e(t)
    if Term_Pressure + Term_Gravity < 0:
        # Esto sucede cuando P_n < P_ATM, el escape se detiene.
        return 0.0
    
    u_e_n = np.sqrt(Term_Pressure + Term_Gravity)
    return u_e_n
# -----------------------------------------------------------------------------
