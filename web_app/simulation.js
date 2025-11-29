/**
 * simulation.js
 * Port of Python rocket simulation logic to JavaScript.
 */

// --- CONSTANTS (SI) ---
const RHO_W = 997.0;          // kg/m^3
const G = 9.81;               // m/s^2
const GAMMA = 1.4;            // Adiabatic index
const RHO_AIR = 1.225;        // kg/m^3
const P_ATM = 101325.0;       // Pa
const DT = 0.005;             // Time step (s) - slightly larger for JS perf if needed

class RocketSimulation {
  constructor(params) {
    this.params = this.convertToSI(params);
    this.reset();
  }

  convertToSI(inputParams) {
    return {
      P_i_abs: (inputParams.p_manometric_psi * 6894.76) + P_ATM,
      V_r: inputParams.V_r_L / 1000.0,
      V_0w: inputParams.V_0w_L / 1000.0,
      A_e: inputParams.A_e_cm2 / 10000.0,
      A_r: inputParams.A_r_cm2 / 10000.0,
      M_r: inputParams.M_r_g / 1000.0,
      H_tube: inputParams.H_tube_m,
      C_D: inputParams.C_D,
      A_ref: inputParams.A_ref_cm2 / 10000.0
    };
  }

  reset() {
    // State: [y, v, M_w]
    const M_0w = this.params.V_0w * RHO_W;
    this.state = {
      y: 0.0,
      v: 0.0,
      M_w: M_0w,
      t: 0.0,
      phase: 'Launch Tube'
    };
    this.history = [];
    this.flightActive = true;
  }

  calculatePressure(M_w) {
    const V_w = M_w / RHO_W;
    const V_air = this.params.V_r - V_w;
    const V_air_0 = this.params.V_r - this.params.V_0w;

    if (V_air <= 0) return P_ATM; // Should not happen if V_0w < V_r

    // Adiabatic expansion
    return this.params.P_i_abs * Math.pow(V_air_0 / V_air, GAMMA);
  }

  calculateEscapeVelocity(P, M_w) {
    const V_w = M_w / RHO_W;
    const h_diff = V_w / this.params.A_r;

    const areaFactor = Math.pow(this.params.A_r, 2) / (Math.pow(this.params.A_r, 2) - Math.pow(this.params.A_e, 2));

    const termPressure = 2.0 * areaFactor * (P - P_ATM) / RHO_W;
    const termGravity = 2.0 * G * areaFactor * h_diff;

    if (termPressure + termGravity < 0) return 0.0;
    return Math.sqrt(termPressure + termGravity);
  }

  calculateDrag(v) {
    // F_D = 0.5 * rho * v^2 * Cd * A
    return 0.5 * RHO_AIR * Math.pow(v, 2) * this.params.C_D * this.params.A_ref;
  }

  derivatives(state) {
    const { y, v, M_w } = state;
    let dMw_dt = 0.0;
    let thrust = 0.0;
    let M_total = this.params.M_r;

    // Phase determination for physics
    // Note: 'Launch Tube' phase logic is simplified here to behave like Water phase 
    // but physically constrained by the tube (not implemented in detail in the python script, 
    // so we follow the python script's approach of integrating it as water phase).

    if (M_w > 1e-5) {
      const P = this.calculatePressure(M_w);
      const u_e = this.calculateEscapeVelocity(P, M_w);

      dMw_dt = -RHO_W * this.params.A_e * u_e;
      thrust = -dMw_dt * u_e;
      M_total += M_w;
    } else {
      // Air/Ballistic
      M_total = this.params.M_r;
      thrust = 0.0;
      dMw_dt = 0.0;
    }

    const F_D = this.calculateDrag(v);
    const gravity = M_total * G;

    const dy_dt = v;
    const dv_dt = (thrust - gravity - Math.sign(v) * F_D) / M_total;

    return { dy_dt, dv_dt, dMw_dt, thrust };
  }

  step() {
    if (!this.flightActive) return;

    const derivs = this.derivatives(this.state);

    // Euler Step
    this.state.y += derivs.dy_dt * DT;
    this.state.v += derivs.dv_dt * DT;
    this.state.M_w += derivs.dMw_dt * DT;
    this.state.t += DT;

    // Boundary checks
    if (this.state.M_w < 0) this.state.M_w = 0.0;

    // Phase Update
    if (this.state.y < this.params.H_tube) {
      this.state.phase = 'Launch Tube';
    } else if (this.state.M_w > 1e-4) {
      this.state.phase = 'Water Thrust';
    } else {
      const P = this.calculatePressure(this.state.M_w);
      if (P > P_ATM && this.state.M_w <= 1e-4) {
        this.state.phase = 'Air Thrust'; // Short phase
      } else {
        this.state.phase = 'Ballistic';
      }
    }

    // Ground collision
    if (this.state.phase === 'Ballistic' && this.state.y <= 0 && this.state.v < 0) {
      this.state.y = 0;
      this.state.v = 0;
      this.flightActive = false;
    }

    // Store history for plotting if needed (limiting size)
    if (this.state.t % 0.1 < DT) {
      this.history.push({ ...this.state });
    }
  }
}
