# 🎯 GUÍA DE USO - Simulación 2D del Cohete de Agua

## ✅ ¡Todo Está Listo!

Tu proyecto de cohete de agua ha sido **completamente actualizado** para incluir:

1. ✅ **Trayectorias 2D** (movimiento horizontal y vertical)
2. ✅ **Ángulo de lanzamiento ajustable** (0° - 90°)
3. ✅ **Cálculo de alcance horizontal máximo**
4. ✅ **Optimización automática de ángulo**
5. ✅ **Visualizaciones mejoradas** (trayectoria parabólica)

---

## 🚀 CÓMO EMPEZAR AHORA MISMO

### Paso 1: Prueba la Comparación de Ángulos (Python)

```bash
python quick_start_2d.py
```

**Qué hace**:
- Prueba automáticamente 5 ángulos diferentes (30°, 45°, 60°, 75°, 90°)
- Muestra tabla comparativa de altura, alcance y velocidad
- **Identifica el ángulo óptimo** para máximo alcance
- Genera 2 gráficos:
  - `trajectory_2d.png` - Trayectoria X vs Y
  - `results_series_2d.png` - 6 gráficos de series de tiempo

**Ejemplo de salida**:
```
📊 COMPARACIÓN DE ÁNGULOS DE LANZAMIENTO:
----------------------------------------------------------------------
  Ángulo |   Altura Máx |  Alcance Máx |  Velocidad Máx
----------------------------------------------------------------------
      30° |       7.26 m |      27.83 m |        58.55 m/s  ⭐ ÓPTIMO
      45° |      12.34 m |      25.94 m |        58.46 m/s
      60° |      16.84 m |      20.42 m |        58.40 m/s
      75° |      20.02 m |      11.64 m |        58.36 m/s
      90° |      21.19 m |       0.00 m |        58.34 m/s
```

---

### Paso 2: Prueba la Aplicación Web Interactiva

```bash
python start_web_server.py
```

**Qué hace**:
- Abre automáticamente el navegador en `http://localhost:8000`
- Te permite **ajustar parámetros con sliders** en tiempo real:
  - Presión inicial (PSI)
  - Volumen de agua
  - Masa del cohete
  - Coeficiente de arrastre
  - **⭐ Ángulo de lanzamiento** (NUEVO)

**Nuevas características visuales**:
- **Trayectoria 2D** en el canvas (no solo vertical)
- **Trail azul** mostrando el camino del cohete
- **Indicador de ángulo** (línea punteada naranja)
- **Cohete rotado** según su dirección de movimiento
- **Estadísticas en vivo**:
  - Max Altura
  - **Max Alcance** (NUEVO)
  - Max Velocidad

**Cómo usar**:
1. Ajusta los sliders a tu gusto
2. Modifica especialmente el **ángulo de lanzamiento**
3. Click en **"LANZAR 🚀"**
4. Observa la trayectoria parabólica
5. Compara diferentes ángulos

---

## 🧪 EXPERIMENTOS RECOMENDADOS

### Experimento 1: Encontrar el Ángulo Óptimo
**Objetivo**: Verificar que 30° da más alcance que 45°

1. Ejecuta `python quick_start_2d.py`
2. Observa la tabla de resultados
3. **Pregunta**: ¿Por qué 30° es mejor que 45°?
4. **Respuesta**: La resistencia del aire favorece ángulos bajos (menos tiempo en el aire = menos pérdida por fricción)

---

### Experimento 2: Efecto del Agua
**Objetivo**: Encontrar el porcentaje óptimo de agua

1. Abre la web app: `python start_web_server.py`
2. Fija el ángulo en 30°
3. Prueba diferentes volúmenes de agua:
   - 10% (0.2L) → Poco empuje
   - 25% (0.5L) → **Óptimo** ⭐
   - 50% (1.0L) → Mucho peso
   - 75% (1.5L) → Demasiado peso

4. **Observa**: Max alcance vs volumen de agua
5. **Conclusión**: ~25-40% es el rango óptimo

