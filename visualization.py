# 5. visualization.py (Plotting and Analysis)
# -----------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.parameters import PARAMS, RHO_W, G, P_ATM, GAMMA

def calculate_approx_tsiolkovsky(df, u_e_avg):
    """
    Calcula la velocidad de la Aproximación 2 (Presión Constante/u_e promedio) 
    para fines pedagógicos. Este es el Error del 14.5% mencionado en el PDF. [1]
    """
    M_r = PARAMS['M_r']
    M_0w = PARAMS['V_0w'] * RHO_W
    
    # Velocidad al inicio de Fase 2 (Water)
    # Filtramos la fase 'Water' y tomamos el primer valor
    water_phase_df = df[df['Phase'] == 'Water']
    if water_phase_df.empty:
         # Fallback si no hay fase de agua (ej. error o condiciones iniciales raras)
         v_i = 0.0
         t_water = np.array([])
         t_water_rel = np.array([])
    else:
        v_i = water_phase_df['Velocity'].iloc[0]
        t_water = water_phase_df['Time'].to_numpy()
        # Ajustar tiempo para que empiece en 0 relativo a la fase de agua para la fórmula simplificada
        # Ojo: La fórmula de Tsiolkovsky asume t desde el inicio del empuje. 
        # Si hay fase 'Launch Tube', el tiempo absoluto es mayor.
        # Para la aproximación pedagógica simple, usaremos t relativo al inicio de la fase de agua.
        t_water_rel = t_water - t_water[0]

    # Modelo lineal de masa para la Aprox. 2 (Simplificación del PDF) [1]
    # M_w(t) = M_0w - m_dot * t
    # m_dot = rho * Ae * ue
    Mw_t_approx = M_0w - RHO_W * PARAMS['A_e'] * u_e_avg * t_water_rel
    
    # Evitar logaritmo de cero o negativo
    Mw_t_approx[Mw_t_approx < 1e-9] = 1e-9 
    
    # Ecuación de Tsiolkovsky simplificada (sin considerar Arrastre/Gravedad en esta aproximación)
    # v(t) = v_i + u_e * ln(m0 / m(t))
    # m0 = Mr + M0w
    # m(t) = Mr + Mw(t)
    v_approx = v_i + u_e_avg * np.log((M_r + M_0w) / (M_r + Mw_t_approx))
    
    return t_water, v_approx

def plot_results(df_results):
    """Genera las gráficas para trayectoria 2D del cohete."""
    
    # --- 1. Trayectoria 2D (X vs Y) ---
    plt.figure(figsize=(12, 8))
    
    colors = {'Launch Tube': 'purple', 'Water': 'blue', 'Air': 'red', 'Ballistic': 'gray', 'Landed': 'green'}
    for phase, group in df_results.groupby('Phase'):
        plt.plot(group['X_Position'], group['Y_Position'], 
                label=phase, color=colors.get(phase, 'black'), linewidth=2)

    plt.axhline(y=0, color='green', linestyle='-', linewidth=3, alpha=0.5, label='Suelo')
    plt.xlabel('Alcance Horizontal (m)', fontsize=12)
    plt.ylabel('Altura (m)', fontsize=12)
    plt.title('Trayectoria 2D del Cohete de Agua', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('trajectory_2d.png', dpi=150)
    
    # --- 2. Gráficas de Serie de Tiempo ---
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    
    # Gráfico 1: Posición X vs Tiempo
    axes[0, 0].plot(df_results['Time'], df_results['X_Position'], color='blue', linewidth=2)
    axes[0, 0].set_ylabel('Posición X (m)')
    axes[0, 0].set_title('Alcance Horizontal vs. Tiempo')
    axes[0, 0].grid(True)
    
    # Gráfico 2: Posición Y vs Tiempo
    axes[0, 1].plot(df_results['Time'], df_results['Y_Position'], color='red', linewidth=2)
    axes[0, 1].set_ylabel('Posición Y (m)')
    axes[0, 1].set_title('Altura vs. Tiempo')
    axes[0, 1].grid(True)
    
    # Gráfico 3: Velocidad Total vs Tiempo
    axes[1, 0].plot(df_results['Time'], df_results['Total_Velocity'], color='purple', linewidth=2)
    axes[1, 0].set_ylabel('Velocidad Total (m/s)')
    axes[1, 0].set_title('Velocidad vs. Tiempo')
    axes[1, 0].grid(True)
    
    # Gráfico 4: Componentes de Velocidad
    axes[1, 1].plot(df_results['Time'], df_results['X_Velocity'], label='Vx', color='blue', linewidth=2)
    axes[1, 1].plot(df_results['Time'], df_results['Y_Velocity'], label='Vy', color='red', linewidth=2)
    axes[1, 1].set_ylabel('Velocidad (m/s)')
    axes[1, 1].set_title('Componentes de Velocidad')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    # Gráfico 5: Presión vs Tiempo
    axes[2, 0].plot(df_results['Time'], df_results['Pressure'] / 1000.0, color='green', linewidth=2)
    axes[2, 0].set_ylabel('Presión (kPa Abs)')
    axes[2, 0].set_xlabel('Tiempo (s)')
    axes[2, 0].set_title('Presión Interna vs. Tiempo')
    axes[2, 0].grid(True)
    
    # Gráfico 6: Masa de Agua vs Tiempo
    axes[2, 1].plot(df_results['Time'], df_results['Water Mass'] * 1000.0, color='orange', linewidth=2)
    axes[2, 1].set_ylabel('Masa de Agua (g)')
    axes[2, 1].set_xlabel('Tiempo (s)')
    axes[2, 1].set_title('Masa de Agua vs. Tiempo')
    axes[2, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('results_series_2d.png', dpi=150)

    # --- 3. Resultados Numéricos Clave ---
    max_height = df_results['Y_Position'].max()
    max_range = df_results['X_Position'].max()
    v_max = df_results['Total_Velocity'].max()
    
    # Tiempo de vaciado
    empty_indices = df_results[df_results['Water Mass'] <= 1e-4]
    t_v = empty_indices['Time'].iloc[0] if not empty_indices.empty else 0.0
    
    t_flight = df_results['Time'].iloc[-1]
    
    print("\n" + "="*70)
    print(" "*20 + "RESULTADOS NUMÉRICOS CLAVE")
    print("="*70)
    print(f"Altura Máxima Alcanzada:          {max_height:.2f} m")
    print(f"Alcance Horizontal Máximo:        {max_range:.2f} m")
    print(f"Velocidad Máxima Alcanzada:       {v_max:.2f} m/s")
    print(f"Tiempo de Vaciado (tv):           {t_v:.3f} s")
    print(f"Tiempo Total de Vuelo:            {t_flight:.2f} s")
    print("="*70)
    
    # Calcular ángulo óptimo teórico (45° en vacío)
    angle_deg = PARAMS['launch_angle_deg']
    print(f"\n💡 Nota: Con {angle_deg:.1f}°, alcance = {max_range:.2f} m")
    print(f"   Para máximo alcance, prueba ángulos cercanos a 45°")
    print("="*70 + "\n")
# -----------------------------------------------------------------------------
