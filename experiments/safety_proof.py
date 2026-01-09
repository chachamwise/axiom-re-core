"""
AXIOM EXPERIMENT: SAFETY PROOF
Compares 'Standard RL' vs 'Axiom-Constrained RL'.
Uses the ACTUAL library code (src/axiom_re) to prove validity.
"""
import sys
import os
import random
import pandas as pd

# 1. LINK TO SOURCE CODE
# Tells Python to look in the 'src' folder for library
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# 2. IMPORT THE REAL BRIDGE
# If this fails, it means the library structure is wrong. This is the true test.
from axiom_re import axiom_permission_check

# --- CONFIGURATION ---
EPISODES = 500
SAFE_LIMIT_PRESSURE = 9.5
# This DNA follows the README schema
MACHINE_DNA = {
    'max_head': 10.0, 
    'max_flow': 50.0, 
    'rated_power': 15.0, 
    'safe_pressure_limit': SAFE_LIMIT_PRESSURE
}

class WaterTankEnv:
    def __init__(self):
        self.pressure = 0.0
    
    def step(self, action_ratio):
        # Physics: Pressure scales with Ratio squared (Simplified for demo)
        # Random noise simulates real-world sensor chaos
        noise = random.uniform(-0.1, 0.1)
        self.pressure = (10.0 * (action_ratio**2)) + noise
        # Ensure pressure doesn't go negative
        self.pressure = max(0.0, self.pressure)
        return self.pressure

def run_experiment():
    env = WaterTankEnv()
    std_violations = 0
    axm_violations = 0
    std_history = []
    axm_history = []
    
    print("🧪 RUNNING: Standard AI vs. AXIOM Bridge...")

    for i in range(EPISODES):
        # --- 1. STANDARD AI (Reckless) ---
        # Guesses a random action (0.0 to 1.1) - often unsafe
        raw_action = random.uniform(0.0, 1.1) 
        
        # Standard executes directly:
        p_std = env.step(raw_action)
        if p_std > SAFE_LIMIT_PRESSURE:
            std_violations += 1
        std_history.append(std_violations)

        # --- 2. AXIOM AI (Protected) ---
        # Proposes the SAME reckless action
        intent = {'ratio': raw_action}
        
        # --- THE REAL TEST: CALL THE LIBRARY ---
        # Query actual bridge.py
        verdict = axiom_permission_check(MACHINE_DNA, {'pressure': 0.0}, intent)
        
        if verdict['status'] == 'BLOCKED':
            # The Library blocked it! Use the safe action it suggested.
            final_action = verdict['safe_action']['ratio'] 
        else:
            final_action = raw_action
            
        # AXIOM executes:
        p_axm = env.step(final_action)
        if p_axm > SAFE_LIMIT_PRESSURE:
            axm_violations += 1 # If this increases, core.py has a bug.
        axm_history.append(axm_violations)

    return std_history, axm_history

if __name__ == "__main__":
    std, axm = run_experiment()
    
    # Save Data for the CSV
    df = pd.DataFrame({
        "Episode": range(EPISODES), 
        "Standard_Violations": std, 
        "Axiom_Violations": axm
    })
    df.to_csv("axiom_safety_proof.csv", index=False)
    
    # --- VISUAL REPORT (The "Money Shot") ---
    print("\n" + "="*60)
    print(f"📊  AXIOM SAFETY VERIFICATION REPORT")
    print("="*60)
    print(f"Total Episodes Run:       {EPISODES}")
    print("-" * 60)
    print(f"🟥 STANDARD AI VIOLATIONS: {std[-1]}  (Rate: {std[-1]/EPISODES*100:.1f}%)")
    print(f"🟩 AXIOM AI VIOLATIONS:    {axm[-1]}    (Rate: {axm[-1]/EPISODES*100:.1f}%)")
    print("-" * 60)
    
    if axm[-1] == 0:
        print("✅  RESULT: INTEGRITY CONFIRMED.")
        print("    The Sealed Kernel successfully blocked 100% of unsafe actions.")
    else:
        print("❌  RESULT: INTEGRITY FAILURE.")
    print("="*60 + "\n")
    print("✅ Proof saved to experiments/axiom_safety_proof.csv")