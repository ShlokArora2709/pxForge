"""
Utilities for managing local image registry.

This module provides functions to load and save image IDs
to a local JSON file for tracking uploaded images.
"""

import os
import json
from pathlib import Path


def get_storage_file():
    """
    Get the path to the storage file.

    Returns:
        Path: Path object pointing to uploaded_images.json
    """
    base_dir = Path(__file__).parent.parent.parent
    return base_dir / "uploaded_images.json"


def load():
    """
    Load image IDs from local storage.

    Returns:
        list: List of image IDs, empty list if file doesn't exist
    """
    storage_file = get_storage_file()
    if storage_file.exists():
        try:
            with open(storage_file, "r") as f:
                data = json.load(f)
                # Filter out None values
                return [img for img in data if img is not None]
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def save(data):
    """
    Save image IDs to local storage.

    Args:
        data (list): List of image IDs to save
    """
    storage_file = get_storage_file()
    storage_file.parent.mkdir(parents=True, exist_ok=True)
    with open(storage_file, "w") as f:
        json.dump(data, f, indent=2)


def validate_image_id(image_id):
    """
    Check if an image ID exists in local storage.

    Args:
        image_id (str): Image ID to validate

    Returns:
        bool: True if image ID exists, False otherwise
    """
    data = load()
    return image_id in data
