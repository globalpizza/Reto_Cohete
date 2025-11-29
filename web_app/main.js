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
  v_water: document.getElementById('v_water'),
  m_rocket: document.getElementById('m_rocket'),
  cd: document.getElementById('cd'),
  a_nozzle: document.getElementById('a_nozzle')
};

// Displays
const displays = {
  p_psi: document.getElementById('val_p_psi'),
  v_water: document.getElementById('val_v_water'),
  m_rocket: document.getElementById('val_m_rocket'),
  cd: document.getElementById('val_cd'),
  a_nozzle: document.getElementById('val_a_nozzle')
};

// Stats
const stats = {
  phase: document.getElementById('stat-phase'),
  height: document.getElementById('stat-height'),
  velocity: document.getElementById('stat-velocity'),
  water: document.getElementById('stat-water'),
  maxHeight: document.getElementById('max-height'),
  maxSpeed: document.getElementById('max-speed')
};

// Buttons
const btnLaunch = document.getElementById('btn-launch');
const btnReset = document.getElementById('btn-reset');

// --- State ---
let sim = null;
let animationId = null;
let isRunning = false;
let scale = 10; // Pixels per meter (initial)
let cameraY = 0; // Camera vertical position
let maxH = 0;
let maxV = 0;

// --- Initialization ---
function init() {
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  // Bind inputs
  Object.keys(inputs).forEach(key => {
    inputs[key].addEventListener('input', (e) => {
      updateDisplay(key, e.target.value);
      if (!isRunning) resetSimulation(); // Live preview reset
    });
  });

  btnLaunch.addEventListener('click', startLaunch);
  btnReset.addEventListener('click', resetSimulation);

  resetSimulation();
  draw(); // Initial draw
}

function resizeCanvas() {
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  draw();
}

function updateDisplay(key, value) {
  let suffix = '';
  if (key === 'p_psi') suffix = ' psi';
  if (key === 'v_water') suffix = ' L';
  if (key === 'm_rocket') suffix = ' g';
  if (key === 'a_nozzle') suffix = ' cm²';

  displays[key].textContent = value + suffix;
}

function getParams() {
  return {
    p_manometric_psi: parseFloat(inputs.p_psi.value),
    V_r_L: 2.0, // Fixed bottle volume for now as per original script default, or could be added
    V_0w_L: parseFloat(inputs.v_water.value),
    A_e_cm2: parseFloat(inputs.a_nozzle.value),
    A_r_cm2: 95.0,
    M_r_g: parseFloat(inputs.m_rocket.value),
    H_tube_m: 1.0,
    C_D: parseFloat(inputs.cd.value),
    A_ref_cm2: 100.0
  };
}

function resetSimulation() {
  cancelAnimationFrame(animationId);
  isRunning = false;
  sim = new RocketSimulation(getParams());
  maxH = 0;
  maxV = 0;
  cameraY = 0;

  // Reset stats
  stats.phase.textContent = "Listo";
  stats.phase.className = "stat-value phase-ready";
  stats.height.textContent = "0.0 m";
  stats.velocity.textContent = "0.0 km/h";
  stats.water.textContent = "100%";
  stats.maxHeight.textContent = "0.0";
  stats.maxSpeed.textContent = "0.0";

  draw();
}

function startLaunch() {
  if (isRunning) return;
  resetSimulation(); // Ensure fresh start
  isRunning = true;
  lastTime = performance.now();
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
  const v = sim.state.v;
  const v_kmh = v * 3.6;

  if (h > maxH) maxH = h;
  if (v_kmh > maxV) maxV = v_kmh;

  stats.height.textContent = h.toFixed(1) + " m";
  stats.velocity.textContent = v_kmh.toFixed(1) + " km/h";

  const waterPercent = (sim.state.M_w / (sim.params.V_0w * RHO_W)) * 100;
  stats.water.textContent = Math.max(0, waterPercent).toFixed(0) + "%";

  stats.maxHeight.textContent = maxH.toFixed(1);
  stats.maxSpeed.textContent = maxV.toFixed(1);

  // Phase styling
  let phaseClass = "phase-ready";
  if (sim.state.phase.includes("Water")) phaseClass = "phase-water";
  if (sim.state.phase.includes("Air")) phaseClass = "phase-air";
  if (sim.state.phase.includes("Ballistic")) phaseClass = "phase-ballistic";

  stats.phase.textContent = sim.state.phase;
  stats.phase.className = "stat-value " + phaseClass;

  draw();

  if (isRunning) {
    animationId = requestAnimationFrame(loop);
  }
}

// --- Drawing ---
function draw() {
  // Clear
  ctx.fillStyle = '#0f172a'; // Match bg
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Camera Logic
  // Keep rocket in middle vertically, but don't go below ground
  const targetCamY = sim.state.y * scale;
  // Smooth follow
  // cameraY = targetCamY; 
  // Actually, let's map simulation Y to canvas Y.
  // Ground is at canvas.height - 50.
  // Up is negative Y in canvas.

  // Dynamic Scale: Zoom out as it goes higher
  // Base scale 20px/m. If height > 20m, reduce scale.
  let currentScale = 20;
  if (sim.state.y > 10) {
    currentScale = 200 / (sim.state.y + 1); // rough zoom out
    if (currentScale < 2) currentScale = 2; // Min scale
  }

  const groundY = canvas.height - 50;
  const rocketCanvasY = groundY - (sim.state.y * currentScale);

  // Draw Ground
  ctx.fillStyle = '#22c55e';
  ctx.fillRect(0, groundY, canvas.width, 50);

  // Draw Grid/Sky hints
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let h = 10; h < 1000; h += 10) {
    const y = groundY - (h * currentScale);
    if (y < 0) break;
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.fillStyle = '#64748b';
    ctx.fillText(h + 'm', 10, y - 2);
  }
  ctx.stroke();

  // Draw Rocket
  ctx.save();
  ctx.translate(canvas.width / 2, rocketCanvasY);

  // Rocket Body
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

  // Water Jet (Visuals)
  if (sim.state.phase.includes("Water") && isRunning) {
    ctx.fillStyle = 'rgba(59, 130, 246, 0.8)';
    ctx.beginPath();
    ctx.moveTo(-5, 30);
    ctx.lineTo(0, 30 + Math.random() * 50 + 20);
    ctx.lineTo(5, 30);
    ctx.fill();

    // Particles
    for (let i = 0; i < 5; i++) {
      ctx.fillStyle = 'rgba(147, 197, 253, 0.6)';
      ctx.beginPath();
      ctx.arc((Math.random() - 0.5) * 10, 30 + Math.random() * 40, Math.random() * 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Air Jet (Visuals)
  if (sim.state.phase.includes("Air") && isRunning) {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.beginPath();
    ctx.moveTo(-5, 30);
    ctx.lineTo(0, 30 + Math.random() * 30);
    ctx.lineTo(5, 30);
    ctx.fill();
  }

  ctx.restore();
}

// Start
init();
