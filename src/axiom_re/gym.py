"""
AXIOM GYM - Universal Digital Twin Environment.
Version: 1.0.0 (Gold Edition)
Copyright (c) 2026 Chacha Mwise / Aquaflux Tech.
License: AXIOM Public License (APL-1.0)
--------------------------------------------------
PHYSICS-BASED SIMULATION.
Provides a deterministic training ground for AI agents.
State transitions are calculated using the PhysicsKernel.
"""
from .core import PhysicsKernel

class AxiomGym:
    """
    A lightweight Digital Twin that morphs based on Machine DNA.
    Compatible with Reinforcement Learning loops (Step/Reset).
    """
    
    def __init__(self, machine_dna: dict):
        """
        Initializes the simulation environment.
        
        Args:
            machine_dna (dict): Configuration defining the physics boundaries.
        """
        self.dna = machine_dna
        
        # --- 1. AUTO-DETECT PHYSICS DOMAIN ---
        def _get(keys, default=0.0):
            for k in keys:
                if k in self.dna: return float(self.dna[k])
            return default

        max_p = _get(['max_head', 'max_voltage', 'max_pressure', 'max_speed'])
        max_f = _get(['max_flow', 'max_current', 'max_airflow', 'max_tonnage'])
        rated_w = _get(['rated_power', 'power_rating'], 10.0)
        
        # --- 2. INSTANTIATE THE KERNEL (The Physics Engine) ---
        self.kernel = PhysicsKernel(max_potential=max_p, max_flux=max_f, rated_power=rated_w)
        
        # --- 3. DEFINE ENVIRONMENT STATE ---
        # "Capacity" represents the maximum fill of the container (Tank, Battery, Silo)
        self.capacity = 100.0 
        self.current_fill = 0.0
        self.safety_limit = _get(['safe_pressure_limit', 'safe_voltage_limit', 'safe_speed_limit'], 9999.0)
        
        self.reset()

    def reset(self):
        """ Resets the environment to the initial state (Empty). """
        self.current_fill = 0.0
        self.state = {"potential_val": 0.0, "fill_level": 0.0}
        return self.state

    def step(self, action: dict):
        """
        Advances the simulation by one time-step.
        
        Args:
            action (dict): Action vector containing 'ratio' or 'hz'.
            
        Returns:
            tuple: (next_state, status)
        """
        # 1. PARSE ACTION
        if 'ratio' in action:
            ratio = float(action['ratio'])
        elif 'hz' in action:
            ratio = float(action['hz']) / 50.0
        else:
            ratio = 0.0

        # 2. CALCULATE PHYSICS (Using the Kernel)
        # Potential scales with square of ratio (Affinity Law)
        current_potential = self.kernel.MAX_POTENTIAL * (ratio ** 2)
        
        # 3. CHECK FOR CATASTROPHIC FAILURE
        # If the Physics Kernel predicts potential > limit, the component breaks.
        if current_potential > self.safety_limit:
            self.state["potential_val"] = round(current_potential, 2)
            return self.state, "CRASHED"

        # 4. CALCULATE FLUX (The Effect)
        # Resistance increases as the container fills (Back Pressure / Back EMF)
        resistance_back_pressure = self.kernel.MAX_POTENTIAL * (self.current_fill / self.capacity)
        
        # The Kernel solves the flow based on the difference between Applied Potential and Resistance
        effective_potential = current_potential - resistance_back_pressure
        
        # We use the kernel's geometric solver, treating effective_potential as the 'head loss' component
        # Note: This is a simplified dynamic simulation using the static kernel.
        current_flux = self.kernel.solve_geometric_flux(resistance_back_pressure, ratio)

        # 5. INTEGRATE TIME (State Update)
        # Fill Rate normalized against Max Flux
        fill_rate = current_flux / self.kernel.MAX_FLUX if self.kernel.MAX_FLUX > 0 else 0
        self.current_fill += fill_rate * 5.0 # Simulation speed multiplier
        
        # Clamp to Max
        if self.current_fill >= self.capacity:
            self.current_fill = self.capacity
            done_status = "SUCCESS"
        else:
            done_status = "RUNNING"

        # 6. OBSERVATION
        self.state = {
            "potential_val": round(current_potential, 2),
            "fill_level": round(self.current_fill, 2)
        }
        
        return self.state, done_status