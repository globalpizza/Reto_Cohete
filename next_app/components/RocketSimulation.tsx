"use client";

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { SimulationParams, SimulationState, convertToSI, rk4Step, RHO_W } from '../utils/physics';

const INITIAL_PARAMS: SimulationParams = {
  p_manometric_psi: 70.0,
  V_r_L: 2.0,
  V_0w_L: 0.5,
  A_e_cm2: 4.5,
  A_r_cm2: 95.0,
  M_r_g: 55.0,
  H_tube_m: 1.0,
  C_D: 0.75,
  A_ref_cm2: 100.0
};

export default function RocketSimulation() {
  // --- STATE ---
  const [params, setParams] = useState<SimulationParams>(INITIAL_PARAMS);
  const [stats, setStats] = useState<SimulationState>({
    y: 0, v: 0, M_w: 0, t: 0, phase: 'Launch Tube'
  });
  const [maxStats, setMaxStats] = useState({ h: 0, v: 0 });
  const [isRunning, setIsRunning] = useState(false);

  // Refs for animation loop
  const requestRef = useRef<number | null>(null);
  const stateRef = useRef<SimulationState>({
    y: 0, v: 0, M_w: 0, t: 0, phase: 'Launch Tube'
  });
  const siParamsRef = useRef(convertToSI(INITIAL_PARAMS));
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // --- LOGIC ---

  const resetSimulation = useCallback(() => {
    setIsRunning(false);
    const si = convertToSI(params);
    siParamsRef.current = si;

    const m0w = si.V_0w * RHO_W;
    const initialState: SimulationState = {
      y: 0, v: 0, M_w: m0w, t: 0, phase: 'Launch Tube'
    };

    stateRef.current = initialState;
    setStats(initialState);
    setMaxStats({ h: 0, v: 0 });

    draw(initialState);
  }, [params]);

  const startLaunch = () => {
    if (isRunning) return;
    resetSimulation();
    setIsRunning(true);
  };

  const updateParams = (key: keyof SimulationParams, value: number) => {
    setParams((prev: SimulationParams) => ({ ...prev, [key]: value }));
  };

  // --- ANIMATION LOOP ---

  const animate = useCallback(() => {
    if (!isRunning) return;

    // Physics Steps (Multiple per frame for stability)
    const dt = 0.005; // 5ms
    const stepsPerFrame = 4; // ~20ms simulated per frame (approx real-time at 60fps)

    let currentState = stateRef.current;
    const siParams = siParamsRef.current;

    for (let i = 0; i < stepsPerFrame; i++) {
      if (currentState.phase === 'Ballistic' && currentState.y <= 0 && currentState.v < 0) {
        currentState.y = 0;
        currentState.v = 0;
        setIsRunning(false);
        break;
      }
      currentState = rk4Step(currentState, siParams, dt);
    }

    stateRef.current = currentState;

    // Update React State for UI (throttled implicitly by render speed, but okay for simple app)
    setStats({ ...currentState });
    setMaxStats((prev: { h: number; v: number }) => ({
      h: Math.max(prev.h, currentState.y),
      v: Math.max(prev.v, currentState.v * 3.6) // km/h
    }));

    draw(currentState);

    if (isRunning) {
      requestRef.current = requestAnimationFrame(animate);
    }
  }, [isRunning]);

  useEffect(() => {
    if (isRunning) {
      requestRef.current = requestAnimationFrame(animate);
    } else {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    }
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [isRunning, animate]);

  // Initial Draw
  useEffect(() => {
    resetSimulation();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // --- DRAWING ---
  const draw = (state: SimulationState) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear
    ctx.fillStyle = '#0f172a'; // Slate 900
    ctx.fillRect(0, 0, width, height);

    // Dynamic Scale
    let scale = 20; // px/m
    if (state.y > 10) {
      scale = Math.max(2, 200 / (state.y + 1));
    }

    const groundY = height - 50;
    const rocketY = groundY - (state.y * scale);

    // Grid
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let h = 10; h < 1000; h += 10) {
      const y = groundY - (h * scale);
      if (y < 0) break;
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.fillStyle = '#64748b';
      ctx.fillText(`${h}m`, 10, y - 2);
    }
    ctx.stroke();

    // Ground
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(0, groundY, width, 50);

    // Rocket
    ctx.save();
    ctx.translate(width / 2, rocketY);

    // Body
    ctx.fillStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.ellipse(0, 0, 10, 30, 0, 0, Math.PI * 2);
    ctx.fill();

    // Fins
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(-10, 20);
    ctx.lineTo(-20, 40);
    ctx.lineTo(-10, 30);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(10, 20);
    ctx.lineTo(20, 40);
    ctx.lineTo(10, 30);
    ctx.fill();

    // Thrust Effects
    if (state.phase === 'Water Thrust') {
      ctx.fillStyle = 'rgba(59, 130, 246, 0.8)';
      ctx.beginPath();
      ctx.moveTo(-5, 30);
      ctx.lineTo(0, 30 + Math.random() * 60 + 20);
      ctx.lineTo(5, 30);
      ctx.fill();
    } else if (state.phase === 'Air Thrust') {
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.beginPath();
      ctx.moveTo(-5, 30);
      ctx.lineTo(0, 30 + Math.random() * 30);
      ctx.lineTo(5, 30);
      ctx.fill();
    }

    ctx.restore();
  };

  // Handle Resize
  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current && canvasRef.current.parentElement) {
        canvasRef.current.width = canvasRef.current.parentElement.clientWidth;
        canvasRef.current.height = canvasRef.current.parentElement.clientHeight;
        draw(stateRef.current);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // --- RENDER ---
  return (
    <div className="flex h-screen bg-slate-900 text-slate-50 font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-80 bg-slate-800/90 backdrop-blur-md border-r border-slate-700 p-6 flex flex-col gap-6 shadow-2xl z-10 overflow-y-auto">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight">
            🚀 WaterRocket<span className="text-blue-500">Sim</span>
          </h1>
          <p className="text-xs text-slate-400">RK4 Precision Physics Engine</p>
        </div>

        <div className="space-y-4">
          <ControlSlider label="Presión Inicial (psi)" value={params.p_manometric_psi} min={20} max={150} step={1} unit="psi" onChange={(v) => updateParams('p_manometric_psi', v)} />
          <ControlSlider label="Volumen Agua (L)" value={params.V_0w_L} min={0.1} max={1.5} step={0.1} unit="L" onChange={(v) => updateParams('V_0w_L', v)} />
          <ControlSlider label="Masa Cohete (g)" value={params.M_r_g} min={20} max={200} step={5} unit="g" onChange={(v) => updateParams('M_r_g', v)} />
          <ControlSlider label="Coef. Arrastre (Cd)" value={params.C_D} min={0.1} max={1.5} step={0.05} unit="" onChange={(v) => updateParams('C_D', v)} />
          <ControlSlider label="Boquilla (cm²)" value={params.A_e_cm2} min={1.0} max={10.0} step={0.5} unit="cm²" onChange={(v) => updateParams('A_e_cm2', v)} />
        </div>

        <div className="flex gap-3 mt-2">
          <button
            onClick={startLaunch}
            className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded-lg shadow-lg shadow-blue-500/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            LANZAR 🚀
          </button>
          <button
            onClick={resetSimulation}
            className="flex-1 bg-transparent border border-slate-600 hover:border-slate-400 text-slate-400 hover:text-white font-bold py-3 px-4 rounded-lg transition-colors"
          >
            RESET
          </button>
        </div>

        <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700 space-y-2">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Estadísticas en Vivo</h3>
          <StatRow label="Fase" value={stats.phase} highlight={stats.phase !== 'Ballistic'} />
          <StatRow label="Altura" value={`${stats.y.toFixed(1)} m`} />
          <StatRow label="Velocidad" value={`${(stats.v * 3.6).toFixed(1)} km/h`} />
          <StatRow label="Agua" value={`${((stats.M_w / (params.V_0w_L * RHO_W / 1000)) * 100).toFixed(0)}%`} />
        </div>
      </aside>

      {/* Main Viewport */}
      <main className="flex-1 relative bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-slate-950">
        <canvas ref={canvasRef} className="block w-full h-full" />

        {/* Overlay Stats */}
        <div className="absolute top-8 right-8 text-right pointer-events-none">
          <div className="bg-black/40 backdrop-blur-sm p-4 rounded-xl border border-white/10 shadow-xl">
            <div className="mb-2">
              <p className="text-sm text-slate-400">Max Altura</p>
              <p className="text-2xl font-bold text-white">{maxStats.h.toFixed(1)} <span className="text-sm font-normal text-slate-500">m</span></p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Max Velocidad</p>
              <p className="text-2xl font-bold text-white">{maxStats.v.toFixed(1)} <span className="text-sm font-normal text-slate-500">km/h</span></p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// --- SUBCOMPONENTS ---

function ControlSlider({ label, value, min, max, step, unit, onChange }: { label: string, value: number, min: number, max: number, step: number, unit: string, onChange: (v: number) => void }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs font-semibold">
        <label className="text-slate-400">{label}</label>
        <span className="text-blue-400">{value} {unit}</span>
      </div>
      <input
        type="range"
        min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400"
      />
    </div>
  );
}

function StatRow({ label, value, highlight = false }: { label: string, value: string, highlight?: boolean }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-slate-400">{label}</span>
      <span className={`font-mono font-bold ${highlight ? 'text-blue-400' : 'text-slate-200'}`}>{value}</span>
    </div>
  );
}
