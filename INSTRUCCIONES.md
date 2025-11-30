# 🚀 Simulador de Cohete de Agua - Instrucciones de Uso

## 📋 Descripción General

Este proyecto simula el vuelo de un cohete de agua usando métodos numéricos de integración (Método de Euler) y ecuaciones físicas precisas que incluyen:
- Expansión adiabática del aire comprimido
- Ecuación de Bernoulli completa para la velocidad de escape
- Fuerzas de arrastre aerodinámico
- Fases de vuelo (tubo de lanzamiento, expulsión de agua, aire residual, balística)

## 🔧 Instalación y Configuración

### 1. Verificar el Entorno Virtual
Ya tienes un entorno virtual configurado en `.venv/`. Las dependencias necesarias ya están instaladas:
- `numpy` - Cálculos numéricos
- `pandas` - Manejo de datos
- `matplotlib` - Visualización de resultados

### 2. Activar el entorno (opcional)
Si deseas activar el entorno virtual manualmente:
```powershell
.\.venv\Scripts\Activate.ps1
```

## 🚀 Cómo Ejecutar la Simulación

### Opción 1: Simulación Básica
Ejecuta la simulación con los parámetros predeterminados:
```powershell
& "C:/Users/santi/OneDrive/Documentos/San/Universidad/Semestre 1 - 2025/S3 - Periodo 3 - 2025/Modelación matemática fundamental/Tareas/Reto_Cohete/.venv/Scripts/python.exe" main_simulation.py
```

O simplemente (si el entorno está activado):
```powershell
python main_simulation.py
```

### Opción 2: Suite de Pruebas Completa
Para verificar que todo funciona correctamente y ver diferentes escenarios:
```powershell
python test_simulation.py
```

Esta suite ejecuta 4 pruebas:
1. ✅ Parámetros predeterminados
2. ✅ Variación de volumen de agua (0.3L, 0.5L, 0.7L, 1.0L)
3. ✅ Variación de presión inicial (40, 60, 80, 100 psi)
4. ✅ Verificación de consistencia física

## 📊 Resultados Generados

Después de ejecutar la simulación, se generan automáticamente:

### 1. Archivos de Gráficos (PNG)
- **`results_series.png`**: Contiene 3 subgráficos:
  - Velocidad vs. Tiempo (comparación con aproximación de Tsiolkovsky)
  - Presión interna vs. Tiempo
  - Masa de agua vs. Tiempo

- **`trajectory.png`**: Trayectoria vertical mostrando las diferentes fases del vuelo

### 2. Salida en Consola
Muestra información clave:
```
Velocidad inicial v_i (al salir del tubo): XX.XX m/s
Velocidad Máxima Alcanzada: XX.XX m/s
Altura Máxima Alcanzada: XX.XX m
Tiempo de Vaciado (tv): X.XXX s
Tiempo Total de Vuelo: X.XX s
```

## ⚙️ Personalizar Parámetros

### Método 1: Editar `utils/parameters.py`
Abre el archivo y modifica los valores en el diccionario `PARAMS`:

```python
PARAMS = {
    'p_manometric_psi': 70.0,    # Presión inicial (psi)
    'V_r_L': 2.0,                # Volumen total de la botella (L)
    'V_0w_L': 0.5,               # Volumen inicial de agua (L)
    'A_e_cm2': 4.5,              # Área de la boquilla (cm²)
    'A_r_cm2': 95.0,             # Área transversal de la botella (cm²)
    'M_r_g': 55.0,               # Masa seca del cohete (g)
    'H_tube_m': 1.0,             # Altura del tubo de lanzamiento (m)
    'C_D': 0.75,                 # Coeficiente de arrastre
    'A_ref_cm2': 100.0,          # Área de referencia para arrastre (cm²)
}
```

### Método 2: Crear un Script Personalizado
Crea un nuevo archivo Python:

```python
from utils.parameters import PARAMS, convert_to_si
from main_simulation import run_simulation
from visualization import plot_results

# Copiar y modificar parámetros
my_params = PARAMS.copy()
my_params['p_manometric_psi'] = 100.0  # Mayor presión
my_params['V_0w_L'] = 0.8              # Más agua
my_params = convert_to_si(my_params)

# Ejecutar simulación
df = run_simulation(my_params)
plot_results(df)
```

