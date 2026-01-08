"""
AXIOM RE - The Constitutional Bridge.
Version: 1.0.0 (Gold Edition)
Copyright (c) 2026 Chacha Mwise / Aquaflux Tech.
License: AXIOM Public License (APL-1.0)
--------------------------------------------------
STATELESS VERIFICATION LAYER.
This module acts as the binary gatekeeper for control actions.
It utilizes the PhysicsKernel to predict state violations before execution.
"""
from .core import PhysicsKernel

def axiom_permission_check(machine_dna: dict, current_state: dict, proposed_action: dict) -> dict:
    """
    Stateless verification function that audits a proposed control action against physical invariants.
    
    This function:
    1. Instantiates a temporary PhysicsKernel based on Machine DNA.
    2. Projects the proposed action into a future state ($\hat{s}_{t+1}$).
    3. Checks $\hat{s}_{t+1}$ against defined safety limits.
    
    Args:
        machine_dna (dict): Configuration containing 'max_potential', 'max_flux', 'rated_power'.
        current_state (dict): Telemetry data (unused in v1.0 Kernel, reserved for v2.0 State Estimation).
        proposed_action (dict): Intent vector containing 'ratio' (0.0-1.5) or 'hz'.
    
    Returns:
        dict: A Verdict Object containing:
              - 'status': "APPROVED" | "BLOCKED"
              - 'reasons': List of violation codes.
              - 'safe_action': The substituted safe command (if blocked).
              - 'efficiency_index': Calculated physical efficiency (0.0 - 1.0).
    """
    
    # --- 1. KERNEL INSTANTIATION (Just-In-Time) ---
    # The Bridge extracts parameters to build the Law for this specific machine.
    # Helper to safely get keys (handles 'max_head' vs 'max_pressure')
    def _get_param(keys, default=1.0):
        for k in keys:
            if k in machine_dna: return float(machine_dna[k])
        return default

    max_p = _get_param(['max_potential', 'max_head', 'max_voltage', 'max_pressure'])
    max_f = _get_param(['max_flux', 'max_flow', 'max_current', 'max_airflow'])
    rated_p = _get_param(['rated_power', 'power_rating'])

    # The Kernel is instantiated, used for calculation, and discarded (Stateless).
    kernel = PhysicsKernel(max_potential=max_p, max_flux=max_f, rated_power=rated_p)

    # --- 2. INTENT NORMALIZATION ---
    # Converts domain-specific units into a Universal Ratio ($\rho$)
    if 'ratio' in proposed_action:
        ratio = float(proposed_action['ratio'])
    elif 'hz' in proposed_action:
        ratio = float(proposed_action['hz']) / 50.0
    elif 'setpoint' in proposed_action:
        ratio = float(proposed_action['setpoint']) / (max_f if max_f > 0 else 1.0)
    else:
        ratio = 0.0 # Default Safe State

    # --- 3. PHYSICS PROJECTION (The Prediction) ---
    # Project Potential Energy ($\hat{P}$)
    predicted_potential = kernel.MAX_POTENTIAL * (ratio**2)
    # Project Flux ($\hat{F}$) via System Curve Intersection
    predicted_flux = kernel.solve_geometric_flux(predicted_potential, ratio)

    # --- 4. CONSTITUTIONAL CHECK (The Guardrails) ---
    violations = []
    
    # Invariant A: System Integrity (Container Limit)
    # Default safe limit is 110% of Max Potential if not specified
    safe_limit = _get_param(['safe_potential_limit', 'safe_pressure_limit', 'safe_voltage_limit'], kernel.MAX_POTENTIAL * 1.1)
    
    if predicted_potential > safe_limit:
        violations.append("CRITICAL: POTENTIAL_LIMIT_EXCEEDED (Integrity Risk)")

    # Invariant B: Component Health (Flux Limit)
    flux_limit = kernel.MAX_FLUX * 1.1
    if predicted_flux > flux_limit:
        violations.append("CRITICAL: FLUX_LIMIT_EXCEEDED (Component Damage Risk)")

    # Invariant C: Polarity
    if ratio < 0:
        violations.append("CRITICAL: REVERSE_POLARITY (Logic Error)")

    # --- 5. VERDICT GENERATION ---
    if violations:
        # INTERVENTION: Force Zero Energy State
        return {
            "status": "BLOCKED",
            "reasons": violations,
            "safe_action": {"ratio": 0.0},
            "efficiency_index": 0.0
        }
    else:
        # APPROVAL: Calculate Physical Efficiency (Output / Input)
        # This serves as a 'Truth Signal' for any attached AI agent.
        if ratio > 0.01:
            efficiency = (predicted_flux / kernel.MAX_FLUX) / ratio
        else:
            efficiency = 0.0
            
        return {
            "status": "APPROVED",
            "reasons": ["COMPLIANT"],
            "safe_action": proposed_action,
            "efficiency_index": min(1.0, efficiency)
        }