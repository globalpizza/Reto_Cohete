# 🚀 COHETE DE AGUA - GUÍA RÁPIDA DE INICIO

## ✅ ESTADO DEL PROYECTO: TODO FUNCIONANDO CORRECTAMENTE

---

## 📦 ¿Qué tienes en este proyecto?

### 1. **Simulación Python Completa** ⚙️
- Física precisa con método de Euler
- Expansión adiabática, Bernoulli, arrastre
- Genera gráficos PNG automáticamente

### 2. **Aplicación Web Interactiva** 🌐
- Visualización animada en tiempo real
- Controles deslizantes para todos los parámetros
- Efectos visuales de propulsión

### 3. **Scripts de Prueba y Demostración** 🧪
- Suite de pruebas completa
- Modo interactivo por consola
- Script de inicio rápido

---

## 🎯 OPCIONES DE USO - ELIGE LA QUE PREFIERAS

### 💻 OPCIÓN 1: Simulación Python Rápida
**¿Cuándo usarla?** Cuando quieras resultados numéricos y gráficos precisos

```powershell
python quick_start.py
```

**Resultado**: 
- Datos numéricos en consola
- 2 gráficos PNG generados
- Tiempo: ~2 segundos

---

### 🌐 OPCIÓN 2: Aplicación Web Visual
**¿Cuándo usarla?** Cuando quieras ver la animación y experimentar interactivamente

```powershell
python start_web_server.py
```

**Resultado**:
- Se abre tu navegador automáticamente
- Interfaz gráfica completa
- Animación en tiempo real del vuelo

**URL Manual**: http://localhost:8000

---

### 🧪 OPCIÓN 3: Suite de Pruebas Completa
**¿Cuándo usarla?** Para verificar que todo funciona y ver comparaciones

```powershell
python test_simulation.py
```

**Resultado**:
- 4 pruebas automáticas
- Comparación de diferentes configuraciones
- Verificación de consistencia física

---

### 🎮 OPCIÓN 4: Modo Interactivo por Consola
**¿Cuándo usarla?** Para explorar sistemáticamente diferentes parámetros

```powershell
python demo_interactive.py
```

**Resultado**:
- Menú interactivo
- Modificar parámetros en vivo
- Análisis de optimización automático

---

## 📂 ARCHIVOS IMPORTANTES

### Archivos Principales
```
main_simulation.py      ← Simulación principal
visualization.py        ← Generación de gráficos
quick_start.py         ← Inicio rápido (recomendado para probar)
start_web_server.py    ← Inicia la aplicación web
test_simulation.py     ← Suite de pruebas
demo_interactive.py    ← Modo interactivo
```

### Carpetas
```
utils/                 ← Parámetros y métodos numéricos
physics/               ← Ecuaciones físicas del cohete
web_app/              ← Aplicación web completa
  ├── index.html      ← Interfaz
  ├── simulation.js   ← Física en JavaScript
  ├── main.js         ← Lógica de animación
  └── style.css       ← Estilos
```

### Documentación
```
INSTRUCCIONES.md       ← Guía completa del simulador Python
web_app/README_WEB.md  ← Guía de la aplicación web
INICIO_RAPIDO.md       ← Este archivo
```

---

## 🎓 EJEMPLO PRÁCTICO: PRIMER USO

### Paso 1: Verificar que funciona
```powershell
python quick_start.py
```

Deberías ver algo como:
```
🎯 Altura Máxima Alcanzada:        21.19 m
⚡ Velocidad Máxima Alcanzada:     58.34 m/s
💧 Tiempo de Vaciado de Agua:      0.041 s
⏱️  Tiempo Total de Vuelo:          4.28 s
```

### Paso 2: Ver los gráficos
Abre estos archivos:
- `results_series.png` - Gráficos de velocidad, presión y masa
- `trajectory.png` - Trayectoria del vuelo

### Paso 3: Probar la aplicación web
```powershell
python start_web_server.py
```

Juega con los controles:
1. Ajusta la presión (70 psi es el valor por defecto)
2. Cambia el volumen de agua (0.5 L es bueno para empezar)
3. Haz clic en "🚀 LANZAR"
4. ¡Observa el vuelo animado!

---

## ⚙️ PARÁMETROS Y SUS EFECTOS

| Parámetro | Valor Típico | Efecto de AUMENTAR |
|-----------|-------------|-------------------|
| **Presión** | 70 psi | ✅ Mayor altura y velocidad |
| **Volumen Agua** | 0.5 L (25%) | ⚠️ Existe un ÓPTIMO (~30%) |
| **Masa Cohete** | 55 g | ❌ Menor altura (más pesado) |
| **Área Boquilla** | 4.5 cm² | ⚠️ Vaciado más rápido, menos presión sostenida |
| **Coef. Arrastre** | 0.75 | ❌ Menor altura (más resistencia) |

