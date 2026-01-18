"""
AXIOM RE - The Constitutional Bridge.
Version: 1.0.1 (Dual-License Ready)
Copyright (c) 2026 Chacha Mwise / Aquaflux Tech.
License: AXIOM Public License (APL-1.0)
--------------------------------------------------
STATELESS VERIFICATION LAYER.
This module acts as the binary gatekeeper for control actions.
It utilizes the PhysicsKernel to predict state violations before execution.
"""
import hashlib
import os
from .core import PhysicsKernel

# --- INTEGRITY CONFIGURATION ---
CERTIFIED_HASH = "8922F9355FD86A98AFF7BC8B8184D3BE8C24DCA0BC50D49984D621FA3EE7C1A6"

def _verify_kernel_integrity() -> bool:
    """Internal function to validate the PhysicsKernel signature on import."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        core_path = os.path.join(current_dir, "core.py")
        
        with open(core_path, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
            
        if current_hash != CERTIFIED_HASH:
            print(f"[AXIOM SECURITY] ⚠️ KERNEL MISMATCH. Expected: {CERTIFIED_HASH[:8]}...")
            return False
        return True
    except Exception:
        return False

# Execute Security Check on Module Import
KERNEL_IS_SECURE = _verify_kernel_integrity()


def axiom_permission_check(machine_dna: dict, current_state: dict, proposed_action: dict) -> dict:
    """
    Stateless verification function that audits a proposed control action against physical invariants.
    
    This function:
    1. Instantiates a temporary PhysicsKernel based on Machine DNA.
    2. Projects the proposed action into a future state ($\hat{s}_{t+1}$).
    3. Checks $\hat{s}_{t+1}$ against defined safety limits.
    
    Args:
        machine_dna (dict): Configuration containing 'max_potential', 'max_flux', 'rated_power'.
        current_state (dict): Telemetry data (unused in v1.0 Kernel).
        proposed_action (dict): Intent vector containing 'ratio' (0.0-1.5) or 'hz'.
    
    Returns:
        dict: A Verdict Object containing 'status', 'reasons', 'safe_action', 'efficiency_index'.
    """
    
    # --- 0. SECURITY GATE ---
    if not KERNEL_IS_SECURE:
        return {
            "status": "BLOCKED",
            "reasons": ["CRITICAL: KERNEL_TAMPERING_DETECTED"],
            "safe_action": {"ratio": 0.0},
            "efficiency_index": 0.0
        }

    # --- 1. KERNEL INSTANTIATION (Just-In-Time) ---
    def _get_param(keys, default=1.0):
        for k in keys:
            if k in machine_dna: return float(machine_dna[k])
        return default

    max_p = _get_param(['max_potential', 'max_head', 'max_voltage', 'max_pressure'])
    max_f = _get_param(['max_flux', 'max_flow', 'max_current', 'max_airflow'])
    rated_p = _get_param(['rated_power', 'power_rating'])

    kernel = PhysicsKernel(max_potential=max_p, max_flux=max_f, rated_power=rated_p)

    # --- 2. INTENT NORMALIZATION ---
    if 'ratio' in proposed_action:
        ratio = float(proposed_action['ratio'])
    elif 'hz' in proposed_action:
        ratio = float(proposed_action['hz']) / 50.0
    elif 'setpoint' in proposed_action:
        ratio = float(proposed_action['setpoint']) / (max_f if max_f > 0 else 1.0)
    else:
        ratio = 0.0 

    # --- 3. PHYSICS PROJECTION ---
    # Scenario A: Maximum Potential (Zero Flow Condition)
    predicted_potential_max = kernel.MAX_POTENTIAL * (ratio**2)
    
    # Scenario B: Maximum Flux (Zero Resistance Condition)
    predicted_flux_max = kernel.solve_geometric_flux(current_potential=0.0, ratio=ratio)

    # --- 4. CONSTITUTIONAL CHECK ---
    violations = []
    
    # Invariant A: System Integrity
    safe_limit_p = _get_param(['safe_potential_limit', 'safe_pressure_limit'], kernel.MAX_POTENTIAL * 1.1)
    if predicted_potential_max > safe_limit_p:
        violations.append(f"CRITICAL: POTENTIAL_LIMIT_EXCEEDED (Pred: {predicted_potential_max:.1f} > Limit: {safe_limit_p:.1f})")

    # Invariant B: Component Health
    safe_limit_f = kernel.MAX_FLUX * 1.1
    if predicted_flux_max > safe_limit_f:
        violations.append(f"CRITICAL: FLUX_LIMIT_EXCEEDED (Pred: {predicted_flux_max:.1f} > Limit: {safe_limit_f:.1f})")

    # Invariant C: Polarity
    if ratio < 0:
        violations.append("CRITICAL: REVERSE_POLARITY (Logic Error)")

    # --- 5. VERDICT GENERATION ---
    if violations:
        return {
            "status": "BLOCKED",
            "reasons": violations,
            "safe_action": {"ratio": 0.0},
            "efficiency_index": 0.0
        }
    else:
        efficiency = ((predicted_flux_max / kernel.MAX_FLUX) / ratio) if ratio > 0.01 else 0.0
        return {
            "status": "APPROVED",
            "reasons": ["COMPLIANT"],
            "safe_action": proposed_action,
            "efficiency_index": min(1.0, efficiency)
        }