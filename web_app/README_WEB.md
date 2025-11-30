# 🌐 Aplicación Web - Simulador de Cohete de Agua

## 📋 Descripción

Esta es una aplicación web interactiva que permite simular el vuelo de un cohete de agua en tiempo real con animación visual. La física está basada en el mismo modelo matemático que la simulación Python.

## 🚀 Cómo Ejecutar

### Opción 1: Servidor Python Simple (Recomendado)

1. Abre una terminal en la carpeta `web_app`
2. Ejecuta:
```powershell
python -m http.server 8000
```

3. Abre tu navegador en: `http://localhost:8000`

### Opción 2: Abrir Directamente

Simplemente abre el archivo `index.html` en tu navegador web favorito (Chrome, Firefox, Edge, etc.)

**Nota**: Algunos navegadores pueden tener restricciones de seguridad al abrir archivos HTML locales directamente. Si encuentras problemas, usa la Opción 1.

## 🎮 Cómo Usar

### Controles Disponibles

**Panel Lateral Izquierdo:**
- **Presión Inicial (psi)**: Ajusta la presión del aire comprimido (20-150 psi)
- **Volumen Botella (L)**: Capacidad total de la botella (1.0-3.0 L)
- **Volumen Agua (L)**: Cantidad de agua inicial (0.1-1.5 L)
  - Se muestra el % de llenado respecto al volumen de la botella
- **Masa Cohete (g)**: Masa seca del cohete sin agua (20-200 g)
- **Coef. Arrastre (Cd)**: Coeficiente de arrastre aerodinámico (0.1-1.5)
- **Boquilla (cm²)**: Área de la boquilla de salida (1.0-10.0 cm²)

### Botones

- **🚀 LANZAR**: Inicia la simulación con los parámetros actuales
- **↺ REINICIAR**: Reinicia la simulación y permite cambiar parámetros

### Estadísticas en Vivo

Durante la simulación, verás:
- **Fase actual**: Qué está haciendo el cohete
  - 🚀 Tubo Lanzamiento
  - 💧 Expulsión Agua
  - 💨 Empuje Aire
  - 🪂 Caída Libre
  - ✅ Aterrizó
- **Altura**: Altura instantánea en metros
- **Velocidad**: Velocidad instantánea en km/h
- **Agua Restante**: Porcentaje de agua que queda

### Panel Superior Derecho

Muestra los valores máximos alcanzados durante el vuelo:
- **Max Altura**: Altura máxima en metros
- **Max Velocidad**: Velocidad máxima en km/h

## 🎨 Visualización

### Elementos Visuales

1. **Cohete**: 
   - Cuerpo blanco/gris
   - Aletas rojas
   - Se mueve verticalmente

2. **Efectos de Propulsión**:
   - **Chorro azul**: Durante la fase de expulsión de agua
   - **Partículas azules**: Gotas de agua siendo expulsadas
   - **Chorro blanco**: Durante la fase de empuje de aire

3. **Escala Dinámica**:
   - La cámara hace zoom out automáticamente a medida que el cohete sube
   - Líneas de cuadrícula cada 10 metros con etiquetas

4. **Suelo**: Banda verde en la parte inferior

## 🔬 Física Implementada

La simulación web implementa la misma física que la versión Python:

1. **Expansión Adiabática**: `P·V^γ = constante`
2. **Ecuación de Bernoulli**: Para calcular velocidad de escape
3. **Método de Euler**: Integración numérica con `dt = 0.005s`
4. **Fuerzas**:
   - Empuje (proporcional a `-dm/dt × u_e`)
   - Gravedad (`m × g`)
   - Arrastre aerodinámico (`0.5 × ρ × v² × Cd × A`)

## 📊 Experimentos Sugeridos

### 1. Optimización del Volumen de Agua
- Fija la presión en 70 psi
- Varía el volumen de agua de 0.2L a 1.0L
- Observa cómo cambia la altura máxima
- **Resultado esperado**: Existe un volumen óptimo alrededor de 25-35% del volumen total

### 2. Efecto de la Presión
- Fija el volumen de agua en 0.5L
- Aumenta gradualmente la presión de 40 a 100 psi
- **Resultado esperado**: Mayor presión = mayor altura

### 3. Efecto del Área de Boquilla
- Fija presión en 70 psi y agua en 0.5L
- Prueba diferentes áreas de boquilla (2, 4.5, 8 cm²)
- **Resultado esperado**: 
  - Boquilla pequeña: Mayor velocidad de escape, pero más lento vaciado
  - Boquilla grande: Menor velocidad, pero más rápido vaciado

### 4. Comparación con Realidad
Si tienes un cohete de agua real:
- Mide sus parámetros (presión, volumen, masa)
- Configura esos valores en el simulador
- Compara la altura predicha con la altura real medida

## 🛠️ Estructura de Archivos

```
web_app/
├── index.html          # Estructura HTML y controles
├── style.css          # Estilos y diseño visual
├── simulation.js      # Física del cohete (port de Python)
├── main.js           # Lógica de UI y animación
└── README_WEB.md     # Este archivo
```

## 🔧 Personalización Avanzada

### Modificar Constantes Físicas

En `simulation.js`, puedes ajustar:
```javascript
const RHO_W = 997.0;      // Densidad del agua
const G = 9.81;           // Gravedad
const GAMMA = 1.4;        // Coef. adiabático
const RHO_AIR = 1.225;    // Densidad del aire
const DT = 0.005;         // Paso de integración
```

### Ajustar Velocidad de Simulación

En `main.js`, función `loop()`:
```javascript
// Cambiar el número de pasos por frame (4 = tiempo real)
for (let i = 0; i < 4; i++) {  // Aumenta para más rápido
  sim.step();
}
```

### Personalizar Colores

En `style.css`, modifica las variables CSS:
```css
:root {
    --accent: #3b82f6;        /* Color principal (azul)
    --bg-dark: #0f172a;       /* Fondo oscuro
    --success: #22c55e;       /* Verde (suelo)
}
```

## 📱 Compatibilidad

✅ Navegadores Soportados:
- Chrome/Edge (Chromium) - Recomendado
- Firefox
- Safari
- Opera

⚠️ Requisitos:
- JavaScript habilitado
- Canvas HTML5 soportado
- Navegador moderno (últimas 2 versiones)

## 🐛 Solución de Problemas

### El cohete no se mueve
- Verifica que presionaste "LANZAR 🚀"
- Asegúrate de que el volumen de agua es menor que el de la botella
- Revisa que la presión es mayor que 0

### La animación va muy lenta
- Reduce la resolución de pantalla
- Aumenta el paso de tiempo `DT` en `simulation.js`
- Cierra otras pestañas del navegador

### No se ven los efectos visuales
- Algunos navegadores pueden tener problemas con transparencias
- Actualiza tu navegador a la última versión
- Prueba en Chrome/Edge

### Los valores no tienen sentido
- Verifica que los parámetros están en rangos razonables
- Presión: 30-100 psi es típico
- Volumen agua: 20-40% del volumen total es óptimo
- No pongas masa del cohete muy baja (<20g)

## 📚 Referencias

Esta aplicación web es un complemento visual de la simulación Python completa. Para análisis más detallados, gráficos avanzados y datos numéricos precisos, usa la versión Python del simulador.

---

**¡Disfruta experimentando con tu cohete de agua virtual en 3D! 🚀💧**
