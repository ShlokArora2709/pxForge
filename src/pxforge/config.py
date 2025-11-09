"""
Configuration management for pxForge CLI.

Handles API endpoint configuration and settings.
"""

import os
from pathlib import Path


DEFAULT_BASE_URL = "https://shlokarora2709-ai-image-editor.hf.space"


def get_base_url():
    """
    Get the API base URL from environment or use default.

    Returns:
        str: API base URL
    """
    return os.environ.get("PXFORGE_API_URL", DEFAULT_BASE_URL)


def get_config_dir():
    """
    Get the configuration directory path.

    Returns:
        Path: Configuration directory path
    """
    config_dir = Path.home() / ".pxforge"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir
