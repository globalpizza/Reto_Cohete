# 6. main_simulation.py (Orquestador y Bucle Principal)
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
from utils.parameters import PARAMS, RHO_W, G, DT, P_ATM
from utils.euler import euler_step
import physics.water_phase as water_phase
from visualization import plot_results

# Función exportada desde water_phase
calculate_pressure = water_phase.calculate_pressure

def run_simulation(params):
    """Ejecuta la simulación completa del cohete en 2D (Fases 1, 2 y 3)."""
    
    # Establecer los parámetros actuales para la simulación
    from physics.derivatives import set_simulation_params
    set_simulation_params(params)
    
    # 1. ESTADO INICIAL (SI) - Ahora en 2D
    M_0w = params['V_0w'] * RHO_W
    angle = params['launch_angle_rad']
    
    # Y = [x, y, vx, vy, M_w]
    # Posición inicial en origen, velocidades iniciales en cero
    Y_n = np.array([0.0, 0.0, 0.0, 0.0, M_0w]) 
    
    t = 0.0
    
    # Data logging setup
    results = []
    
    # Condición de vuelo
    flight_active = True
    max_height_reached = False
    
    while flight_active and t < 100.0: # Límite de tiempo de seguridad
        
        x_n, y_n, vx_n, vy_n, M_w_n = Y_n
        
        # Velocidad total
        v_total = np.sqrt(vx_n**2 + vy_n**2)
        
        # 2. DETERMINACIÓN DE LA FASE
        # Distancia recorrida desde el origen
        dist_from_origin = np.sqrt(x_n**2 + y_n**2)
        
        if dist_from_origin < params['H_tube_m']:
            phase = 'Launch Tube' # Fase 1
            
        elif M_w_n > 1e-4:
            phase = 'Water' # Fase 2
            
        elif calculate_pressure(M_w_n, params) > P_ATM and M_w_n <= 1e-4:
            phase = 'Air' # Fase 3A
            
        else:
            phase = 'Ballistic' # Fase 3B
            
        # Detectar altura máxima
        if vy_n < 0 and y_n > 0:
            max_height_reached = True
            
        # 3. CÁLCULO DE VARIABLES AUXILIARES PARA LOGGING
        P_n = calculate_pressure(M_w_n, params)
        
        results.append({
            'Time': t,
            'X_Position': x_n,
            'Y_Position': y_n, 
            'X_Velocity': vx_n,
            'Y_Velocity': vy_n,
            'Total_Velocity': v_total,
            'Water Mass': M_w_n,
            'Pressure': P_n,
            'Phase': phase
        })
        
        # 4. CONDICIÓN DE FIN DE VUELO
        # Si toca el suelo (y <= 0) después de haber alcanzado altura máxima
        if y_n <= 0 and max_height_reached and t > 0.1:
            flight_active = False
            # Guardar posición final en el suelo
            results.append({
                'Time': t,
                'X_Position': x_n,
                'Y_Position': 0.0,
                'X_Velocity': 0.0,
                'Y_Velocity': 0.0,
                'Total_Velocity': 0.0,
                'Water Mass': 0.0,
                'Pressure': P_ATM,
                'Phase': 'Landed'
            })
            break
            
        # 5. PASO DE INTEGRACIÓN (Euler)
        Y_n = euler_step(Y_n, params)
        
        # Ajuste de condiciones de frontera
        if Y_n[4] < 0:  # M_w_n
            Y_n[4] = 0.0
        
        t += DT

    df_results = pd.DataFrame(results)
    
    # Log información del vuelo
    max_height = df_results['Y_Position'].max()
    max_range = df_results['X_Position'].max()
    max_velocity = df_results['Total_Velocity'].max()
    
    print(f"Ángulo de lanzamiento: {params['launch_angle_deg']:.1f}°")
    print(f"Altura máxima alcanzada: {max_height:.2f} m")
    print(f"Alcance horizontal máximo: {max_range:.2f} m")
    print(f"Velocidad máxima: {max_velocity:.2f} m/s")
    
    return df_results

# --- EJECUCIÓN DEL ORQUESTADOR ---
if __name__ == "__main__":
    print("Iniciando Simulación del Cohete de Agua...")
    print(f"Parámetros iniciales: P_i_abs = {PARAMS['P_i_abs']:.0f} Pa, V_0w = {PARAMS['V_0w']:.4f} m^3")

    df = run_simulation(PARAMS)
    plot_results(df)
# -----------------------------------------------------------------------------
