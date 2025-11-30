# 🚀 Cambios Realizados: Actualización a Simulación 2D

## 📋 Resumen de Cambios

Se ha actualizado completamente el proyecto de simulación de cohete de agua para incluir **trayectorias bidimensionales (2D)** con **ángulo de lanzamiento ajustable**. Esto permite:

✅ **Calcular alcance horizontal** (no solo altura vertical)  
✅ **Optimizar el ángulo de lanzamiento** para máximo alcance  
✅ **Visualizar trayectorias parabólicas** realistas  
✅ **Comparar diferentes configuraciones** de lanzamiento  

---

## 🔧 Archivos Modificados

### 1. **Python - Simulación Core**

#### `utils/parameters.py`
- ✨ **Nuevo parámetro**: `launch_angle_deg = 45.0` (ángulo de lanzamiento en grados)
- ✨ **Conversión automática**: `launch_angle_rad` calculado en radianes

#### `physics/derivatives.py`
- 🔄 **Función completamente reescrita** para 2D
- **Antes**: `derivatives([y, v, M_w])` → `[dy/dt, dv/dt, dMw/dt]`
- **Ahora**: `derivatives([x, y, vx, vy, M_w])` → `[dx/dt, dy/dt, dvx/dt, dvy/dt, dMw/dt]`
- ✨ Nueva función: `calculate_drag_2d(vx, vy)` retorna `(F_Dx, F_Dy)`
- ✨ Empuje descompuesto en componentes X e Y basados en:
  - Dirección de velocidad cuando está en movimiento
  - Ángulo de lanzamiento al inicio

#### `main_simulation.py`
- 🔄 **Estado inicial**: `Y_n = [0, 0, 0, 0, M_0w]` (x, y, vx, vy, agua)
- ✨ **Nuevas columnas** en resultados:
  - `X_Position` (m)
  - `Y_Position` (m) 
  - `X_Velocity` (m/s)
  - `Y_Velocity` (m/s)
  - `Total_Velocity` (m/s)
- ✨ **Nuevas métricas**:
  - Altura máxima alcanzada
  - **Alcance horizontal máximo** ⭐
- 🔄 **Criterio de terminación**: `y <= 0` después de alcanzar altura máxima

#### `visualization.py`
- 🔄 **Función completamente reescrita** para visualización 2D
- ✨ **Nuevo gráfico**: `trajectory_2d.png` - Trayectoria X vs Y con código de color por fase
- 🔄 **Gráfico actualizado**: `results_series_2d.png` - 6 subplots:
  1. Posición X vs tiempo
  2. Posición Y vs tiempo
  3. Velocidad total vs tiempo
  4. Velocidades vx y vy vs tiempo
  5. Presión interna vs tiempo
  6. Masa de agua vs tiempo
- ✨ Muestra tanto altura máxima como alcance máximo
- 📝 Nota educativa sobre ángulo óptimo de 45° (sin fricción)

#### `quick_start_2d.py` ⭐ NUEVO
- 🆕 Script de comparación de ángulos
- Prueba automáticamente: 30°, 45°, 60°, 75°, 90°
- Muestra tabla comparativa de:
  - Altura máxima
  - Alcance máximo
  - Velocidad máxima
- **Encuentra automáticamente el ángulo óptimo** para máximo alcance
- Genera visualizaciones detalladas del mejor caso

---

### 2. **JavaScript - Aplicación Web**

#### `web_app/simulation.js`
- 🔄 **Clase RocketSimulation completamente actualizada**
- ✨ `convertToSI()`: Ahora incluye conversión de `launch_angle_deg` a radianes
- 🔄 **Estado**: `{x, y, vx, vy, M_w, t, phase}` (5 elementos)
- ✨ `calculateDrag()` → `calculateDrag(vx, vy)` retorna `{F_Dx, F_Dy}`
- 🔄 `derivatives()`: Calcula derivadas en 2D
  - Empuje en X e Y
  - Arrastre en X e Y
  - Gravedad solo en Y
