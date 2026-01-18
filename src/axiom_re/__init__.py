"""
AXIOM RE - Industrial Physics Verification Kernel.
Version: 1.0.2
Copyright (c) 2026 Chacha Mwise / Aquaflux Tech.
License: AXIOM Public License (APL-1.0)
"""

# Expose critical components to the package level
from .core import PhysicsKernel
from .bridge import axiom_permission_check
from .gym import AxiomGym

__version__ = "1.0.2"
__author__ = "Chacha Mwise"