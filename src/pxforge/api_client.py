"""
API client for making requests to the pxForge backend.

Provides functions for interacting with the image processing API
with proper error handling and response validation.
"""

import requests
from typing import Optional, Dict, Any
from pathlib import Path
from .config import get_base_url


def make_request(
    endpoint: str,
    method: str = "POST",
    files: Optional[Dict] = None,
    data: Optional[Dict] = None,
    timeout: int = 300,
    use_form_data: bool = False
) -> Dict[str, Any]:
    """
    Make an HTTP request to the API.

    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        files: Files to upload
        data: JSON data or form data to send
        timeout: Request timeout in seconds
        use_form_data: Force form data encoding (application/x-www-form-urlencoded)

    Returns:
        dict: API response data

    Raises:
        requests.RequestException: If request fails
    """
    base_url = get_base_url()
    url = f"{base_url}{endpoint}"

    # When files are present or use_form_data is True, use form data
    # Otherwise, use JSON (application/json)
    if files or use_form_data:
        response = requests.request(
            method=method,
            url=url,
            files=files,
            data=data,
            timeout=timeout
        )
    else:
        response = requests.request(
            method=method,
            url=url,
            json=data,
            timeout=timeout
        )

    response.raise_for_status()
    return response.json()


def upload_image(image_path: str) -> Dict[str, Any]:
    """
    Upload an image to the server.

    Args:
        image_path: Path to the image file

    Returns:
        dict: Response containing image ID and URL

    Raises:
        FileNotFoundError: If image file doesn't exist
        requests.RequestException: If upload fails
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(path, "rb") as img_file:
        files = {"image": img_file}
        return make_request("/upload", files=files)


def download_image(url: str, output_path: str):
    """
    Download an image from a URL.

    Args:
        url: Image URL to download from
        output_path: Path to save the downloaded image

    Raises:
        requests.RequestException: If download fails
    """
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "wb") as f:
        f.write(response.content)