- 🔄 `step()`: Integra las 5 variables de estado
- ✨ Tracking de `maxHeightReached` para terminación correcta

#### `web_app/index.html`
- ✨ **Nuevo control**: Slider de ángulo de lanzamiento (0° - 90°)
  ```html
  <input type="range" id="launch_angle" min="0" max="90" value="45" step="5">
  ```
- ✨ **Nueva estadística**: Max Alcance (m)
  ```html
  <p>Max Alcance: <span id="max-range">0.0</span> m</p>
  ```

#### `web_app/main.js`
- ✨ Agregado `launch_angle` a inputs y displays
- ✨ Agregado `maxR` (max range) a tracking de estado
- 🔄 `updateDisplay()`: Maneja sufijo "°" para ángulo
- 🔄 `getParams()`: Incluye `launch_angle_deg`
- 🔄 `resetSimulation()`: Reinicia `maxR = 0`
- 🔄 `loop()`: 
  - Calcula velocidad total: `sqrt(vx² + vy²)`
  - Trackea `maxR = max(x)`
  - Actualiza display de alcance
- 🔄 `draw()`: **Visualización 2D completa**
  - Trayectoria mostrada en X e Y
  - Trail de trayectoria (línea azul)
  - Indicador de ángulo de lanzamiento (línea punteada naranja)
  - Cohete rotado según dirección de velocidad
  - Punto de lanzamiento offset desde la izquierda

---

## 🎯 Resultados de Pruebas

### Comparación de Ángulos (Parámetros por defecto)

| Ángulo | Altura Máx | Alcance Máx | Velocidad Máx |
|--------|------------|-------------|---------------|
| 30°    | **7.26 m** | **27.83 m** ⭐ | 58.55 m/s |
| 45°    | 12.34 m    | 25.94 m     | 58.46 m/s |
| 60°    | 16.84 m    | 20.42 m     | 58.40 m/s |
| 75°    | 20.02 m    | 11.64 m     | 58.36 m/s |
| 90°    | 21.19 m    | 0.00 m      | 58.34 m/s |

### 🏆 Hallazgo Importante

**El ángulo óptimo es ~30°** (NO 45° como en el caso ideal sin fricción)

**¿Por qué?**
- En el vacío (sin fricción del aire), el ángulo óptimo es exactamente 45°
- Con resistencia del aire, ángulos más bajos (~30°) minimizan el tiempo de vuelo y la pérdida de energía por fricción
- El cohete pasa menos tiempo en el aire, por lo que pierde menos velocidad por arrastre

---

## 📊 Visualizaciones Generadas

### 1. `trajectory_2d.png`
- Gráfico X vs Y mostrando la trayectoria parabólica completa
- Código de color por fase:
  - 🟦 Azul: Expulsión de agua (máximo empuje)
  - 🟩 Verde: Empuje de aire (empuje reducido)
  - 🟥 Rojo: Vuelo balístico (solo gravedad)
- Marcadores de inicio y fin
- Grid con líneas de referencia

### 2. `results_series_2d.png`
- 6 subplots con todas las variables vs tiempo:
  - Posición horizontal
  - Posición vertical
  - Velocidad total
  - Componentes de velocidad (vx, vy)
  - Presión interna
  - Masa de agua restante

---

## 🚀 Cómo Usar

### Python

```bash
# Ejecutar comparación de ángulos
python quick_start_2d.py

# O ejecutar con ángulo específico
python main_simulation.py
# (edita parameters.py para cambiar launch_angle_deg)
```

### Aplicación Web

1. **Iniciar servidor**:
   ```bash
   python start_web_server.py
   ```

2. **Abrir navegador** en `http://localhost:8000`

3. **Ajustar controles**:
   - Presión inicial
   - Volumen de agua
   - Masa del cohete
   - Coeficiente de arrastre
   - Área de boquilla
   - **⭐ Ángulo de lanzamiento** (nuevo)

