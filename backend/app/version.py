"""
Version Management
Application version information and build metadata.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

VERSION = __version__
VERSION_INFO = __version_info__


def get_version() -> str:
    """Get current application version."""
    return __version__


def get_version_info() -> tuple[int, int, int]:
    """Get version info as tuple."""
    return __version_info__
