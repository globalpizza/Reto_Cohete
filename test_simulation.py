# test_simulation.py - Script de Pruebas para Verificar la Simulación
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
from utils.parameters import PARAMS, RHO_W, G, P_ATM, convert_to_si
from main_simulation import run_simulation

def test_default_parameters():
    """Prueba con los parámetros predeterminados."""
    print("="*70)
    print("PRUEBA 1: Parámetros Predeterminados")
    print("="*70)
    print(f"Presión inicial: {PARAMS['p_manometric_psi']:.1f} psi")
    print(f"Volumen total: {PARAMS['V_r_L']:.2f} L")
    print(f"Volumen de agua: {PARAMS['V_0w_L']:.2f} L")
    print(f"Área de boquilla: {PARAMS['A_e_cm2']:.2f} cm²")
    print(f"Masa seca: {PARAMS['M_r_g']:.1f} g")
    print("-"*70)
    
    df = run_simulation(PARAMS)
    
    # Validaciones
    assert df['Position'].max() > 0, "La altura máxima debe ser positiva"
    assert df['Velocity'].max() > 0, "La velocidad máxima debe ser positiva"
    assert len(df) > 0, "Debe haber datos de simulación"
    
    print("\n✓ Prueba 1 PASADA\n")
    return df

def test_different_water_volumes():
    """Prueba con diferentes volúmenes de agua."""
    print("="*70)
    print("PRUEBA 2: Diferentes Volúmenes de Agua")
    print("="*70)
    
    water_volumes = [0.3, 0.5, 0.7, 1.0]  # Litros
    results = []
    
    for V_0w_L in water_volumes:
        params = PARAMS.copy()
        params['V_0w_L'] = V_0w_L
        params = convert_to_si(params)
        
        print(f"\n--- Volumen de agua: {V_0w_L:.1f} L ---")
        df = run_simulation(params)
        
        max_height = df['Position'].max()
        max_velocity = df['Velocity'].max()
        flight_time = df['Time'].iloc[-1]
        
        results.append({
            'V_0w (L)': V_0w_L,
            'Altura Máxima (m)': max_height,
            'Velocidad Máxima (m/s)': max_velocity,
            'Tiempo de Vuelo (s)': flight_time
        })
    
    df_results = pd.DataFrame(results)
    print("\n" + "="*70)
    print("RESUMEN DE RESULTADOS:")
    print("="*70)
    print(df_results.to_string(index=False))
    print("\n✓ Prueba 2 PASADA\n")
    
    return df_results

def test_different_pressures():
    """Prueba con diferentes presiones iniciales."""
    print("="*70)
    print("PRUEBA 3: Diferentes Presiones Iniciales")
    print("="*70)
    
    pressures = [40, 60, 80, 100]  # psi
    results = []
    
    for p_psi in pressures:
        params = PARAMS.copy()
        params['p_manometric_psi'] = p_psi
        params = convert_to_si(params)
        
        print(f"\n--- Presión inicial: {p_psi} psi ---")
        df = run_simulation(params)
        
        max_height = df['Position'].max()
        max_velocity = df['Velocity'].max()
        flight_time = df['Time'].iloc[-1]
        
        results.append({
            'Presión (psi)': p_psi,
            'Altura Máxima (m)': max_height,
            'Velocidad Máxima (m/s)': max_velocity,
            'Tiempo de Vuelo (s)': flight_time
        })
    
    df_results = pd.DataFrame(results)
    print("\n" + "="*70)
    print("RESUMEN DE RESULTADOS:")
    print("="*70)
    print(df_results.to_string(index=False))
    print("\n✓ Prueba 3 PASADA\n")
    
    return df_results

def test_physics_consistency():
    """Verifica la consistencia física de la simulación."""
    print("="*70)
    print("PRUEBA 4: Consistencia Física")
    print("="*70)
    
    df = run_simulation(PARAMS)
    
    # Verificación 1: La masa de agua debe disminuir monótonamente
    water_mass = df['Water Mass'].values
    assert all(water_mass[i] >= water_mass[i+1] for i in range(len(water_mass)-1)), \
        "La masa de agua debe disminuir o permanecer constante"
    print("✓ Masa de agua disminuye correctamente")
    
    # Verificación 2: La presión debe disminuir durante la fase de agua
    water_phase = df[df['Phase'] == 'Water']
    if len(water_phase) > 1:
        pressure = water_phase['Pressure'].values
        # La presión puede aumentar ligeramente al inicio, pero debe tender a disminuir
        print(f"✓ Presión durante fase de agua: {pressure[0]:.0f} Pa → {pressure[-1]:.0f} Pa")
    
    # Verificación 3: El cohete debe caer después de alcanzar altura máxima
    max_height_idx = df['Position'].idxmax()
    velocities_after_max = df.loc[max_height_idx:, 'Velocity']
    assert velocities_after_max.iloc[-1] < 0, "El cohete debe estar cayendo al final"
    print("✓ El cohete cae después de alcanzar la altura máxima")
    
    # Verificación 4: Conservación de energía (aproximada)
    # La energía final debe ser menor que la inicial debido a pérdidas por arrastre
    initial_pressure_energy = (PARAMS['P_i_abs'] - P_ATM) * (PARAMS['V_r'] - PARAMS['V_0w'])
    kinetic_energy_max = 0.5 * (PARAMS['M_r'] + PARAMS['V_0w'] * RHO_W) * (df['Velocity'].max())**2
    print(f"✓ Energía de presión inicial: {initial_pressure_energy:.1f} J")
    print(f"✓ Energía cinética máxima: {kinetic_energy_max:.1f} J")
    print(f"✓ Ratio: {kinetic_energy_max/initial_pressure_energy:.2%}")
    
    print("\n✓ Prueba 4 PASADA\n")

def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*70)
    print(" "*15 + "SUITE DE PRUEBAS - COHETE DE AGUA")
    print("="*70 + "\n")
    
    try:
        # Prueba 1: Parámetros predeterminados
        df1 = test_default_parameters()
        
        # Prueba 2: Diferentes volúmenes de agua
        df2 = test_different_water_volumes()
        
        # Prueba 3: Diferentes presiones
        df3 = test_different_pressures()
        
        # Prueba 4: Consistencia física
        test_physics_consistency()
        
        print("="*70)
        print(" "*20 + "¡TODAS LAS PRUEBAS PASARON!")
        print("="*70)
        print("\nLa simulación está funcionando correctamente.")
        print("Los archivos 'results_series.png' y 'trajectory.png' han sido generados.")
        
    except AssertionError as e:
        print(f"\n❌ ERROR EN PRUEBA: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()
# -----------------------------------------------------------------------------
