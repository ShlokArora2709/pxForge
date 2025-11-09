"""
Color adjustment commands.

Provides commands for color space conversion and
brightness/contrast adjustments.
"""

import click
from ..api_client import make_request
from ..utilities import validate_image_id


@click.command()
@click.argument("image_id")
def to_bw(image_id):
    """
    Convert an image to black and white (grayscale).

    IMAGE_ID: ID of the image to convert
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Converting image to black and white...")
        result = make_request("/toBW", data={"image_id": image_id})

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Image converted to B&W successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to convert image: {e}", err=True)


@click.command()
@click.argument("image_id")
def to_rgb(image_id):
    """
    Convert an image to RGB color space.

    IMAGE_ID: ID of the image to convert
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Converting image to RGB...")
        result = make_request("/toRGB", data={"image_id": image_id})

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Image converted to RGB successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to convert image: {e}", err=True)


@click.command()
@click.argument("image_id")
def contrast(image_id):
    """
    Adjust image contrast.

    IMAGE_ID: ID of the image to adjust
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Adjusting image contrast...")
        result = make_request("/contrast", data={"image_id": image_id})

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Contrast adjusted successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to adjust contrast: {e}", err=True)


@click.command()
@click.argument("image_id")
def brightness(image_id):
    """
    Adjust image brightness.

    IMAGE_ID: ID of the image to adjust
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Adjusting image brightness...")
        result = make_request("/brightness", data={"image_id": image_id})

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Brightness adjusted successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to adjust brightness: {e}", err=True)
