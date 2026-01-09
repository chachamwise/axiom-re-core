# AXIOM: The Universal Physics Kernel

![Version](https://img.shields.io/badge/version-1.0.1_Gold-blue.svg)
![License](https://img.shields.io/badge/license-AXIOM_Public_License-red.svg)
![Status](https://img.shields.io/badge/integrity-SEALED-green.svg)

> **⚠️ DISCLAIMER:** This repository contains **no AI, policies, or learning components.** > It provides only the deterministic verification kernel (`PhysicsKernel`) and the constitutional interface (`Bridge`).  
> AI agents utilizing this kernel can be found in the [`experiments/`](experiments/) folder.

---

**AXIOM RE (Reasoning Engine)** is a stateless, physics-constrained verification architecture for autonomous industrial systems. It decouples physical laws from control logic, acting as an immutable "Constitutional Layer" for AI agents.

## 🧠 The Philosophy: "Code is Law"

In critical infrastructure (Water, Energy, Mining), a control error is not a bug—it is a disaster. 
Standard AI (RL/NN) is probabilistic and therefore inherently unsafe for zero-tolerance environments.

**AXIOM** solves this by embedding a **Sealed Physics Kernel** that verifies every action against algebraic invariants derived from Dimensional Analysis and Affinity Laws. It does not optimize for rewards; it enforces physical feasibility.

## 🏗️ Architecture

The system operates as a strict three-layer hierarchy. For a detailed engineering breakdown and safety guarantees, see the [Formal Scope](docs/FORMAL_SCOPE.md).

![AXIOM RE Architecture](https://raw.githubusercontent.com/chachamwise/axiom-re-core/main/docs/figures/axiom_re_architecture_v1.svg)

1.  **The Agent (External):** Generates a proposed control action ($a_t$). This layer is untrusted and stochastic.
2.  **The Constitutional Bridge (`bridge.py`):** A stateless interface that intercepts $a_t$. It queries the Kernel to project the future state $\hat{s}_{t+1}$.
3.  **The Physics Kernel (`core.py`):** The sealed, deterministic core. It contains the algebraic invariants ($\Omega$) and performs the geometric projection of Potential and Flux. It returns raw physics data, not decisions.

**See also:** [Preprint Abstract & Contributions](docs/PREPRINT_ABSTRACT.md)

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/chachamwise/axiom-re-core.git
cd axiom-re-core
pip install -r requirements.txt
```

## Usage Example

```python
from axiom_re import PhysicsKernel, axiom_permission_check

# 1. Define Machine DNA (e.g., A 15kW Water Pump)
dna = {
    'max_head': 80.0,
    'max_flow': 45.0,
    'rated_power': 15.0,
    'safe_pressure_limit': 75.0
}

# 2. Receive Agent Intent
intent = {'hz': 60.0}

# 3. Verify (The Bridge)
verdict = axiom_permission_check(dna, current_state={}, proposed_action=intent)

if verdict['status'] == 'BLOCKED':
    print(f"🛑 ACTION BLOCKED: {verdict['reasons']}")
    print(f"👉 Safe Action Substituted: {verdict['safe_action']}")
else:
    print("✅ Action Approved")
```

## 🧪 Proven Safety

AXIOM demonstrates **zero kernel-defined safety invariant violations** in the provided experiments.

* 📜 **Proof Script:** [experiments/safety_proof.py](https://github.com/chachamwise/axiom-re-core/blob/main/experiments/safety_proof.py)
* 📊 **Raw Results:** [experiments/axiom_safety_proof.csv](https://github.com/chachamwise/axiom-re-core/blob/main/experiments/axiom_safety_proof.csv)

| Metric | Standard RL (PPO) | AXIOM-Constrained RL |
| :--- | :---: | :---: |
| Training Episodes | 500 | 500 |
| **Safety Violations** | **59** | **0** |
| Convergence Time | Slow (Trial & Error) | Fast (Guided) |

## 🛡️ License & Integrity

Licensed under the **AXIOM Public License (APL-1.0)**. 

* **Free for academic research and non-commercial use.**
* **Commercial use** requires a distinct agreement.
* **Integrity Clause:** The file `core.py` (The Physics Kernel) may **NOT** be modified. It must be used as a sealed dependency to maintain the validity of safety guarantees.

---

## 📜 Citation

If you use AXIOM in your research, you must cite the architecture:

> Mwise, C. (2026). *AXIOM: A Stateless Physics-Constrained Verification Architecture for Safe Autonomous Systems*. Aquaflux Tech.

**BibTeX:**
```bibtex
@software{axiom_re_core,
  author = {Mwise, Chacha},
  title = {AXIOM: A Stateless Physics-Constrained Verification Architecture for Safe Autonomous Systems},
  version = {1.0.0},
  year = {2026},
  url = {https://github.com/chachamwise/axiom-re-core}
}