# Formal Scope & Operational Boundaries

**Version:** 1.0.0 (Gold)  
**Date:** 2026-01-08  
**Applies to:** AXIOM RE Kernel (`core.py`, `bridge.py`)

---

## 1. Core Guarantee (Invariant Enforcement)

The AXIOM RE Kernel guarantees **Stateless Verification of Control Intent**.  

Given a machine configuration $\Omega$ (DNA) and a proposed action $a_t$, the Kernel will **strictly reject any $a_t$** where the deterministic projection of the future state $\hat{s}_{t+1}$ violates the algebraic invariants defined in $\Omega$.

* **Nature of Guarantee:** Deterministic / Algebraic  
* **Scope:** Logic & Decision Layer  
* **Failure Rate:** 0% (within floating-point precision limits)

---

## 2. Operational Assumptions

The safety guarantees of AXIOM RE are valid under the following assumptions:

1. **Sensor Fidelity:** Input state data $s_t$ (e.g., pressure, voltage) must truthfully represent physical reality. AXIOM does not detect sensor spoofing or calibration drift without external observation.  
2. **Actuator Compliance:** If an action is blocked and a Safe Action $a_{safe}$ is substituted, the physical actuator must respect the command. Mechanical failures (e.g., stuck valves) are **outside software verification scope**.  
3. **DNA Accuracy:** The "System Curve" ($\beta$-factor) derives from `max_potential`, `max_flux`, and `rated_power`. Incorrect configuration yields incorrect safety boundaries.

---

## 3. Explicit Exclusions (Out-of-Scope)

AXIOM RE v1.0.0 does **not guarantee** the following:

* **Material Fatigue:** Cannot predict failure due to degradation (rust, cracks) unless modeled explicitly.  
* **Stochastic Externalities:** Events outside the physics model (e.g., tree falling on a line) are not preventable, though AXIOM reacts to resulting state changes.  
* **Adversarial Hardware Attacks:** Physical tampering, memory injection, or cyberattacks are outside the Kernel’s scope.

---

## 4. Safe State Definition

Upon a `BLOCKED` verdict, AXIOM RE defaults to a:

* **Zero-Energy State** (Ratio = 0.0)  
* or a pre-configured **Safe Setpoint**  

It **does not attempt complex recovery**; it simply enforces cessation of the violation.

---

## 5. Summary for Reviewers

AXIOM RE is a **Verification Architecture**, **not an Oracle**.  
It guarantees that the *AI Agent* will **never cause a physics violation** under the stated assumptions and within the deterministic model.

---

**References:**  
* See experimental validation in [experiments/safety_proof.py](../experiments/safety_proof.py)  
* See preprint abstract: [Preprint Abstract](PREPRINT_ABSTRACT.md)
