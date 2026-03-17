"""
Configuration module for Chrome browser
"""

from .paths import get_paths_by_os
from .flags import get_flags_by_os

__all__ = ['get_paths_by_os', 'get_flags_by_os']