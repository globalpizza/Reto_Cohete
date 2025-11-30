# demo_interactive.py - Demostración Interactiva del Simulador de Cohete
# -----------------------------------------------------------------------------
"""
Script interactivo para explorar diferentes configuraciones del cohete de agua.
Permite al usuario modificar parámetros y ver los resultados inmediatamente.
"""

import numpy as np
import pandas as pd
from utils.parameters import PARAMS, convert_to_si
from main_simulation import run_simulation
from visualization import plot_results

def print_header():
    """Imprime el encabezado del programa."""
    print("\n" + "="*70)
    print(" "*15 + "🚀 SIMULADOR DE COHETE DE AGUA 🚀")
    print("="*70)

def print_menu():
    """Muestra el menú principal."""
    print("\n📋 MENÚ PRINCIPAL:")
    print("-" * 70)
    print("1. Ejecutar simulación con parámetros actuales")
    print("2. Modificar presión inicial")
    print("3. Modificar volumen de agua")
    print("4. Modificar área de boquilla")
    print("5. Ejecutar análisis de optimización (volumen de agua)")
    print("6. Comparar diferentes presiones")
    print("7. Ver parámetros actuales")
    print("8. Restaurar parámetros predeterminados")
    print("0. Salir")
    print("-" * 70)

def show_current_params(params):
    """Muestra los parámetros actuales."""
    print("\n⚙️  PARÁMETROS ACTUALES:")
    print("-" * 70)
    print(f"Presión inicial:        {params['p_manometric_psi']:.1f} psi")
    print(f"Volumen de botella:     {params['V_r_L']:.2f} L")
    print(f"Volumen de agua:        {params['V_0w_L']:.2f} L ({params['V_0w_L']/params['V_r_L']*100:.1f}% de llenado)")
    print(f"Área de boquilla:       {params['A_e_cm2']:.2f} cm²")
    print(f"Área de botella:        {params['A_r_cm2']:.2f} cm²")
    print(f"Masa seca:              {params['M_r_g']:.1f} g")
    print(f"Altura del tubo:        {params['H_tube_m']:.2f} m")
    print(f"Coef. de arrastre:      {params['C_D']:.2f}")
    print(f"Área de referencia:     {params['A_ref_cm2']:.2f} cm²")
    print("-" * 70)

def run_single_simulation(params):
    """Ejecuta una simulación individual."""
    print("\n🚀 Ejecutando simulación...")
    print("-" * 70)
    
    params_si = convert_to_si(params.copy())
    df = run_simulation(params_si)
    
    max_height = df['Position'].max()
    max_velocity = df['Velocity'].max()
    flight_time = df['Time'].iloc[-1]
    
    # Calcular tiempo de vaciado
    empty_indices = df[df['Water Mass'] <= 1e-4]
    t_empty = empty_indices['Time'].iloc[0] if not empty_indices.empty else 0.0
    
    print("\n📊 RESULTADOS:")
    print("-" * 70)
    print(f"✓ Altura máxima:        {max_height:.2f} m")
    print(f"✓ Velocidad máxima:     {max_velocity:.2f} m/s")
    print(f"✓ Tiempo de vaciado:    {t_empty:.3f} s")
    print(f"✓ Tiempo de vuelo:      {flight_time:.2f} s")
    print("-" * 70)
    print("\n📈 Gráficos generados: 'results_series.png' y 'trajectory.png'")
    
    plot_results(df)
    
    input("\nPresiona Enter para continuar...")

def modify_pressure(params):
    """Permite modificar la presión inicial."""
    print(f"\n🔧 Presión actual: {params['p_manometric_psi']:.1f} psi")
    print("Rango típico: 30-100 psi")
    
    try:
        new_pressure = float(input("Ingresa nueva presión (psi): "))
        if 10 <= new_pressure <= 150:
            params['p_manometric_psi'] = new_pressure
            print(f"✓ Presión actualizada a {new_pressure:.1f} psi")
        else:
            print("⚠️  Advertencia: Presión fuera del rango típico (30-100 psi)")
            confirm = input("¿Continuar de todos modos? (s/n): ")
            if confirm.lower() == 's':
                params['p_manometric_psi'] = new_pressure
                print(f"✓ Presión actualizada a {new_pressure:.1f} psi")
    except ValueError:
        print("❌ Valor inválido. No se modificó la presión.")
    
    input("\nPresiona Enter para continuar...")

def modify_water_volume(params):
    """Permite modificar el volumen de agua."""
    print(f"\n🔧 Volumen de agua actual: {params['V_0w_L']:.2f} L")
    print(f"Volumen máximo (botella): {params['V_r_L']:.2f} L")
    
    try:
        new_volume = float(input("Ingresa nuevo volumen de agua (L): "))
        if 0 < new_volume < params['V_r_L']:
            params['V_0w_L'] = new_volume
            print(f"✓ Volumen actualizado a {new_volume:.2f} L ({new_volume/params['V_r_L']*100:.1f}% de llenado)")
        else:
            print(f"❌ Error: El volumen debe estar entre 0 y {params['V_r_L']:.2f} L")
    except ValueError:
        print("❌ Valor inválido. No se modificó el volumen.")
    
    input("\nPresiona Enter para continuar...")