---

## 🔬 EXPERIMENTOS SUGERIDOS

### Experimento 1: Encuentra el Volumen Óptimo
**En modo interactivo:**
```powershell
python demo_interactive.py
# Opción 5: Análisis de optimización
```

**En web:**
- Fija presión en 70 psi
- Varía agua de 0.2L a 1.2L
- Anota la altura máxima de cada uno
- Encuentra el pico

### Experimento 2: Comparar Presiones
**En modo interactivo:**
```powershell
python demo_interactive.py
# Opción 6: Comparar diferentes presiones
```

### Experimento 3: Diseñar tu Cohete Ideal
**En web:**
1. Empieza con parámetros por defecto
2. Cambia UN parámetro a la vez
3. Observa cómo afecta la altura máxima
4. Encuentra tu configuración óptima

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### "Module not found: numpy/pandas/matplotlib"
```powershell
python -m pip install numpy pandas matplotlib
```

### La simulación no termina / tarda mucho
- Verifica que los parámetros son razonables
- Presión entre 20-150 psi
- Volumen de agua < volumen de botella

### El servidor web no abre el navegador
- Ve manualmente a: http://localhost:8000
- O abre `web_app/index.html` directamente

### Los gráficos no se generan
- Verifica que matplotlib está instalado
- Si quieres que se muestren en pantalla, edita `visualization.py`:
  - Descomenta las líneas `# plt.show()`

---

## 📊 RESULTADOS ESPERADOS (Parámetros por Defecto)

Con los valores predeterminados (70 psi, 0.5L agua, 55g masa):

```
✓ Altura Máxima:     ~21.2 m
✓ Velocidad Máxima:  ~58.3 m/s (~210 km/h)
✓ Tiempo de Vaciado: ~0.04 s
✓ Tiempo de Vuelo:   ~4.3 s
```

Si tus resultados son muy diferentes, verifica:
1. Parámetros iniciales en `utils/parameters.py`
2. Que no hay errores en consola
3. Que las dependencias están instaladas

---

## 💡 CONSEJOS PARA ESTUDIANTES

### Para el Análisis Matemático:
1. Usa `test_simulation.py` para generar datos
2. Los gráficos PNG muestran las comparaciones
3. Lee los comentarios en el código (marcan las ecuaciones)

### Para la Presentación:
1. Usa la aplicación web para demostrar
2. Los gráficos PNG son perfectos para slides
3. Los números del `quick_start.py` son para reportes

### Para Entender la Física:
1. Lee `physics/water_phase.py` - ecuaciones principales
2. Lee `physics/derivatives.py` - sistema de EDOs
3. Compara con tus apuntes de clase

---

## 📞 COMANDOS ÚTILES DE REFERENCIA

```powershell
# INICIO RÁPIDO - Primera vez
python quick_start.py

# APLICACIÓN WEB - Visual e interactivo
python start_web_server.py

# PRUEBAS COMPLETAS - Verificación
python test_simulation.py

# MODO INTERACTIVO - Experimentación
python demo_interactive.py

# SIMULACIÓN BÁSICA - Solo datos
python main_simulation.py
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Marca cuando completes cada paso:

- [ ] ✓ Ejecuté `python quick_start.py` y funcionó
- [ ] ✓ Vi los archivos PNG generados
- [ ] ✓ Abrí la aplicación web y vi la animación
- [ ] ✓ Cambié parámetros y observé diferencias
- [ ] ✓ Entiendo qué hace cada archivo
- [ ] ✓ Puedo explicar la física implementada
- [ ] ✓ Realicé al menos un experimento

---

## 🎓 PRÓXIMOS PASOS

1. **Entender el código**:
   - Lee los archivos en orden: `parameters.py` → `water_phase.py` → `derivatives.py`
   - Cada archivo tiene comentarios explicativos

2. **Experimentar**:
   - Prueba diferentes configuraciones
   - Anota qué parámetros dan la mejor altura

3. **Comparar con teoría**:
   - Revisa las ecuaciones en tus apuntes
   - Compara con la Aproximación de Tsiolkovsky (gráfico rojo)

4. **Personalizar**:
   - Modifica parámetros en `parameters.py`
   - Crea tus propios experimentos

---

**🚀 ¡Todo está listo! Elige una opción de arriba y comienza a experimentar. ¡Buen vuelo! 🚀**

---

*Creado con 💙 para aprender física de cohetes de agua*
*Versión: 1.0 - Noviembre 2025*
