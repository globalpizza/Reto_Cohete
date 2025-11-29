/**
 * physics.ts
 * Core physics logic for Water Rocket Simulation.
 * Implements Runge-Kutta 4 (RK4) integration for high precision.
 */

// --- CONSTANTS (SI) ---
export const RHO_W = 997.0;          // kg/m^3
export const G = 9.81;               // m/s^2
export const GAMMA = 1.4;            // Adiabatic index
export const RHO_AIR = 1.225;        // kg/m^3
export const P_ATM = 101325.0;       // Pa

// --- TYPES ---
export interface SimulationParams {
  p_manometric_psi: number;
  V_r_L: number;
  V_0w_L: number;
  A_e_cm2: number;
  A_r_cm2: number;
  M_r_g: number;
  H_tube_m: number;
  C_D: number;
  A_ref_cm2: number;
}

export interface SimulationState {
  y: number;      // Position (m)
  v: number;      // Velocity (m/s)
  M_w: number;    // Water Mass (kg)
  t: number;      // Time (s)
  phase: 'Launch Tube' | 'Water Thrust' | 'Air Thrust' | 'Ballistic';
}

export interface SIParams {
  P_i_abs: number;
  V_r: number;
  V_0w: number;
  A_e: number;
  A_r: number;
  M_r: number;
  H_tube: number;
  C_D: number;
  A_ref: number;
}

// --- CONVERSION ---
export function convertToSI(params: SimulationParams): SIParams {
  return {
    P_i_abs: (params.p_manometric_psi * 6894.76) + P_ATM,
    V_r: params.V_r_L / 1000.0,
    V_0w: params.V_0w_L / 1000.0,
    A_e: params.A_e_cm2 / 10000.0,
    A_r: params.A_r_cm2 / 10000.0,
    M_r: params.M_r_g / 1000.0,
    H_tube: params.H_tube_m,
    C_D: params.C_D,
    A_ref: params.A_ref_cm2 / 10000.0
  };
}

// --- PHYSICS FUNCTIONS ---

function calculatePressure(M_w: number, params: SIParams): number {
  const V_w = M_w / RHO_W;
  const V_air = params.V_r - V_w;
  const V_air_0 = params.V_r - params.V_0w;

  if (V_air <= 0) return P_ATM;

  // Adiabatic expansion: P * V^gamma = const
  return params.P_i_abs * Math.pow(V_air_0 / V_air, GAMMA);
}

function calculateEscapeVelocity(P: number, M_w: number, params: SIParams): number {
  const V_w = M_w / RHO_W;
  const h_diff = V_w / params.A_r;

  const areaFactor = Math.pow(params.A_r, 2) / (Math.pow(params.A_r, 2) - Math.pow(params.A_e, 2));

  const termPressure = 2.0 * areaFactor * (P - P_ATM) / RHO_W;
  const termGravity = 2.0 * G * areaFactor * h_diff;

  if (termPressure + termGravity < 0) return 0.0;
  return Math.sqrt(termPressure + termGravity);
}

function calculateDrag(v: number, params: SIParams): number {
  return 0.5 * RHO_AIR * Math.pow(v, 2) * params.C_D * params.A_ref;
}

// Derivative vector: [dy/dt, dv/dt, dMw/dt]
type Derivatives = [number, number, number];

function getDerivatives(state: SimulationState, params: SIParams): Derivatives {
  const { v, M_w } = state;
  let dMw_dt = 0.0;
  let thrust = 0.0;
  let M_total = params.M_r;

  // Physics Phase Logic
  if (M_w > 1e-5) {
    const P = calculatePressure(M_w, params);
    const u_e = calculateEscapeVelocity(P, M_w, params);

    dMw_dt = -RHO_W * params.A_e * u_e;
    thrust = -dMw_dt * u_e;
    M_total += M_w;
  } else {
    // Air/Ballistic
    M_total = params.M_r;
    thrust = 0.0;
    dMw_dt = 0.0;
  }

  const F_D = calculateDrag(v, params);
  const gravity = M_total * G;

  const dy_dt = v;
  const dv_dt = (thrust - gravity - Math.sign(v) * F_D) / M_total;

  return [dy_dt, dv_dt, dMw_dt];
}

// --- RK4 INTEGRATOR ---

export function rk4Step(state: SimulationState, params: SIParams, dt: number): SimulationState {
  // Unpack state for vector math
  const y0 = state.y;
  const v0 = state.v;
  const mw0 = state.M_w;

  // Helper to create a temp state for intermediate k steps
  const tempState = (dy: number, dv: number, dmw: number): SimulationState => ({
    ...state,
    y: y0 + dy,
    v: v0 + dv,
    M_w: Math.max(0, mw0 + dmw) // Clamp mass
  });

  // k1
  const [k1_y, k1_v, k1_mw] = getDerivatives(state, params);

  // k2
  const s2 = tempState(k1_y * dt * 0.5, k1_v * dt * 0.5, k1_mw * dt * 0.5);
  const [k2_y, k2_v, k2_mw] = getDerivatives(s2, params);

  // k3
  const s3 = tempState(k2_y * dt * 0.5, k2_v * dt * 0.5, k2_mw * dt * 0.5);
  const [k3_y, k3_v, k3_mw] = getDerivatives(s3, params);

  // k4
  const s4 = tempState(k3_y * dt, k3_v * dt, k3_mw * dt);
  const [k4_y, k4_v, k4_mw] = getDerivatives(s4, params);

  // Combine
  const y_new = y0 + (dt / 6.0) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y);
  const v_new = v0 + (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v);
  const mw_new = Math.max(0, mw0 + (dt / 6.0) * (k1_mw + 2 * k2_mw + 2 * k3_mw + k4_mw));

  // Determine Phase for UI
  let phase: SimulationState['phase'] = 'Ballistic';

  if (y_new < params.H_tube) {
    phase = 'Launch Tube';
  } else if (mw_new > 1e-4) {
    phase = 'Water Thrust';
  } else {
    const P = calculatePressure(mw_new, params);
    if (P > P_ATM && mw_new <= 1e-4) {
      phase = 'Air Thrust';
    } else {
      phase = 'Ballistic';
    }
  }

  return {
    y: y_new,
    v: v_new,
    M_w: mw_new,
    t: state.t + dt,
    phase: phase
  };
}