---

### Experimento 3: Presión vs Alcance
**Objetivo**: ¿Más presión = más alcance?

1. En la web app, fija:
   - Ángulo: 30°
   - Agua: 0.5L (25%)
   
2. Prueba diferentes presiones:
   - 20 psi (baja)
   - 70 psi (media)
   - 150 psi (alta)

3. **Observa**: Cómo cambia el alcance
4. **Pregunta**: ¿Hay un límite de utilidad?

---

### Experimento 4: Vacío vs Aire Real
**Objetivo**: Ver el efecto de la fricción del aire

**Método 1: Python**
1. Edita `utils/parameters.py`:
   ```python
   'C_D': 0.0,  # Sin fricción (vacío)
   ```
2. Ejecuta `python quick_start_2d.py`
3. **Observa**: ¿Ahora 45° es óptimo?

**Método 2: Web App**
1. Ajusta el slider de Cd a **0.1** (mínimo, casi sin fricción)
2. Prueba ángulo 45° vs 30°
3. Compara alcances

---

## 📊 INTERPRETAR LOS GRÁFICOS

### `trajectory_2d.png`
Este gráfico muestra **X vs Y** (vista lateral del vuelo):

- **Azul**: Fase de expulsión de agua (máximo empuje)
- **Verde**: Fase de aire comprimido (empuje medio)
- **Rojo**: Fase balística (solo gravedad)
- **Punto verde**: Inicio (0, 0)
- **Punto rojo**: Aterrizaje (alcance máximo, 0)

**Qué buscar**:
- Trayectoria más "plana" = ángulo bajo
- Trayectoria más "alta" = ángulo alto
- **Alcance máximo**: Distancia horizontal del punto rojo

---

### `results_series_2d.png`
6 gráficos mostrando variables vs tiempo:

1. **Posición X**: Avance horizontal (debe crecer hasta aterrizar)
2. **Posición Y**: Altura (sube y baja, toca 0 al final)
3. **Velocidad Total**: Pico al inicio (empuje máximo), luego decrece
4. **vx y vy**: Componentes de velocidad
   - vx: Decrece por fricción
   - vy: Sube, llega a 0 en altura máx, luego negativa (caída)
5. **Presión**: Decrece rápidamente (expansión adiabática)
6. **Masa de agua**: Decrece linealmente hasta 0

---

## 🎓 CONCEPTOS CLAVE APRENDIDOS

### 1. Ángulo Óptimo ≠ 45° en la Realidad
- **Teoría (vacío)**: 45° es óptimo
- **Práctica (con aire)**: ~30° es mejor
- **Razón**: Fricción favorece trayectorias rápidas (menos tiempo = menos pérdida)

### 2. Trade-off: Altura vs Alcance
- **90°**: Máxima altura, cero alcance
- **30°**: Altura media, máximo alcance
- **0°**: Cero altura, cero alcance (lanzamiento horizontal)

### 3. Optimización Multi-Variable
No solo el ángulo importa:
- Presión inicial
- Cantidad de agua
- Área de boquilla
- Coeficiente de arrastre (forma aerodinámica)

**Todos interactúan** para determinar el alcance final.

---

## 💡 TIPS Y TRUCOS

### Para Máximo Alcance
1. **Ángulo**: ~25-35° (depende de otros parámetros)
2. **Agua**: 25-40% del volumen total
3. **Presión**: Lo más alta posible (límite de seguridad: 150 psi)
4. **Forma**: Cd bajo (diseño aerodinámico)
5. **Boquilla**: Ni muy grande (poco tiempo de empuje) ni muy pequeña (poco flujo)

### Para Máxima Altura
1. **Ángulo**: 85-90°
2. **Agua**: 30-40%
3. **Presión**: Máxima
4. **Boquilla**: Óptima para tu presión/agua

---

## 🔧 MODIFICAR PARÁMETROS

### Opción 1: Archivo de Configuración (Python)

Edita `utils/parameters.py`:

