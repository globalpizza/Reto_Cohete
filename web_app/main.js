/**
 * main.js
 * Handles UI interactions and the animation loop.
 */

// --- DOM Elements ---
const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

// Inputs
const inputs = {
  p_psi: document.getElementById('p_psi'),
  v_bottle: document.getElementById('v_bottle'),
  v_water: document.getElementById('v_water'),
  m_rocket: document.getElementById('m_rocket'),
  cd: document.getElementById('cd'),
  a_nozzle: document.getElementById('a_nozzle'),
  launch_angle: document.getElementById('launch_angle')
};

// Displays
const displays = {
  p_psi: document.getElementById('val_p_psi'),
  v_bottle: document.getElementById('val_v_bottle'),
  v_water: document.getElementById('val_v_water'),
  m_rocket: document.getElementById('val_m_rocket'),
  cd: document.getElementById('val_cd'),
  a_nozzle: document.getElementById('val_a_nozzle'),
  launch_angle: document.getElementById('val_launch_angle')
};

// Stats
const stats = {
  phase: document.getElementById('stat-phase'),
  height: document.getElementById('stat-height'),
  range: document.getElementById('stat-range'),
  velocity: document.getElementById('stat-velocity'),
  water: document.getElementById('stat-water'),
  time: document.getElementById('stat-time'),
  maxHeight: document.getElementById('max-height'),
  maxRange: document.getElementById('max-range'),
  maxSpeed: document.getElementById('max-speed'),
  flightTime: document.getElementById('flight-time')
};

// Buttons
const btnLaunch = document.getElementById('btn-launch');
const btnReset = document.getElementById('btn-reset');
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');

// Presets
const PRESETS = {
  beginner: {
    p_psi: 50,
    v_bottle: 2.0,
    v_water: 0.5,
    m_rocket: 60,
    cd: 0.75,
    a_nozzle: 4.5,
    launch_angle: 45
  },
  optimal: {
    p_psi: 85,
    v_bottle: 2.0,
    v_water: 0.7,
    m_rocket: 45,
    cd: 0.55,
    a_nozzle: 5.0,
    launch_angle: 30
  },
  'max-height': {
    p_psi: 100,
    v_bottle: 2.0,
    v_water: 0.8,
    m_rocket: 40,
    cd: 0.5,
    a_nozzle: 4.0,
    launch_angle: 85
  },
  'max-range': {
    p_psi: 90,
    v_bottle: 2.0,
    v_water: 0.65,
    m_rocket: 45,
    cd: 0.5,
    a_nozzle: 5.5,
    launch_angle: 30
  }
};

// --- State ---
let sim = null;
let animationId = null;
let isRunning = false;
let scale = 10; // Pixels per meter (initial)
let cameraY = 0; // Camera vertical position
let maxH = 0;
let maxR = 0;
let maxV = 0;

// --- Initialization ---
function init() {
  // Initialize simulation FIRST
  resetSimulation();
  
  // Then setup canvas
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  // Mobile menu toggle
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768 && 
          !sidebar.contains(e.target) && 
          !menuToggle.contains(e.target) &&
          sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
      }
    });
  }
  
  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const preset = btn.dataset.preset;
      applyPreset(preset);
      
      // Visual feedback
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
  
  // Bind inputs
  Object.keys(inputs).forEach(key => {
    inputs[key].addEventListener('input', (e) => {
      // Si cambia el volumen de botella, ajustar límite de agua
      if (key === 'v_bottle') {
        const bottleVol = parseFloat(e.target.value);
        inputs.v_water.max = bottleVol * 0.95; // Max 95% de llenado
        // Si el agua actual excede el nuevo límite, ajustarla
        if (parseFloat(inputs.v_water.value) > bottleVol * 0.95) {
          inputs.v_water.value = bottleVol * 0.95;
          updateDisplay('v_water', inputs.v_water.value);
        }
      }
      
      updateDisplay(key, e.target.value);
      if (!isRunning) resetSimulation(); // Live preview reset
    });
  });

  btnLaunch.addEventListener('click', startLaunch);
  btnReset.addEventListener('click', resetSimulation);
  
  // Initialize all displays
  Object.keys(inputs).forEach(key => {
    updateDisplay(key, inputs[key].value);
  });

  draw(); // Initial draw (now sim exists)
}

function applyPreset(presetName) {
  const preset = PRESETS[presetName];
  if (!preset) return;
  
  Object.keys(preset).forEach(key => {
    if (inputs[key]) {
      inputs[key].value = preset[key];
      updateDisplay(key, preset[key]);
    }
  });
  
  resetSimulation();
}

function resizeCanvas() {
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  if (sim) draw();
}

