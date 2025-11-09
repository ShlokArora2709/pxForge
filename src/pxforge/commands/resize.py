"""
Resize and transformation commands.

Provides commands for resizing, cropping, and rotating images.
"""

import click
from ..api_client import make_request
from ..utilities import validate_image_id


@click.command()
@click.argument("image_id")
@click.option("--width", "-w", type=int, required=True, help="Target width in pixels")
@click.option("--height", "-h", type=int, required=True, help="Target height in pixels")
def resize(image_id, width, height):
    """
    Resize an image to specified dimensions.

    IMAGE_ID: ID of the image to resize
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Resizing image to {width}x{height}...")
        result = make_request(
            "/resize",
            data={"image_id": image_id, "width": width, "height": height}
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Image resized successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to resize image: {e}", err=True)


@click.command()
@click.argument("image_id")
@click.option("--ratio", "-r", required=True, help="Aspect ratio (e.g., 16:9, 4:3)")
def aspect_ratio(image_id, ratio):
    """
    Crop image to maintain specified aspect ratio.

    IMAGE_ID: ID of the image to crop
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Applying aspect ratio {ratio}...")
        result = make_request(
            "/aspect-ratio",
            data={"image_id": image_id, "aspect_ratio": ratio}
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Aspect ratio applied successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to apply aspect ratio: {e}", err=True)


@click.command()
@click.argument("image_id")
@click.option("--angle", "-a", type=int, required=True, help="Rotation angle in degrees")
def rotate(image_id, angle):
    """
    Rotate an image by specified angle.

    IMAGE_ID: ID of the image to rotate
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Rotating image by {angle} degrees...")
        result = make_request(
            "/rotate",
            data={"image_id": image_id, "angle": angle}
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Image rotated successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to rotate image: {e}", err=True)
