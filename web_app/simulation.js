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
      A_ref: inputParams.A_ref_cm2 / 10000.0,
      launch_angle_rad: (inputParams.launch_angle_deg || 45) * Math.PI / 180.0
    };
  }

  reset() {
    // State: [x, y, vx, vy, M_w]
    const M_0w = this.params.V_0w * RHO_W;
    this.state = {
      x: 0.0,
      y: 0.0,
      vx: 0.0,
      vy: 0.0,
      M_w: M_0w,
      t: 0.0,
      phase: 'Launch Tube'
    };
    this.history = [];
    this.flightActive = true;
    this.maxHeightReached = false;
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

  calculateDrag(vx, vy) {
    // Calculate drag in 2D
    const v_total = Math.sqrt(vx * vx + vy * vy);
    if (v_total < 1e-6) return { F_Dx: 0.0, F_Dy: 0.0 };
    
    const F_D_mag = 0.5 * RHO_AIR * v_total * v_total * this.params.C_D * this.params.A_ref;
    const F_Dx = -F_D_mag * (vx / v_total);
    const F_Dy = -F_D_mag * (vy / v_total);
    
    return { F_Dx, F_Dy };
  }

  derivatives(state) {
    const { x, y, vx, vy, M_w } = state;
    let dMw_dt = 0.0;
    let thrust_x = 0.0;
    let thrust_y = 0.0;
    let M_total = this.params.M_r;

    if (M_w > 1e-5) {
      const P = this.calculatePressure(M_w);
      const u_e = this.calculateEscapeVelocity(P, M_w);

      dMw_dt = -RHO_W * this.params.A_e * u_e;
      const thrust_mag = -dMw_dt * u_e;
      
      // Determine thrust direction
      const v_total = Math.sqrt(vx * vx + vy * vy);
      if (v_total > 1e-3) {
        // Use velocity direction
        thrust_x = thrust_mag * (vx / v_total);
        thrust_y = thrust_mag * (vy / v_total);
      } else {
        // Use launch angle
        thrust_x = thrust_mag * Math.cos(this.params.launch_angle_rad);
        thrust_y = thrust_mag * Math.sin(this.params.launch_angle_rad);
      }
      
      M_total += M_w;
    } else {
      M_total = this.params.M_r;
      thrust_x = 0.0;
      thrust_y = 0.0;
      dMw_dt = 0.0;
    }

    const drag = this.calculateDrag(vx, vy);
    const gravity_y = -M_total * G;

    const dx_dt = vx;
    const dy_dt = vy;
    const dvx_dt = (thrust_x + drag.F_Dx) / M_total;
    const dvy_dt = (thrust_y + drag.F_Dy + gravity_y) / M_total;

    return { dx_dt, dy_dt, dvx_dt, dvy_dt, dMw_dt, thrust_x, thrust_y };
  }

  step() {
    if (!this.flightActive) return;

    const derivs = this.derivatives(this.state);

    // Euler Step
    this.state.x += derivs.dx_dt * DT;
    this.state.y += derivs.dy_dt * DT;
    this.state.vx += derivs.dvx_dt * DT;
    this.state.vy += derivs.dvy_dt * DT;
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
        this.state.phase = 'Air Thrust';
      } else {
        this.state.phase = 'Ballistic';
      }
    }

    // Track max height for termination
    if (this.state.vy < 0 && !this.maxHeightReached) {
      this.maxHeightReached = true;
    }

    // Ground collision
    if (this.state.y <= 0 && this.maxHeightReached) {
      this.state.y = 0;
      this.state.vx = 0;
      this.state.vy = 0;
      this.flightActive = false;
    }

    // Store history
    if (this.state.t % 0.1 < DT) {
      this.history.push({ ...this.state });
    }
  }
}