def modify_nozzle_area(params):
    """Permite modificar el área de la boquilla."""
    print(f"\n🔧 Área de boquilla actual: {params['A_e_cm2']:.2f} cm²")
    print("Rango típico: 2-10 cm²")
    
    try:
        new_area = float(input("Ingresa nueva área de boquilla (cm²): "))
        if new_area > 0:
            params['A_e_cm2'] = new_area
            print(f"✓ Área actualizada a {new_area:.2f} cm²")
        else:
            print("❌ Error: El área debe ser positiva")
    except ValueError:
        print("❌ Valor inválido. No se modificó el área.")
    
    input("\nPresiona Enter para continuar...")

def optimize_water_volume(params):
    """Encuentra el volumen óptimo de agua."""
    print("\n🔬 ANÁLISIS DE OPTIMIZACIÓN - VOLUMEN DE AGUA")
    print("-" * 70)
    print("Probando diferentes volúmenes de agua...")
    
    volumes = np.linspace(0.2, params['V_r_L'] * 0.95, 15)
    results = []
    
    for i, vol in enumerate(volumes):
        test_params = params.copy()
        test_params['V_0w_L'] = vol
        test_params_si = convert_to_si(test_params)
        
        df = run_simulation(test_params_si)
        max_height = df['Position'].max()
        
        results.append({
            'Volumen (L)': vol,
            'Altura (m)': max_height,
            '% Llenado': vol/params['V_r_L']*100
        })
        
        # Barra de progreso simple
        progress = (i + 1) / len(volumes) * 100
        print(f"Progreso: {progress:.0f}% - V={vol:.2f}L → h={max_height:.2f}m")
    
    df_results = pd.DataFrame(results)
    
    # Encontrar el óptimo
    optimal_idx = df_results['Altura (m)'].idxmax()
    optimal = df_results.iloc[optimal_idx]
    
    print("\n" + "="*70)
    print("📊 RESULTADOS DEL ANÁLISIS:")
    print("="*70)
    print(df_results.to_string(index=False))
    print("\n" + "="*70)
    print("🏆 CONFIGURACIÓN ÓPTIMA ENCONTRADA:")
    print("="*70)
    print(f"Volumen de agua óptimo: {optimal['Volumen (L)']:.2f} L ({optimal['% Llenado']:.1f}% de llenado)")
    print(f"Altura máxima alcanzada: {optimal['Altura (m)']:.2f} m")
    print("="*70)
    
    apply = input("\n¿Aplicar esta configuración? (s/n): ")
    if apply.lower() == 's':
        params['V_0w_L'] = optimal['Volumen (L)']
        print(f"✓ Configuración actualizada a {optimal['Volumen (L)']:.2f} L")
    
    input("\nPresiona Enter para continuar...")

def compare_pressures(params):
    """Compara diferentes presiones iniciales."""
    print("\n🔬 COMPARACIÓN DE PRESIONES")
    print("-" * 70)
    
    pressures = [40, 60, 80, 100]
    results = []
    
    for pressure in pressures:
        test_params = params.copy()
        test_params['p_manometric_psi'] = pressure
        test_params_si = convert_to_si(test_params)
        
        df = run_simulation(test_params_si)
        max_height = df['Position'].max()
        max_velocity = df['Velocity'].max()
        
        results.append({
            'Presión (psi)': pressure,
            'Altura (m)': max_height,
            'Velocidad (m/s)': max_velocity
        })
        
        print(f"✓ Probado: {pressure} psi → {max_height:.2f} m")
    
    df_results = pd.DataFrame(results)
    
    print("\n" + "="*70)
    print("📊 TABLA COMPARATIVA:")
    print("="*70)
    print(df_results.to_string(index=False))
    print("="*70)
    
    input("\nPresiona Enter para continuar...")

def reset_params():
    """Restaura los parámetros predeterminados."""
    default_params = {
        'p_manometric_psi': 70.0,
        'V_r_L': 2.0,
        'V_0w_L': 0.5,
        'A_e_cm2': 4.5,
        'A_r_cm2': 95.0,
        'M_r_g': 55.0,
        'H_tube_m': 1.0,
        'C_D': 0.75,
        'A_ref_cm2': 100.0,
    }
    print("\n✓ Parámetros restaurados a valores predeterminados")
    input("\nPresiona Enter para continuar...")
    return default_params

def main():
    """Función principal del programa interactivo."""
    print_header()
    
    # Inicializar con parámetros predeterminados
    current_params = PARAMS.copy()
    
    while True:
        print_menu()
        
        try:
            choice = input("\nSelecciona una opción (0-8): ").strip()
            
            if choice == '0':
                print("\n👋 ¡Gracias por usar el Simulador de Cohete de Agua!")
                print("="*70)
                break
            
            elif choice == '1':
                run_single_simulation(current_params)
            
            elif choice == '2':
                modify_pressure(current_params)
            
            elif choice == '3':
                modify_water_volume(current_params)
            
            elif choice == '4':
                modify_nozzle_area(current_params)
            
            elif choice == '5':
                optimize_water_volume(current_params)
            
            elif choice == '6':
                compare_pressures(current_params)
            
            elif choice == '7':
                show_current_params(current_params)
                input("\nPresiona Enter para continuar...")
            
            elif choice == '8':
                current_params = reset_params()
            
            else:
                print("\n❌ Opción inválida. Por favor selecciona 0-8.")
                input("\nPresiona Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------
