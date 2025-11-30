# 🚀 Next.js Water Rocket Simulator

Aplicación web moderna construida con **Next.js 16**, **React 19** y **TypeScript** que simula el vuelo de un cohete de agua con física de alta precisión usando el **método Runge-Kutta 4 (RK4)**.

## 🌟 Características

- ⚡ **Física RK4**: Integración numérica de 4to orden (más precisa que Euler)
- 🎨 **UI Moderna**: Tailwind CSS v4
- 📱 **Responsive**: Desktop, tablet y móvil
- 🎮 **Interactiva**: Controles en tiempo real
- 📊 **Estadísticas en Vivo**: Altura, velocidad, fase

## 🚀 Inicio Rápido

### Opción 1: Script PowerShell (desde la raíz del proyecto)

```powershell
.\start_next_app.ps1
```

### Opción 2: Comandos Manuales

```powershell
cd next_app
npm install  # Primera vez
npm run dev
```

Abre: **http://localhost:3000**

## 📦 Estructura

```
app/page.tsx              # Página principal
components/RocketSimulation.tsx  # Componente de simulación
utils/physics.ts          # Motor de física (RK4)
```

## 🎮 Controles

- **Presión (psi)**: 20-150
- **Volumen Agua (L)**: 0.1-1.5
- **Masa Cohete (g)**: 20-200
- **Coef. Arrastre**: 0.1-1.5
- **Boquilla (cm²)**: 1.0-10.0

## 🔬 Física

- **Método**: Runge-Kutta 4 (error O(h⁴))
- **Ecuaciones**: Adiabática, Bernoulli, Empuje, Arrastre
- **Precisión**: Superior a Euler simple

## 🛠️ Comandos

```powershell
npm run dev    # Desarrollo
npm run build  # Producción
npm start      # Ejecutar build
```

## 📚 Recursos

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript](https://www.typescriptlang.org)

---

**Para más información, consulta la documentación completa en el directorio raíz del proyecto.**
