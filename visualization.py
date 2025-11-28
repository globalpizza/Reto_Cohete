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
    """Genera las gráficas de V, P, M, y la Trayectoria (conceptual 3D)."""
    
    # --- Cálculo de u_e Promedio para Tsiolkovsky (Aproximación Pedagógica) ---
    # Para el cálculo de la aproximación 2, necesitamos un u_e promedio o constante.
    # El cálculo de u_e inicial es suficiente para esta comparación pedagógica simple.
    P_i = PARAMS['P_i_abs']
    A_r = PARAMS['A_r']
    A_e = PARAMS['A_e']
    
    # u_e constante de la Aprox. 2 (Presión constante) [1]
    # Nota: Si P_i es muy bajo, esto podría dar error, pero asumimos condiciones normales.
    term_p = 2 * A_r**2 * (P_i - P_ATM) / (RHO_W * (A_r**2 - A_e**2))
    if term_p < 0: term_p = 0
    u_e_approx = np.sqrt(term_p)
    
    t_approx, v_approx_tsiol = calculate_approx_tsiolkovsky(df_results, u_e_approx)

    
    # --- 1. Gráficas de Serie de Tiempo (2D) ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Gráfico 1: Velocidad vs. Tiempo (Comparación Pedagógica)
    axes[0].plot(df_results['Time'], df_results['Velocity'], label='Velocidad Exacta (Euler, Fd+g)', color='blue', linewidth=2)
    if len(t_approx) > 0:
        axes[0].plot(t_approx, v_approx_tsiol, label='Aproximación 2 (Tsiolkovsky, P constante)', color='red', linestyle='--', linewidth=1.5)
    axes[0].set_ylabel('Velocidad (m/s)')
    axes[0].set_title('Velocidad del Cohete vs. Tiempo (Comparación Modelos)')
    axes[0].grid(True)
    axes[0].legend()
    
    # Gráfico 2: Presión vs. Tiempo
    axes[1].plot(df_results['Time'], df_results['Pressure'] / 1000.0, label='Presión (Adiabática)', color='green')
    axes[1].set_ylabel('Presión (kPa Abs)')
    axes[1].set_title('Presión Interna de Aire vs. Tiempo')
    axes[1].grid(True)
    
    # Gráfico 3: Masa de Agua vs. Tiempo
    axes[2].plot(df_results['Time'], df_results['Water Mass'] * 1000.0, label='Masa de Agua', color='orange')
    axes[2].set_ylabel('Masa de Agua (g)')
    axes[2].set_xlabel('Tiempo (s)')
    axes[2].set_title('Masa de Agua Expulsada vs. Tiempo')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('results_series.png')
    # plt.show()
    
    # --- 2. Gráfico Conceptual de Trayectoria (3D/2D vertical) ---
    # Simulación conceptual de la altura para visualizar fases
    plt.figure(figsize=(8, 6))
    
    colors = {'Launch Tube': 'purple', 'Water': 'blue', 'Air': 'red', 'Ballistic': 'gray'}
    for phase, group in df_results.groupby('Phase'):
        plt.plot(group['Time'], group['Position'], label=phase, color=colors.get(phase, 'black'), linewidth=2)

    plt.axhline(y=0, color='k', linestyle='-')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura (m)')
    plt.title('Trayectoria Vertical del Cohete por Fases')
    plt.legend()
    plt.grid(True)
    plt.savefig('trajectory.png')
    # plt.show()

    # --- 3. Resultados Numéricos Clave ---
    v_max = df_results['Velocity'].max()
    h_max = df_results['Position'].max()
    
    # Tiempo de vaciado: cuando la masa de agua llega a ~0
    # Buscamos el primer instante donde Phase cambia de Water a Air o Ballistic, o Water Mass es 0
    empty_indices = df_results[df_results['Water Mass'] <= 1e-4]
    t_v = empty_indices['Time'].iloc[0] if not empty_indices.empty else 0.0
    
    t_flight = df_results['Time'].iloc[-1]
    
    print("\n--- RESULTADOS NUMÉRICOS CLAVE ---")
    print(f"Velocidad Máxima Alcanzada: {v_max:.2f} m/s")
    print(f"Altura Máxima Alcanzada: {h_max:.2f} m")
    print(f"Tiempo de Vaciado (tv): {t_v:.3f} s")
    print(f"Tiempo Total de Vuelo: {t_flight:.2f} s")
# -----------------------------------------------------------------------------
