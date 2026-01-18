"""
AXIOM EXPERIMENT: SAFETY INTEGRITY VERIFICATION
Comparative Analysis: Unconstrained Control vs. Axiom-Guarded Control.

This script executes a stochastic simulation to verify that the
Axiom Bridge correctly intercepts and modifies unsafe control signals
before they reach the physical environment.
"""
import sys
import os
import random
import pandas as pd

# 1. LIBRARY PATH CONFIGURATION
# The system must resolve the path to the local 'src' directory to ensure 
# the script utilizes the local library version rather than system packages.
# Path resolution: Current Dir (experiments) -> Parent (root) -> Source (src)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.append(src_path)

# 2. IMPORT AXIOM LIBRARY
# Import the 'axiom_re' package. Failure here indicates a directory structure mismatch.
try:
    from axiom_re import axiom_permission_check
except ImportError as e:
    print("CRITICAL ERROR: Failed to import 'axiom_re' library.")
    print(f"Search Path: {src_path}")
    print(f"Technical Details: {e}")
    print("Ensure you have created the 'src/axiom_re/__init__.py' file.")
    sys.exit(1)

# --- SIMULATION CONFIGURATION ---
EPISODES = 500
SAFE_LIMIT_PRESSURE = 9.5

# Machine Configuration (DNA) matching standard pump specifications
MACHINE_DNA = {
    'max_head': 10.0, 
    'max_flow': 50.0, 
    'rated_power': 15.0, 
    'safe_pressure_limit': SAFE_LIMIT_PRESSURE
}

class SimulatedEnvironment:
    """
    Simple physics environment representing a pressurized container.
    """
    def __init__(self):
        self.pressure = 0.0
    
    def step(self, control_ratio):
        # Deterministic Physics: Pressure ~= Ratio^2 * Max_Head
        # Stochastic Noise: +/- 0.1 to simulate sensor variance
        noise = random.uniform(-0.1, 0.1)
        self.pressure = (10.0 * (control_ratio**2)) + noise
        self.pressure = max(0.0, self.pressure)
        return self.pressure

def run_verification_test():
    env = SimulatedEnvironment()
    
    baseline_violations = 0
    guarded_violations = 0
    
    baseline_history = []
    guarded_history = []
    
    print(f"Starting Safety Verification Loop ({EPISODES} Episodes)...")

    for i in range(EPISODES):
        # --- 1. GENERATE CONTROL SIGNAL ---
        # Simulate a stochastic agent generating random inputs (0.0 - 1.1)
        # Note: Inputs > 0.975 will typically exceed the 9.5 pressure limit.
        raw_input_signal = random.uniform(0.0, 1.1) 
        
        # --- 2. BASELINE EXECUTION (Unconstrained) ---
        # The raw signal is passed directly to the environment.
        p_baseline = env.step(raw_input_signal)
        if p_baseline > SAFE_LIMIT_PRESSURE:
            baseline_violations += 1
        baseline_history.append(baseline_violations)

        # --- 3. AXIOM-GUARDED EXECUTION (Protected) ---
        intent_vector = {'ratio': raw_input_signal}
        
        # Verify signal against Physics Kernel via Bridge
        verdict = axiom_permission_check(MACHINE_DNA, {'pressure': 0.0}, intent_vector)
        
        if verdict['status'] == 'BLOCKED':
            # Signal was deemed unsafe; use the Kernel's safe fallback
            executed_action = verdict['safe_action']['ratio'] 
        else:
            # Signal was deemed safe; proceed with intent
            executed_action = raw_input_signal
            
        # Execute the validated action
        p_guarded = env.step(executed_action)
        
        # Check if the Kernel failed to prevent a violation
        if p_guarded > SAFE_LIMIT_PRESSURE:
            guarded_violations += 1 
        guarded_history.append(guarded_violations)

    return baseline_history, guarded_history

if __name__ == "__main__":
    baseline_data, guarded_data = run_verification_test()
    
    # Export results to CSV for audit trail
    df = pd.DataFrame({
        "Episode": range(EPISODES), 
        "Baseline_Violations": baseline_data, 
        "Axiom_Violations": guarded_data
    })
    
    output_path = os.path.join(current_dir, "axiom_safety_proof.csv")
    df.to_csv(output_path, index=False)
    
    # --- GENERATE CONSOLE SUMMARY ---
    baseline_fail_rate = (baseline_data[-1] / EPISODES) * 100
    guarded_fail_rate = (guarded_data[-1] / EPISODES) * 100

    print("\n" + "="*60)
    print(f"📊 AXIOM CORE: INTEGRITY VERIFICATION REPORT")
    print("="*60)
    print(f"Sample Size:            {EPISODES} Episodes")
    print(f"Safety Limit:           {SAFE_LIMIT_PRESSURE} Units")
    print("-" * 60)
    print(f"Baseline (Unprotected): {baseline_data[-1]} Violations ({baseline_fail_rate:.1f}%)")
    print(f"Axiom Guarded:          {guarded_data[-1]} Violations ({guarded_fail_rate:.1f}%)")
    print("-" * 60)
    
    if guarded_data[-1] == 0:
        print("✅ PASS: Integrity Verified. Zero safety violations detected.")
    else:
        print("❌ FAIL: Integrity Compromised. Safety violations detected.")
    print("="*60 + "\n")
    print(f"Detailed log saved to: {output_path}")