## 📁 Estructura del Proyecto

```
Reto_Cohete/
├── main_simulation.py          # Orquestador principal
├── test_simulation.py          # Suite de pruebas
├── visualization.py            # Generación de gráficos
├── utils/
│   ├── parameters.py          # Parámetros y constantes
│   └── euler.py               # Método de integración numérica
├── physics/
│   ├── water_phase.py         # Cálculos de presión y velocidad de escape
│   └── derivatives.py         # Ecuaciones diferenciales del sistema
└── .venv/                     # Entorno virtual Python
```

## 🔬 Fases de la Simulación

1. **Launch Tube (Tubo de Lanzamiento)**: El cohete acelera mientras está en el tubo guía
2. **Water (Expulsión de Agua)**: Fase principal de empuje por expulsión de agua
3. **Air (Aire Residual)**: Pequeño empuje adicional por el aire comprimido remanente
4. **Ballistic (Balística)**: Vuelo libre bajo gravedad y arrastre hasta impacto

## 📈 Interpretación de Resultados

### Valores Típicos Esperados
Con los parámetros predeterminados (70 psi, 0.5L agua):
- **Velocidad máxima**: ~58 m/s
- **Altura máxima**: ~21 m
- **Tiempo de vaciado**: ~0.04 s
- **Tiempo de vuelo total**: ~4.3 s

### Optimización
Para maximizar la altura:
- Existe un **volumen óptimo de agua** (~25-40% del volumen total)
- Mayor presión inicial generalmente aumenta el rendimiento
- El área de la boquilla afecta el tiempo de vaciado y la velocidad de escape

## ⚠️ Notas Importantes

1. **Precisión Numérica**: 
   - El paso de tiempo (`DT = 0.001 s`) es fijo y pequeño para mayor precisión
   - Para simulaciones más rápidas (menos precisas), puedes aumentar `DT` en `parameters.py`

2. **Limitaciones del Modelo**:
   - No incluye efectos de rotación
   - Asume trayectoria vertical perfecta
   - El arrastre usa un coeficiente constante
   - No modela el empuje residual del aire detalladamente

3. **Validación Física**:
   - La energía cinética puede exceder la energía de presión inicial debido a la energía potencial gravitacional del agua
   - La simulación incluye todas las fuerzas relevantes (empuje, gravedad, arrastre)

## 🧪 Experimentos Sugeridos

1. **Búsqueda del Volumen Óptimo**:
   - Varía `V_0w_L` de 0.2L a 1.5L en incrementos de 0.1L
   - Grafica altura máxima vs. volumen de agua

2. **Efecto de la Presión**:
   - Compara diferentes presiones iniciales (30, 50, 70, 90 psi)
   - Analiza la relación presión-altura

3. **Diseño de Boquilla**:
   - Modifica `A_e_cm2` para ver el efecto del diámetro de salida
   - Encuentra el área óptima para tu configuración

## 📞 Solución de Problemas

### Error: "Module not found"
```powershell
# Reinstalar dependencias
python -m pip install numpy pandas matplotlib
```

### La simulación tarda demasiado
- Aumenta `DT` en `utils/parameters.py` (ej: `DT = 0.01`)
- Reduce el límite de tiempo en `main_simulation.py` si es necesario

### Las gráficas no se muestran
- Las gráficas se guardan automáticamente como archivos PNG
- Para visualizarlas, abre `results_series.png` y `trajectory.png`
- Si quieres que se muestren en pantalla, descomenta `plt.show()` en `visualization.py`

## 📚 Referencias Físicas

El modelo se basa en:
1. Expansión adiabática de gases ideales: `P * V^γ = constante`
2. Ecuación de Bernoulli con términos de presión y gravedad
3. Ecuación de Tsiolkovsky para cohetes
4. Arrastre aerodinámico cuadrático: `F_D = 0.5 * ρ * v² * C_D * A`

---

**¡Disfruta experimentando con tu cohete de agua virtual! 🚀💧**
