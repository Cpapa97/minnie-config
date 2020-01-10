# Make sure the imports for the adapters and stuff can work correctly with how I have the configuration setup.

# Also enable this package to do some commandline mounting of dj-stor01 from at-storage03.ad.bcm.edu

from .minnie65_config import *
from .adapters import mesh, decimated_mesh, adapter_objects

__all__ = ['adapters', 'minnie65_config']