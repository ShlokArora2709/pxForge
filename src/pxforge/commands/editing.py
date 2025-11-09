"""
Advanced editing commands.

Provides commands for AI-powered editing operations like
background replacement, prompt-based editing, and watermarking.
"""

import click
from pathlib import Path
from ..api_client import make_request
from ..utilities import validate_image_id


@click.command()
@click.argument("image_id")
@click.argument("bg_image_path", type=click.Path(exists=True))
def replace_bg(image_id, bg_image_path):
    """
    Replace image background with a new background.

    IMAGE_ID: ID of the foreground image

    BG_IMAGE_PATH: Path to the new background image

    Note: This operation may take several minutes to complete.
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo("Replacing background (this may take a while)...")

        with open(bg_image_path, "rb") as bg_file:
            files = {"bg": bg_file}
            result = make_request(
                "/replace-bg",
                files=files,
                data={"image_id": image_id},
                timeout=600
            )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Background replaced successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to replace background: {e}", err=True)


@click.command()
@click.argument("image_id")
@click.option("--prompt", "-p", required=True, help="Edit instruction prompt")
def prompt_edit(image_id, prompt):
    """
    Edit image using AI based on a text prompt.

    IMAGE_ID: ID of the image to edit

    Examples:
    - "make the sky more blue"
    - "add a sunset in the background"
    - "make it look like winter"

    Note: This operation may take several minutes to complete.
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Editing image with prompt: '{prompt}'")
        click.echo("(this may take a while)...")

        result = make_request(
            "/prompt-edit",
            data={"image_id": image_id, "prompt": prompt},
            timeout=600
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Image edited successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to edit image: {e}", err=True)


@click.command()
@click.argument("image_id")
@click.option("--text", "-t", required=True, help="Watermark text")
@click.option("--position", "-p", type=click.Choice(
    ["top-left", "top-right", "bottom-left", "bottom-right"],
    case_sensitive=False
), default="bottom-right", help="Watermark position")
def watermark(image_id, text, position):
    """
    Add a text watermark to an image.

    IMAGE_ID: ID of the image to watermark
    """
    if not validate_image_id(image_id):
        click.echo(f"Error: Image ID {image_id} not found in registry", err=True)
        return

    try:
        click.echo(f"Adding watermark '{text}' at {position}...")
        result = make_request(
            "/watermark",
            data={
                "image_id": image_id,
                "watermark": text,
                "position": position
            },
            use_form_data=True
        )

        if result.get("success"):
            url = result.get("image_url")
            click.echo("Watermark added successfully!")
            click.echo(f"URL: {url}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)

    except Exception as e:
        click.echo(f"Failed to add watermark: {e}", err=True)