function updateDisplay(key, value) {
  let suffix = '';
  if (key === 'p_psi') suffix = ' psi';
  if (key === 'v_bottle') suffix = ' L';
  if (key === 'v_water') {
    const bottleVol = parseFloat(inputs.v_bottle.value);
    const waterVol = parseFloat(value);
    const percent = ((waterVol / bottleVol) * 100).toFixed(0);
    suffix = ` L (${percent}%)`;
  }
  if (key === 'm_rocket') suffix = ' g';
  if (key === 'a_nozzle') suffix = ' cm²';
  if (key === 'launch_angle') suffix = '°';

  displays[key].textContent = value + suffix;
}

function getParams() {
  return {
    p_manometric_psi: parseFloat(inputs.p_psi.value),
    V_r_L: parseFloat(inputs.v_bottle.value),
    V_0w_L: parseFloat(inputs.v_water.value),
    A_e_cm2: parseFloat(inputs.a_nozzle.value),
    A_r_cm2: 95.0,
    M_r_g: parseFloat(inputs.m_rocket.value),
    H_tube_m: 1.0,
    C_D: parseFloat(inputs.cd.value),
    A_ref_cm2: 100.0,
    launch_angle_deg: parseFloat(inputs.launch_angle.value)
  };
}

function resetSimulation() {
  cancelAnimationFrame(animationId);
  isRunning = false;
  sim = new RocketSimulation(getParams());
  maxH = 0;
  maxR = 0;
  maxV = 0;
  cameraY = 0;

  // Reset stats
  stats.phase.textContent = "Listo";
  stats.phase.className = "stat-value phase-ready";
  stats.height.textContent = "0.0 m";
  stats.range.textContent = "0.0 m";
  stats.velocity.textContent = "0.0 km/h";
  stats.water.textContent = "100%";
  stats.time.textContent = "0.0 s";
  stats.maxHeight.textContent = "0.0";
  stats.maxRange.textContent = "0.0";
  stats.maxSpeed.textContent = "0.0";
  stats.flightTime.textContent = "0.0";
  
  // Reset progress
  document.getElementById('progressContainer').style.display = 'none';
  document.getElementById('progressFill').style.width = '0%';

  draw();
}

function startLaunch() {
  if (isRunning) return;
  resetSimulation(); // Ensure fresh start
  isRunning = true;
  lastTime = performance.now();
  
  // Show progress
  document.getElementById('progressContainer').style.display = 'block';
  
  loop();
}

let lastTime = 0;
const SIM_SPEED = 1.0; // Real-time multiplier

function loop(timestamp) {
  if (!isRunning) return;

  // Run physics steps
  // We run multiple physics steps per frame to keep stability if needed, 
  // but here we just run enough to match real time or faster.
  // For simplicity, we run 5 physics steps per frame (approx 60fps * 5 * 0.005s = 1.5s simulated per second)
  // Let's try to match real-time: 1 frame ~ 16ms. DT=5ms. So ~3 steps per frame.

  for (let i = 0; i < 4; i++) {
    sim.step();
  }

  if (!sim.flightActive) {
    isRunning = false;
  }

  // Update Stats
  const h = sim.state.y;
  const r = sim.state.x;
  const v_total = Math.sqrt(sim.state.vx * sim.state.vx + sim.state.vy * sim.state.vy);
  const v_kmh = v_total * 3.6;

  if (h > maxH) maxH = h;
  if (r > maxR) maxR = r;
  if (v_kmh > maxV) maxV = v_kmh;

  stats.height.textContent = h.toFixed(1) + " m";
  stats.range.textContent = r.toFixed(1) + " m";
  stats.velocity.textContent = v_kmh.toFixed(1) + " km/h";
  stats.time.textContent = sim.state.t.toFixed(2) + " s";

  const waterPercent = (sim.state.M_w / (sim.params.V_0w * RHO_W)) * 100;
  stats.water.textContent = Math.max(0, waterPercent).toFixed(0) + "%";

  stats.maxHeight.textContent = maxH.toFixed(1);
  stats.maxRange.textContent = maxR.toFixed(1);
  stats.maxSpeed.textContent = maxV.toFixed(1);
  stats.flightTime.textContent = sim.state.t.toFixed(2);
  
  // Update progress bar
  const progress = Math.min(100, (sim.state.t / 5.0) * 100); // Assume max 5s flight
  document.getElementById('progressFill').style.width = progress + '%';

  // Phase styling
  let phaseClass = "phase-ready";
  let phaseDisplay = sim.state.phase;
  
  if (sim.state.phase.includes("Water")) {
    phaseClass = "phase-water";
    phaseDisplay = "💧 Expulsión Agua";
  } else if (sim.state.phase.includes("Air")) {
    phaseClass = "phase-air";
    phaseDisplay = "💨 Empuje Aire";
  } else if (sim.state.phase.includes("Ballistic")) {
    phaseClass = "phase-ballistic";
    phaseDisplay = "🪂 Caída Libre";
  } else if (sim.state.phase.includes("Launch")) {
    phaseClass = "phase-water";
    phaseDisplay = "🚀 Tubo Lanzamiento";
  }
  
  if (!sim.flightActive && sim.state.y <= 0) {
    phaseDisplay = "✅ Aterrizó";
    phaseClass = "phase-ready";
  }

  stats.phase.textContent = phaseDisplay;
  stats.phase.className = "stat-value " + phaseClass;

  draw();

  if (isRunning) {
    animationId = requestAnimationFrame(loop);
  }
}

