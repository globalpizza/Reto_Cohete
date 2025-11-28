# 6. main_simulation.py (Orquestador y Bucle Principal)
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
from utils.parameters import PARAMS, RHO_W, G, DT, P_ATM
from utils.euler import euler_step
from physics.derivatives import calculate_pressure
from visualization import plot_results

def run_simulation(params):
    """Ejecuta la simulación completa del cohete (Fases 1, 2 y 3)."""
    
    # 1. ESTADO INICIAL (SI)
    M_0w = params['V_0w'] * RHO_W
    # Y = [y, v, M_w]
    Y_n = np.array([0.0, 0.0, M_0w]) 
    
    t = 0.0
    
    # Data logging setup
    results = []
    
    # Condición de vuelo (Hasta que impacte el suelo después de altura máxima)
    flight_active = True
    
    while flight_active and t < 100.0: # Límite de tiempo de seguridad
        
        y_n, v_n, M_w_n = Y_n
        
        # 2. DETERMINACIÓN DE LA FASE
        
        if y_n < params['H_tube_m']:
            phase = 'Launch Tube' # Fase 1 (se integra como Fase 2)
            
        elif M_w_n > 1e-4: # Usamos un umbral pequeño en lugar de 1e-9 para estabilidad numérica
            phase = 'Water' # Fase 2
            
        elif calculate_pressure(M_w_n) > P_ATM and M_w_n <= 1e-4:
            phase = 'Air' # Fase 3A (Empuje residual del aire) - Simplificado en derivatives.py
            
        else:
            phase = 'Ballistic' # Fase 3B
            
            
        # 3. CÁLCULO DE VARIABLES AUXILIARES PARA LOGGING
        P_n = calculate_pressure(M_w_n)
        
        results.append({
            'Time': t, 
            'Position': y_n, 
            'Velocity': v_n, 
            'Water Mass': M_w_n,
            'Pressure': P_n,
            'Phase': phase
        })
        
        # 4. CONDICIÓN DE FIN DE VUELO
        # Si estamos en fase balística, cayendo (v < 0) y llegamos al suelo (y <= 0)
        if phase == 'Ballistic' and v_n < 0 and y_n <= 0:
            flight_active = False
            break
            
        # 5. PASO DE INTEGRACIÓN (Euler)
        Y_n = euler_step(Y_n)
        
        # Ajuste de condiciones de frontera después del paso (la masa no puede ser negativa)
        if Y_n[2] < 0:
            Y_n[2] = 0.0 # M_w_n1
        
        t += DT

    df_results = pd.DataFrame(results)
    
    # Log la velocidad inicial (v_i) al salir del tubo para el análisis
    tube_phase = df_results[df_results['Phase'] == 'Launch Tube']
    if not tube_phase.empty:
        v_i_tube = tube_phase['Velocity'].max()
        print(f"Velocidad inicial v_i (al salir del tubo): {v_i_tube:.2f} m/s")
    else:
        print("Advertencia: No se detectó fase de tubo de lanzamiento.")
    
    return df_results

# --- EJECUCIÓN DEL ORQUESTADOR ---
if __name__ == "__main__":
    print("Iniciando Simulación del Cohete de Agua...")
    print(f"Parámetros iniciales: P_i_abs = {PARAMS['P_i_abs']:.0f} Pa, V_0w = {PARAMS['V_0w']:.4f} m^3")

    df = run_simulation(PARAMS)
    plot_results(df)
# -----------------------------------------------------------------------------
