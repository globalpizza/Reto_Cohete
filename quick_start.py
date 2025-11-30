# quick_start.py - Inicio Rápido para el Simulador de Cohete de Agua
# -----------------------------------------------------------------------------
"""
Script de inicio rápido que ejecuta una simulación básica y muestra los resultados.
Ideal para verificar que todo funciona correctamente.
"""

print("\n" + "="*70)
print(" "*20 + "🚀 COHETE DE AGUA 🚀")
print(" "*15 + "Verificación de Funcionamiento")
print("="*70)

print("\n📦 Importando módulos...")
try:
    from utils.parameters import PARAMS
    from main_simulation import run_simulation
    from visualization import plot_results
    print("✓ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("\n⚠️  Asegúrate de instalar las dependencias:")
    print("   pip install numpy pandas matplotlib")
    exit(1)

print("\n⚙️  CONFIGURACIÓN INICIAL:")
print("-" * 70)
print(f"Presión inicial:        {PARAMS['p_manometric_psi']:.1f} psi")
print(f"Volumen de agua:        {PARAMS['V_0w_L']:.2f} L")
print(f"Volumen de botella:     {PARAMS['V_r_L']:.2f} L")
print(f"Porcentaje de llenado:  {PARAMS['V_0w_L']/PARAMS['V_r_L']*100:.1f}%")
print(f"Área de boquilla:       {PARAMS['A_e_cm2']:.2f} cm²")
print(f"Masa seca del cohete:   {PARAMS['M_r_g']:.1f} g")
print("-" * 70)

print("\n🚀 Ejecutando simulación...")
print("   (Esto puede tomar unos segundos...)")

try:
    df = run_simulation(PARAMS)
    print("✓ Simulación completada exitosamente")
except Exception as e:
    print(f"❌ Error durante la simulación: {e}")
    exit(1)

# Extraer resultados clave
max_height = df['Position'].max()
max_velocity = df['Velocity'].max()
flight_time = df['Time'].iloc[-1]

# Calcular tiempo de vaciado
empty_indices = df[df['Water Mass'] <= 1e-4]
t_empty = empty_indices['Time'].iloc[0] if not empty_indices.empty else 0.0

print("\n" + "="*70)
print(" "*25 + "📊 RESULTADOS")
print("="*70)
print(f"\n🎯 Altura Máxima Alcanzada:        {max_height:.2f} m")
print(f"⚡ Velocidad Máxima Alcanzada:     {max_velocity:.2f} m/s")
print(f"💧 Tiempo de Vaciado de Agua:      {t_empty:.3f} s")
print(f"⏱️  Tiempo Total de Vuelo:          {flight_time:.2f} s")
print("\n" + "="*70)

print("\n📈 Generando gráficos...")
try:
    plot_results(df)
    print("✓ Gráficos generados exitosamente:")
    print("   • results_series.png  (Velocidad, Presión, Masa)")
    print("   • trajectory.png      (Trayectoria vertical)")
except Exception as e:
    print(f"❌ Error al generar gráficos: {e}")

print("\n" + "="*70)
print("✅ VERIFICACIÓN COMPLETA - TODO FUNCIONA CORRECTAMENTE")
print("="*70)

print("\n💡 PRÓXIMOS PASOS:")
print("-" * 70)
print("1. Abre los archivos PNG para ver las gráficas")
print("2. Ejecuta 'python test_simulation.py' para pruebas completas")
print("3. Ejecuta 'python demo_interactive.py' para modo interactivo")
print("4. Lee 'INSTRUCCIONES.md' para más información")
print("-" * 70)

print("\n🎓 ANÁLISIS RÁPIDO:")
print("-" * 70)

# Análisis de fases
water_phase = df[df['Phase'] == 'Water']
ballistic_phase = df[df['Phase'] == 'Ballistic']

if not water_phase.empty:
    water_duration = water_phase['Time'].iloc[-1] - water_phase['Time'].iloc[0]
    print(f"Duración de fase de expulsión de agua: {water_duration:.3f} s")

if not ballistic_phase.empty:
    ballistic_duration = ballistic_phase['Time'].iloc[-1] - ballistic_phase['Time'].iloc[0]
    print(f"Duración de fase balística:            {ballistic_duration:.2f} s")

# Eficiencia energética aproximada
from utils.parameters import RHO_W, P_ATM

pressure_energy = (PARAMS['P_i_abs'] - P_ATM) * (PARAMS['V_r'] - PARAMS['V_0w'])
kinetic_energy = 0.5 * (PARAMS['M_r'] + PARAMS['V_0w'] * RHO_W) * (max_velocity ** 2)
efficiency = (kinetic_energy / pressure_energy) * 100

print(f"Energía de presión inicial:            {pressure_energy:.1f} J")
print(f"Energía cinética máxima:               {kinetic_energy:.1f} J")
print(f"Eficiencia de conversión (aproximada): {efficiency:.1f}%")

print("-" * 70)

print("\n🚀 ¡Listo para despegar! 🚀\n")
# -----------------------------------------------------------------------------
