"""
Basic commands for pxForge CLI.

Includes upload, list, delete, and download functionality.
"""

import click
from pathlib import Path
from ..api_client import upload_image, download_image, make_request
from ..utilities import load, save, validate_image_id


@click.command()
@click.argument("image_path", type=click.Path(exists=True))
def upload(image_path):
    """
    Upload an image to the server.

    IMAGE_PATH: Path to the image file to upload
    """
    try:
        click.echo(f"Uploading image from {image_path}...")
        result = upload_image(image_path)

        image_id = result.get("image_id")
        image_url = result.get("image_url")

        click.echo("Image uploaded successfully!")
        click.echo(f"Image ID: {image_id}")
        click.echo(f"URL: {image_url}")

        # Save to local registry
        data = load()
        if image_id not in data:
            data.append(image_id)
            save(data)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Failed to upload image: {e}", err=True)


@click.command()
def list_images():
    """
    List all uploaded image IDs from local registry.
    """
    click.echo("Fetching list of uploaded images...")
    imgs = load()

    if not imgs:
        click.echo("No images found in local registry.")
        return

    click.echo(f"\nFound {len(imgs)} image(s):")
    for idx, img in enumerate(imgs, 1):
        click.echo(f"{idx}. {img}")


@click.command()
@click.argument("image_id")
def delete(image_id):
    """
    Delete an image ID from local registry.

    IMAGE_ID: ID of the image to delete from registry
    """
    data = load()

    if image_id not in data:
        click.echo(f"Error: {image_id} not found in registry", err=True)
        return

    data.remove(image_id)
    save(data)
    click.echo(f"Deleted {image_id} from local registry")


@click.command()
@click.argument("url")
@click.argument("output_path", type=click.Path())
def download(url, output_path):
    """
    Download an image from a URL.

    URL: Image URL to download from

    OUTPUT_PATH: Path to save the downloaded image
    """
    try:
        click.echo(f"Downloading image from {url}...")
        download_image(url, output_path)
        click.echo(f"Image saved to {output_path}")
    except Exception as e:
        click.echo(f"Failed to download image: {e}", err=True)
