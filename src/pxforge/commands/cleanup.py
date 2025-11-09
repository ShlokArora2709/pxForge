"""
Image cleanup commands.

Provides commands for background removal, object removal,
and noise reduction using AI models.
"""

import click
from ..api_client import make_request
from ..utilities import validate_image_id


@click.command()
@click.argument("image_id")
def remove_bg(image_id):
    """
    Remove background from an image using AI.

    IMAGE_ID: ID of the image to process

    Note: This operation may take a few minutes to complete.
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Removing background (this may take a while)...")
        result = make_request(
            "/remove-background",
            data={"image_id": image_id},
            timeout=600
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Background removed successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to remove background: {e}", err=True)


@click.command()
@click.argument("image_id")
@click.option("--x", type=int, required=True, help="X coordinate of object center")
@click.option("--y", type=int, required=True, help="Y coordinate of object center")
@click.option("--width", "-w", type=int, default=100, help="Bounding box width in pixels")
@click.option("--height", "-h", type=int, default=100, help="Bounding box height in pixels")
def remove_object(image_id, x, y, width, height):
    """
    Remove an object from an image using inpainting.

    IMAGE_ID: ID of the image to process
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Removing object at ({x}, {y}) with size {width}x{height}...")
        result = make_request(
            "/remove-object",
            data={
                "image_id": image_id,
                "x": x,
                "y": y,
                "width": width,
                "height": height
            },
            timeout=600
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Object removed successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to remove object: {e}", err=True)


@click.command()
@click.argument("image_id")
def remove_noise(image_id):
    """
    Remove noise and enhance image quality using AI upscaling.

    IMAGE_ID: ID of the image to process

    Note: This operation may take several minutes to complete.
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Removing noise and enhancing quality (this may take a while)...")
        result = make_request(
            "/remove-noise",
            data={"image_id": image_id},
            timeout=600
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Noise removed and image enhanced successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to remove noise: {e}", err=True)