4. **Lanzar y observar**:
   - Trayectoria 2D en tiempo real
   - Trail de trayectoria (línea azul)
   - Indicador de ángulo
   - Estadísticas en vivo:
     - Altura actual
     - Velocidad actual
     - Agua restante
     - **Max altura**
     - **Max alcance** ⭐

---

## 🧪 Experimentos Sugeridos

### 1. Encontrar el Ángulo Óptimo
- Ejecuta `quick_start_2d.py`
- Observa cómo varía el alcance con el ángulo
- **Pregunta**: ¿Por qué 30° es mejor que 45°?

### 2. Efecto de la Presión
- Aumenta la presión → ¿Cambia el ángulo óptimo?
- Prueba: 20 psi, 70 psi, 150 psi

### 3. Efecto del Agua
- Muy poca agua (10%) vs mucha agua (70%)
- ¿Cuál da mayor alcance?
- ¿Cambia el ángulo óptimo?

### 4. Arrastre vs Sin Arrastre
- Establece `C_D = 0.0` (sin arrastre)
- Compara con `C_D = 0.75` (realista)
- ¿Ahora 45° es óptimo?

---

## 📚 Física Detrás de los Cambios

### Ecuaciones 2D

**Estado**: `Y = [x, y, vx, vy, M_w]`

**Derivadas**:
```
dx/dt = vx
dy/dt = vy

dvx/dt = (F_thrust_x + F_drag_x) / M_total
dvy/dt = (F_thrust_y + F_drag_y - M_total * g) / M_total

dM_w/dt = -ρ_w * A_e * u_e
```

**Fuerzas**:
- **Empuje**: Dirección de velocidad (o ángulo inicial)
  ```
  F_thrust_x = |F_thrust| * (vx / |v|)
  F_thrust_y = |F_thrust| * (vy / |v|)
  ```

- **Arrastre**: Opuesto a la velocidad
  ```
  F_drag_x = -0.5 * ρ * |v|² * Cd * A * (vx / |v|)
  F_drag_y = -0.5 * ρ * |v|² * Cd * A * (vy / |v|)
  ```

- **Gravedad**: Solo vertical
  ```
  F_gravity = -M_total * g  (dirección Y)
  ```

---

## ✅ Estado del Proyecto

### Completado
- ✅ Simulación Python 2D funcional
- ✅ Script de comparación de ángulos
- ✅ Visualizaciones 2D (trajectory, time series)
- ✅ Aplicación web con control de ángulo
- ✅ Canvas 2D con trayectoria en tiempo real
- ✅ Tracking de alcance máximo
- ✅ Documentación actualizada

### Pendiente (Opcional)
- ⏳ Actualizar Next.js app (next_app/) para 2D
- ⏳ Crear análisis de optimización multi-variable
- ⏳ Agregar viento lateral (componente adicional)
- ⏳ Modo de comparación lado-a-lado de ángulos

---

## 🎓 Conceptos Aprendidos

1. **Ángulo óptimo ≠ 45° en la realidad**
   - Fricción del aire cambia la física
   - Menor tiempo de vuelo = menor pérdida por arrastre

2. **Movimiento en 2D**
   - Separación de componentes X e Y
   - Fuerzas vectoriales
   - Integración numérica multi-dimensional

3. **Optimización bajo restricciones**
   - Trade-off entre altura y alcance
   - Resistencia del aire como restricción real

4. **Simulación vs Teoría**
   - Teoría (vacío): 45° óptimo
   - Simulación (realista): ~30° óptimo
   - Importancia de modelos precisos

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que todos los archivos estén actualizados
2. Ejecuta `python quick_start_2d.py` para verificar Python
3. Abre la consola del navegador (F12) para errores de JavaScript
4. Revisa este documento para entender los cambios

---

**¡Disfruta explorando trayectorias 2D! 🚀📐**

_Actualizado: Noviembre 30, 2025_