// --- Drawing ---
function draw() {
  // Clear
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (!sim) return;

  // Dynamic Scale
  let currentScale = 15;
  const maxDim = Math.max(maxH, maxR);
  if (maxDim > 15) {
    currentScale = Math.max(2, (canvas.height - 150) / maxDim);
  }

  const groundY = canvas.height - 60;
  const launchX = 120;
  const rocketCanvasX = launchX + (sim.state.x * currentScale);
  const rocketCanvasY = groundY - (sim.state.y * currentScale);

  // Draw Grid Background (improved)
  ctx.save();
  
  // Horizontal grid lines (height)
  ctx.strokeStyle = 'rgba(51, 65, 85, 0.3)';
  ctx.lineWidth = 1;
  ctx.font = '11px Inter, sans-serif';
  ctx.fillStyle = '#64748b';
  
  for (let h = 5; h < 200; h += 5) {
    const y = groundY - (h * currentScale);
    if (y < 20) break;
    
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
    
    if (h % 10 === 0) {
      ctx.fillText(h + 'm', 8, y - 3);
    }
  }
  
  // Vertical grid lines (distance)
  for (let d = 10; d < 200; d += 10) {
    const x = launchX + (d * currentScale);
    if (x > canvas.width - 20) break;
    
    ctx.beginPath();
    ctx.moveTo(x, groundY);
    ctx.lineTo(x, 0);
    ctx.stroke();
    
    ctx.fillText(d + 'm', x - 10, groundY - 5);
  }
  
  ctx.restore();

  // Draw Ground with grass texture
  const gradient = ctx.createLinearGradient(0, groundY, 0, canvas.height);
  gradient.addColorStop(0, '#22c55e');
  gradient.addColorStop(1, '#16a34a');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
  
  // Ground line
  ctx.strokeStyle = '#15803d';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, groundY);
  ctx.lineTo(canvas.width, groundY);
  ctx.stroke();

  // Draw trajectory trail with gradient
  if (sim.history.length > 1) {
    ctx.strokeStyle = 'rgba(59, 130, 246, 0.6)';
    ctx.lineWidth = 3;
    ctx.shadowColor = 'rgba(59, 130, 246, 0.5)';
    ctx.shadowBlur = 6;
    ctx.beginPath();
    ctx.moveTo(launchX, groundY);
    sim.history.forEach(point => {
      const px = launchX + (point.x * currentScale);
      const py = groundY - (point.y * currentScale);
      ctx.lineTo(px, py);
    });
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  // Draw launch angle indicator
  ctx.save();
  ctx.translate(launchX, groundY);
  ctx.strokeStyle = 'rgba(251, 146, 60, 0.8)';
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 5]);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  const angleLen = 60;
  ctx.lineTo(angleLen * Math.cos(sim.params.launch_angle_rad), 
             -angleLen * Math.sin(sim.params.launch_angle_rad));
  ctx.stroke();
  ctx.setLineDash([]);
  
  // Angle arc
  ctx.strokeStyle = 'rgba(251, 146, 60, 0.5)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(0, 0, 30, -sim.params.launch_angle_rad, 0, false);
  ctx.stroke();
  
  // Angle label
  ctx.fillStyle = '#fb923c';
  ctx.font = 'bold 12px Inter';
  const angleDeg = (sim.params.launch_angle_rad * 180 / Math.PI).toFixed(0);
  ctx.fillText(angleDeg + '°', 35, -10);
  
  ctx.restore();

  // Draw launch platform
  ctx.fillStyle = '#475569';
  ctx.fillRect(launchX - 15, groundY - 5, 30, 5);

  // Draw Rocket
  ctx.save();
  ctx.translate(rocketCanvasX, rocketCanvasY);
  
  // Rotate rocket based on velocity direction
  let rocketAngle = sim.params.launch_angle_rad;
  if (sim.state.vx !== 0 || sim.state.vy !== 0) {
    rocketAngle = Math.atan2(sim.state.vy, sim.state.vx) - Math.PI / 2;
  } else {
    rocketAngle = sim.params.launch_angle_rad - Math.PI / 2;
  }
  ctx.rotate(rocketAngle);

  // Rocket Body with gradient
  const bodyGradient = ctx.createLinearGradient(-10, 0, 10, 0);
  bodyGradient.addColorStop(0, '#cbd5e1');
  bodyGradient.addColorStop(0.5, '#f1f5f9');
  bodyGradient.addColorStop(1, '#cbd5e1');
  ctx.fillStyle = bodyGradient;
  ctx.beginPath();
  ctx.ellipse(0, 0, 12, 32, 0, 0, Math.PI * 2);
  ctx.fill();
  
  // Rocket outline
  ctx.strokeStyle = '#94a3b8';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Nose cone
  ctx.fillStyle = '#ef4444';
  ctx.beginPath();
  ctx.moveTo(0, -32);
  ctx.lineTo(-8, -18);
  ctx.lineTo(8, -18);
  ctx.closePath();
  ctx.fill();

  // Fins (improved)
  ctx.fillStyle = '#ef4444';
  ctx.strokeStyle = '#dc2626';
  ctx.lineWidth = 1;
  
  ctx.beginPath();
  ctx.moveTo(-12, 20);
  ctx.lineTo(-22, 38);
  ctx.lineTo(-12, 32);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  
  ctx.beginPath();
  ctx.moveTo(12, 20);
  ctx.lineTo(22, 38);
  ctx.lineTo(12, 32);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Window
  ctx.fillStyle = '#3b82f6';
  ctx.beginPath();
  ctx.arc(0, -8, 4, 0, Math.PI * 2);
  ctx.fill();

  // Water Jet (Visuals) - improved
  if (sim.state.phase.includes("Water") && isRunning) {
    ctx.fillStyle = 'rgba(59, 130, 246, 0.7)';
    ctx.shadowColor = 'rgba(59, 130, 246, 0.8)';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.moveTo(-6, 32);
    ctx.lineTo(-3, 32 + Math.random() * 60 + 30);
    ctx.lineTo(0, 32 + Math.random() * 70 + 40);
    ctx.lineTo(3, 32 + Math.random() * 60 + 30);
    ctx.lineTo(6, 32);
    ctx.closePath();
    ctx.fill();
    ctx.shadowBlur = 0;

    // Particles
    for (let i = 0; i < 8; i++) {
      const offsetX = (Math.random() - 0.5) * 20;
      const offsetY = 32 + Math.random() * 60;
      const size = Math.random() * 4 + 1;
      
      ctx.fillStyle = `rgba(147, 197, 253, ${0.4 + Math.random() * 0.4})`;
      ctx.beginPath();
      ctx.arc(offsetX, offsetY, size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Air Jet (Visuals) - improved
  if (sim.state.phase.includes("Air") && isRunning) {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.shadowColor = 'rgba(255, 255, 255, 0.3)';
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.moveTo(-4, 32);
    ctx.lineTo(0, 32 + Math.random() * 35 + 15);
    ctx.lineTo(4, 32);
    ctx.closePath();
    ctx.fill();
    ctx.shadowBlur = 0;
  }

  ctx.restore();
  
  // Draw velocity vector (for debugging/education)
  if (isRunning && (sim.state.vx !== 0 || sim.state.vy !== 0)) {
    ctx.save();
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2;
    ctx.setLineDash([3, 3]);
    
    const vScale = 0.5;
    const vx = sim.state.vx * vScale;
    const vy = sim.state.vy * vScale;
    
    ctx.beginPath();
    ctx.moveTo(rocketCanvasX, rocketCanvasY);
    ctx.lineTo(rocketCanvasX + vx, rocketCanvasY - vy);
    ctx.stroke();
    
    // Arrow head
    const angle = Math.atan2(-vy, vx);
    ctx.translate(rocketCanvasX + vx, rocketCanvasY - vy);
    ctx.rotate(angle);
    ctx.fillStyle = '#fbbf24';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-8, -4);
    ctx.lineTo(-8, 4);
    ctx.closePath();
    ctx.fill();
    
    ctx.restore();
  }
  
  // Scale indicator
  ctx.save();
  ctx.fillStyle = '#64748b';
  ctx.font = '12px Inter';
  ctx.fillText(`Escala: ${(1/currentScale).toFixed(2)} m/px`, 10, canvas.height - 70);
  ctx.restore();
}

// Start
init();
