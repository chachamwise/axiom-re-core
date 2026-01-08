"""
AXIOM RE - The Universal Physics Engine.
Version: 1.0.0 (Gold Edition)
Copyright (c) 2026 Chacha Mwise / Aquaflux Tech.
License: AXIOM Public License (APL-1.0)
--------------------------------------------------
SEALED KERNEL. DO NOT MODIFY.
"""
import math

__version__ = "1.0.0"

class PhysicsKernel:
    """
    Stateless deterministic evaluator of physical invariants.
    
    This kernel implements algebraic enforcement of Affinity Laws and Dimensional Analysis
    to predict future states (Potential, Flux) based on control ratios.
    
    It contains no control policy, no learning parameters, and no internal state.
    
    Attributes:
        MAX_POTENTIAL (float): The physical limit of potential energy (Head, Voltage, Pressure).
        MAX_FLUX (float): The physical limit of flow rate (Flow, Current, Velocity).
        B_FACTOR (float): Derived system resistance coefficient describing the impedance curve.
    """
    
    def __init__(self, max_potential: float, max_flux: float, rated_power: float):
        """
        Initializes the immutable physics constants for a specific machine.
        
        Args:
            max_potential (float): Maximum rating for Head (m), Voltage (V), or Pressure (bar).
            max_flux (float): Maximum rating for Flow (m3/h), Current (A), or Velocity (m/s).
            rated_power (float): Rated power consumption (kW) at nominal operation point.
        """
        # Defensive Input Sanitization: Ensure strictly positive magnitude
        self.MAX_POTENTIAL = abs(float(max_potential)) if abs(float(max_potential)) > 0 else 1.0
        self.MAX_FLUX = abs(float(max_flux))
        self.RATED_POWER = abs(float(rated_power))
        
        # Derivation of System Impedance (B_FACTOR)
        # Assumption: Nominal operation occurs at approx 85% of Max Potential.
        # Physics Model: Potential_Loss = B_Factor * Flux^2
        p_rated_est = self.MAX_POTENTIAL * 0.85 
        
        if self.MAX_FLUX > 0.001:
            self.B_FACTOR = (self.MAX_POTENTIAL - p_rated_est) / (self.MAX_FLUX**2)
        else:
            self.B_FACTOR = 1.0

    def solve_geometric_flux(self, current_potential: float, ratio: float = 1.0) -> float:
        """
        Predicts Flow/Flux based on the intersection of the Pump Curve and System Curve.
        
        Formula: Flux = sqrt( (Limit - Current_Potential) / B_Factor )
        
        Args:
            current_potential (float): The opposing force (Static Head, Grid Voltage).
            ratio (float): The normalized control input (0.0 - 1.5).
            
        Returns:
            float: Predicted Flux. Returns 0.0 if physics limits are exceeded.
        """
        # Clamp ratio to prevent unbounded energy projection
        ratio = max(0.0, min(1.5, ratio))
        
        # Affinity Law: Potential scales with square of speed (ratio)
        potential_limit = self.MAX_POTENTIAL * (ratio**2)
        
        # Physical Constraint: Flow cannot occur if opposing potential exceeds generation
        if current_potential >= potential_limit or current_potential < 0:
            return 0.0
            
        delta = potential_limit - current_potential
        try:
            return math.sqrt(delta / self.B_FACTOR)
        except (ValueError, ZeroDivisionError):
            return 0.0

    def analyze_variance(self, real_val: float, expected_val: float) -> float:
        """
        Calculates the deviation ratio between Observed Physics and Theoretical Physics.
        Used for anomaly detection (Cavitation, Leakage, Sensor Drift).
        
        Returns:
            float: Variance Ratio (1.0 = Ideal). 
                   > 1.0 implies System Impedance drop (Leak/Burst).
                   < 1.0 implies System Impedance rise (Blockage).
        """
        if expected_val < 0.0001: 
            return 1.0 # Singularity prevention
        return real_val / expected_val

    def get_version(self):
        return __version__