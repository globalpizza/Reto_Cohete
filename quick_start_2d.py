# quick_start_2d.py - Inicio rápido para simulación 2D
# -----------------------------------------------------------------------------
import numpy as np
from utils.parameters import PARAMS
from main_simulation import run_simulation
from visualization import plot_results

print("="*70)
print(" "*15 + "🚀 COHETE DE AGUA - SIMULACIÓN 2D 🚀")
print(" "*10 + "Trayectoria Completa con Ángulo de Lanzamiento")
print("="*70)
print()

# Probar con diferentes ángulos
angles_to_test = [30, 45, 60, 75, 90]

print("📊 COMPARACIÓN DE ÁNGULOS DE LANZAMIENTO:")
print("-"*70)
print(f"{'Ángulo':>8} | {'Altura Máx':>12} | {'Alcance Máx':>12} | {'Velocidad Máx':>14}")
print("-"*70)

results_comparison = []

for angle in angles_to_test:
    # Configurar parámetros
    test_params = PARAMS.copy()
    test_params['launch_angle_deg'] = angle
    test_params['launch_angle_rad'] = np.radians(angle)
    
    # Ejecutar simulación (silenciosa)
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    df = run_simulation(test_params)
    
    sys.stdout = old_stdout
    
    # Extraer resultados
    max_height = df['Y_Position'].max()
    max_range = df['X_Position'].max()
    max_velocity = df['Total_Velocity'].max()
    
    print(f"{angle:>8}° | {max_height:>10.2f} m | {max_range:>10.2f} m | {max_velocity:>12.2f} m/s")
    
    results_comparison.append({
        'angle': angle,
        'height': max_height,
        'range': max_range,
        'velocity': max_velocity
    })

print("-"*70)

# Encontrar el ángulo óptimo para alcance
best_range_idx = max(range(len(results_comparison)), key=lambda i: results_comparison[i]['range'])
best_angle = results_comparison[best_range_idx]['angle']
best_range = results_comparison[best_range_idx]['range']

print(f"\n🎯 ÁNGULO ÓPTIMO PARA MÁXIMO ALCANCE: {best_angle}°")
print(f"   Alcance máximo logrado: {best_range:.2f} m")
print("="*70)

# Ejecutar simulación detallada con el ángulo óptimo
print(f"\n🚀 EJECUTANDO SIMULACIÓN DETALLADA CON {best_angle}°...")
print("-"*70)

optimal_params = PARAMS.copy()
optimal_params['launch_angle_deg'] = best_angle
optimal_params['launch_angle_rad'] = np.radians(best_angle)

df_final = run_simulation(optimal_params)
plot_results(df_final)

print("\n📈 Gráficos generados:")
print("   • trajectory_2d.png       - Trayectoria X vs Y")
print("   • results_series_2d.png   - Series de tiempo completas")
print()
print("="*70)
print("✅ SIMULACIÓN 2D COMPLETADA")
print("="*70)
# -----------------------------------------------------------------------------
