"""
AXIOM RE Package Initialization
Exposes the Core Physics Kernel, Constitutional Bridge, and Digital Twin.
"""

from .core import PhysicsKernel
from .bridge import axiom_permission_check
from .gym import AxiomGym

__version__ = "1.0.1"