```python
PARAMS = {
    'P_i_manometric_psi': 100.0,      # Aumenta presión
    'V_r_L': 2.0,                     # Volumen botella
    'V_0w_L': 0.6,                    # Más agua
    'A_e_cm2': 5.0,                   # Boquilla más grande
    'M_r_g': 50.0,                    # Cohete más liviano
    'C_D': 0.6,                       # Más aerodinámico
    'launch_angle_deg': 35.0,         # Cambia ángulo
    # ... otros parámetros
}
```

Luego ejecuta:
```bash
python main_simulation.py
python visualization.py
```

---

### Opción 2: Web App (Tiempo Real)

1. Inicia: `python start_web_server.py`
2. Usa los **sliders** para ajustar en vivo
3. Click **LANZAR** para probar
4. Click **REINICIAR** para otra configuración

**Ventaja**: Inmediato, visual, interactivo

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problema: Script no encuentra módulos
```
ModuleNotFoundError: No module named 'numpy'
```

**Solución**:
```bash
pip install numpy pandas matplotlib
```

---

### Problema: Gráficos no se muestran

**Windows**:
```python
# Agrega al inicio de visualization.py:
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
```

**Linux/Mac**:
```python
matplotlib.use('Qt5Agg')
```

---

### Problema: Web app muestra error en consola

1. Abre **DevTools** (F12 en el navegador)
2. Ve a la pestaña **Console**
3. Busca el error
4. Verifica que todos los archivos en `web_app/` estén actualizados:
   - `index.html`
   - `simulation.js`
   - `main.js`
   - `style.css`

---

### Problema: Servidor web no inicia (puerto ocupado)

```bash
# Verifica qué usa el puerto 8000
netstat -ano | findstr :8000

# Mata el proceso (Windows)
taskkill /PID <número_PID> /F

# O cambia el puerto en start_web_server.py
PORT = 8080  # Usa otro puerto
```

---

## 📚 ARCHIVOS DE DOCUMENTACIÓN

- `README.md` - Visión general del proyecto
- `CAMBIOS_2D.md` - Detalles técnicos de la actualización 2D
- `INSTRUCCIONES.md` - Guía de uso completa
- `RESUMEN_COMPLETO.md` - Análisis técnico detallado
- `INICIO_RAPIDO.md` - Inicio rápido original
- **`GUIA_USO_2D.md`** - Este archivo (guía práctica)

---

## 🎯 PRÓXIMOS PASOS SUGERIDOS

1. ✅ **Ejecuta `quick_start_2d.py`** para ver la comparación de ángulos
2. ✅ **Prueba la web app** con diferentes configuraciones
3. ✅ **Experimenta** con los 4 experimentos sugeridos
4. ✅ **Compara** resultados teóricos (45°) vs simulados (30°)
5. ✅ **Modifica** parámetros y observa cómo cambian los resultados

---

## 🏆 DESAFÍOS AVANZADOS

### Desafío 1: Encontrar la Configuración Óptima Global
Encuentra la combinación de:
- Ángulo
- Presión
- Volumen de agua
- Área de boquilla

...que maximice el alcance horizontal.

### Desafío 2: Predecir el Comportamiento
Sin ejecutar la simulación:
1. ¿Qué pasa si Cd = 0.0 (vacío)?
2. ¿Cuál sería el ángulo óptimo?
3. Luego verifica con la simulación

### Desafío 3: Diseño para Competencia
Diseña un cohete que:
- Alcance **al menos 30 metros**
- Use presión **máxima 100 psi** (seguridad)
- Tenga masa **máxima 70g**

---

## 📞 AYUDA ADICIONAL

Si tienes problemas o preguntas:

1. Revisa la sección **Solución de Problemas** arriba
2. Consulta `README.md` para visión general
3. Lee `CAMBIOS_2D.md` para detalles técnicos
4. Verifica los archivos de ejemplo en el proyecto

---

**¡Listo para empezar! 🚀**

_Ejecuta: `python quick_start_2d.py` ahora mismo_
