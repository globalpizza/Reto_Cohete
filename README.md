# 🚀 Simulador de Cohete de Agua - Proyecto Completo

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Next.js](https://img.shields.io/badge/Next.js-16.0-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Simulación física completa de un **cohete de agua** con tres implementaciones diferentes:

1. **Python** (Método de Euler) - Simulación científica con visualizaciones
2. **Web App (Vanilla JS)** - Visualización interactiva en tiempo real
3. **Next.js App** (TypeScript + RK4) - Aplicación web moderna de alta precisión

### ⭐ Características Principales

- ✅ **Trayectorias 2D** con ángulo de lanzamiento ajustable
- ✅ **Cálculo de alcance horizontal** y altura máxima
- ✅ **Física realista**: Expansión adiabática, ecuación de Bernoulli, Tsiolkovsky
- ✅ **Fases del vuelo**: Tubo de lanzamiento, expulsión de agua, empuje de aire, vuelo balístico
- ✅ **Resistencia del aire** con arrastre cuadrático
- ✅ **Visualizaciones interactivas** y gráficos científicos
- ✅ **Comparación de ángulos** para encontrar el óptimo

---

## 🎯 ¿Qué Hay de Nuevo? (Actualización 2D)

### Antes (1D - Solo Vertical)
- Simulaba solo movimiento vertical
- Calculaba únicamente altura máxima
- Ángulo de lanzamiento no considerado

### Ahora (2D - Completo) ⭐
- **Trayectorias parabólicas completas** (X e Y)
- **Alcance horizontal** además de altura
- **Ángulo de lanzamiento ajustable** (0° - 90°)
- **Optimización de ángulo** para máximo alcance
- **Visualización de trayectoria** en tiempo real

📖 Ver detalles completos en [CAMBIOS_2D.md](CAMBIOS_2D.md)

---

## 🚀 Inicio Rápido

### Opción 1: Script de Comparación de Ángulos (Recomendado)

```bash
# Instalar dependencias
pip install numpy pandas matplotlib

# Ejecutar comparación automática
python quick_start_2d.py
```

**Salida**: Tabla comparativa + gráficos de trayectoria 2D

### Opción 2: Aplicación Web Interactiva

```bash
# Iniciar servidor
python start_web_server.py

# Abre automáticamente: http://localhost:8000
```

**Controles disponibles**:
- Presión inicial (PSI)
- Volumen de botella y agua
- Masa del cohete
- Coeficiente de arrastre
- Área de boquilla
- **⭐ Ángulo de lanzamiento** (nuevo)

### Opción 3: App Next.js (Avanzado)

```bash
cd next_app
npm install
npm run dev

# Abre: http://localhost:3000
```

---

## 📁 Estructura del Proyecto

```
Reto_Cohete/
│
├── 📄 README.md                    # Este archivo
├── 📄 CAMBIOS_2D.md               # Documentación de cambios 2D
├── 📄 INSTRUCCIONES.md            # Guía detallada de uso
├── 📄 RESUMEN_COMPLETO.md         # Resumen técnico completo
├── 📄 INICIO_RAPIDO.md            # Guía de inicio rápido
│
├── 🐍 Python - Simulación Core
│   ├── main_simulation.py         # Orquestador principal
│   ├── quick_start_2d.py          # ⭐ Script de comparación de ángulos
│   ├── visualization.py           # Generación de gráficos 2D
│   ├── demo_interactive.py        # Demo interactiva
│   ├── test_simulation.py         # Suite de pruebas
│   │
│   ├── utils/
│   │   ├── parameters.py          # Parámetros físicos (+ ángulo)
│   │   └── euler.py               # Integración numérica
│   │
│   └── physics/
│       ├── derivatives.py         # ⭐ Derivadas 2D (X, Y)
│       └── water_phase.py         # Cálculos de fase de agua
│
├── 🌐 Web App (Vanilla JS)
│   ├── web_app/
│   │   ├── index.html             # UI con slider de ángulo
│   │   ├── simulation.js          # ⭐ Física 2D en JS
│   │   ├── main.js                # ⭐ Visualización 2D + trayectoria
│   │   └── style.css              # Estilos
│   │
│   └── start_web_server.py        # Servidor local
│
└── ⚡ Next.js App
    └── next_app/
        ├── app/
        │   ├── page.tsx           # Página principal
        │   └── layout.tsx         # Layout global
        ├── components/
        │   └── RocketSimulation.tsx # Componente de simulación
        ├── utils/
        │   └── physics.ts         # Motor de física (RK4)
        └── package.json           # Dependencias Node
```

---

## 🧪 Resultados de Pruebas

### Comparación de Ángulos (Configuración por Defecto)

| Ángulo | Altura Máx | **Alcance Máx** | Velocidad Máx |
|--------|------------|-----------------|---------------|
| 30°    | 7.26 m     | **27.83 m** ⭐   | 58.55 m/s     |
| 45°    | 12.34 m    | 25.94 m         | 58.46 m/s     |
| 60°    | 16.84 m    | 20.42 m         | 58.40 m/s     |
| 75°    | 20.02 m    | 11.64 m         | 58.36 m/s     |
| 90°    | 21.19 m    | 0.00 m          | 58.34 m/s     |

### 🎯 Hallazgo Clave

**El ángulo óptimo para máximo alcance es ~30°**, no 45° como en la teoría ideal.

**Razón**: La resistencia del aire favorece ángulos más bajos que minimizan el tiempo de vuelo y la pérdida de energía por fricción.

---

## 📊 Visualizaciones Generadas

### 1. Trayectoria 2D (`trajectory_2d.png`)
- Gráfico X vs Y mostrando trayectoria parabólica completa
- Código de color por fase: Agua (azul) → Aire (verde) → Balístico (rojo)
- Marcadores de inicio y aterrizaje

### 2. Series de Tiempo (`results_series_2d.png`)
6 subplots mostrando:
1. Posición X vs tiempo
2. Posición Y vs tiempo  
3. Velocidad total vs tiempo
4. Componentes vx y vy vs tiempo
5. Presión interna vs tiempo
6. Masa de agua vs tiempo

---

## 🔬 Física Implementada

### Modelo Completo

1. **Fase de Agua** (Mayor empuje)
   - Expansión adiabática: `P·V^γ = constante`
   - Ecuación de Bernoulli para velocidad de salida
   - Ecuación de Tsiolkovsky (cohete)

2. **Fase de Aire** (Empuje reducido)
   - Escape de aire comprimido
   - Presión decayendo hasta P_atm

3. **Fase Balística** (Sin empuje)
   - Solo gravedad y arrastre
   - Movimiento parabólico modificado

### Ecuaciones 2D

**Vector de estado**: `Y = [x, y, vx, vy, M_w]`

**Derivadas**:
```
dx/dt = vx
dy/dt = vy

dvx/dt = (F_thrust_x + F_drag_x) / M_total
dvy/dt = (F_thrust_y + F_drag_y - M_total·g) / M_total

dM_w/dt = -ρ_w · A_e · u_e
```

**Fuerzas**:
- **Empuje**: Dirección de velocidad (o ángulo inicial si v=0)
- **Arrastre**: `F_D = -0.5 · ρ · v² · Cd · A · (v̂)`
- **Gravedad**: `-M · g` (solo eje Y)

---

## 🎓 Experimentos Sugeridos

### 1. Optimización de Ángulo
```bash
python quick_start_2d.py
```
- Prueba múltiples ángulos automáticamente
- Encuentra el óptimo para tu configuración

### 2. Efecto del Agua
- Muy poca agua (10%): Poco empuje, corto alcance
- Mucha agua (70%): Mucho peso inicial, también corto alcance
- **Óptimo**: ~25-40% del volumen de la botella

### 3. Presión vs Alcance
```python
# En parameters.py, cambia:
'P_i_manometric_psi': 20   # Baja presión
'P_i_manometric_psi': 150  # Alta presión
```

### 4. Arrastre vs Vacío
```python
# En parameters.py:
'C_D': 0.0   # Simula vacío (sin fricción)
'C_D': 0.75  # Realista
```
**Pregunta**: ¿Ahora 45° es óptimo?

---

## 📚 Documentación Completa

- 📖 [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Guía paso a paso
- 📖 [INSTRUCCIONES.md](INSTRUCCIONES.md) - Uso detallado
- 📖 [RESUMEN_COMPLETO.md](RESUMEN_COMPLETO.md) - Análisis técnico
- 📖 [CAMBIOS_2D.md](CAMBIOS_2D.md) - Nueva funcionalidad 2D
- 📖 [web_app/README.md](web_app/README.md) - Guía de la web app
- 📖 [next_app/README.md](next_app/README.md) - Guía de Next.js app

---

## 🛠️ Tecnologías Utilizadas

### Python
- **NumPy**: Operaciones vectoriales y arrays
- **Pandas**: Manejo de datos tabulares
- **Matplotlib**: Visualizaciones científicas

### JavaScript (Web App)
- **Vanilla JS**: Sin dependencias
- **HTML5 Canvas**: Renderizado 2D
- **CSS3**: Estilos modernos

### Next.js App
- **React 19**: UI componentes
- **TypeScript**: Tipado estático
- **Tailwind CSS v4**: Estilos utility-first
- **Runge-Kutta 4**: Integración de alta precisión

---

## 🧮 Parámetros Configurables

| Parámetro | Rango | Default | Descripción |
|-----------|-------|---------|-------------|
| Presión inicial | 20-150 psi | 70 psi | Presión manométrica del aire |
| Volumen botella | 1.0-3.0 L | 2.0 L | Capacidad total |
| Volumen agua | 0.1-1.5 L | 0.5 L | Agua inicial (25%) |
| Masa cohete | 20-200 g | 55 g | Masa en vacío |
| Coef. arrastre | 0.1-1.5 | 0.75 | Cd aerodinámico |
| Área boquilla | 1.0-10.0 cm² | 4.5 cm² | Área de salida |
| **⭐ Ángulo lanzamiento** | 0-90° | 45° | Ángulo desde horizontal |

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install numpy pandas matplotlib
```

### Error: "Cannot read properties of null"
- Asegúrate de que todos los archivos HTML, JS y CSS estén en `web_app/`
- Verifica la consola del navegador (F12)

### Gráficos no se generan
```bash
# En algunos sistemas, matplotlib necesita:
import matplotlib
matplotlib.use('TkAgg')  # O 'Qt5Agg'
```

### Servidor web no inicia
```bash
# Verifica que el puerto 8000 esté libre
netstat -ano | findstr :8000

# O cambia el puerto en start_web_server.py
PORT = 8080  # Otro puerto
```

---

## 🎯 Roadmap Futuro

- [ ] Actualizar Next.js app para 2D
- [ ] Agregar viento lateral (3D completo)
- [ ] Optimización automática multi-variable
- [ ] Exportar datos a CSV/Excel
- [ ] Comparación lado-a-lado de configuraciones
- [ ] Modo de competencia (ranking de alcance)
- [ ] Soporte para múltiples cohetes simultáneos

---

**¡Disfruta explorando la física de los cohetes de agua! 🚀🔬**

_Última actualización: Noviembre 30, 2025_
