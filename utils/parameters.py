# 1. utils/parameters.py (Constants and Unit Conversion)
# -----------------------------------------------------------------------------
import numpy as np

# --- CONSTANTES FISICAS (SI) ---
# Se usan valores típicos de ingeniería y del PDF (donde se indican).
RHO_W = 997.0          # Densidad del agua [kg/m^3][1]
G = 9.81               # Gravedad [m/s^2]
GAMMA = 1.4            # Coeficiente adiabático del aire [1]
RHO_AIR = 1.225        # Densidad del aire (a nivel del mar) [kg/m^3]
P_ATM = 101325.0       # Presión atmosférica estándar [Pa]
DT = 0.001             # Paso de tiempo para integración de Euler [s]

# --- PARAMETROS DE DISEÑO EDITABLES (Convertidos a SI internamente) ---
# Usamos valores predeterminados para la primera ejecución:
# p_i = 70 psi (aprox. 482,600 Pa manométricos -> 583,925 Pa absolutos)
# V_r = 2.0 L, V_0w = 0.5 L, A_e = 4.5 cm^2, M_r = 0.055 kg
PARAMS = {
    # Entrada de Usuario (Unidades de Enseñanza)
    'p_manometric_psi': 70.0,
    'V_r_L': 2.0,           # Volumen total de la botella [L]
    'V_0w_L': 0.5,          # Volumen inicial de agua [L]
    'A_e_cm2': 4.5,         # Área de la boquilla [cm^2]
    'A_r_cm2': 95.0,        # Área interna transversal botella (para altura) [cm^2]
    'M_r_g': 55.0,          # Masa seca del cohete [g][1]
    'H_tube_m': 1.0,        # Longitud del tubo de lanzamiento [m]
    'C_D': 0.75,            # Coeficiente de arrastre (editable)
    'A_ref_cm2': 100.0,     # Área de referencia para arrastre (ej: basado en diámetro)
    
    # Parámetros Internos (SI) - Calculados en el setup
    'P_i_abs': 0.0,         # Presión absoluta inicial [Pa]
    'V_r': 0.0,             # Volumen total de la botella [m^3]
    'V_0w': 0.0,            # Volumen inicial de agua [m^3]
    'A_e': 0.0,             # Área de la boquilla [m^2]
    'A_r': 0.0,             # Área interna botella [m^2]
    'M_r': 0.0,             # Masa seca del cohete [kg]
    'A_ref': 0.0            # Área de referencia para arrastre [m^2]
}

def convert_to_si(p):
    """Convierte los parámetros de entrada a unidades SI."""
    # Presión: psi manométricos a Pa absolutos
    p['P_i_abs'] = (p['p_manometric_psi'] * 6894.76) + P_ATM
    # Volumen: L a m^3
    p['V_r'] = p['V_r_L'] / 1000.0
    p['V_0w'] = p['V_0w_L'] / 1000.0
    # Área: cm^2 a m^2
    p['A_e'] = p['A_e_cm2'] / 10000.0
    p['A_r'] = p['A_r_cm2'] / 10000.0
    p['A_ref'] = p['A_ref_cm2'] / 10000.0
    # Masa: g a kg
    p['M_r'] = p['M_r_g'] / 1000.0
    return p

# Inicializa los parámetros en SI para la primera ejecución
PARAMS = convert_to_si(PARAMS)
# -----------------------------------------------------------------------------
