"""
pxForge CLI - AI-powered image editing tool.

A command-line interface for advanced image processing operations
including resizing, color adjustments, AI-powered cleanup, and editing.
"""

import click
from .commands import basic, resize, color, cleanup, editing


class OrderedGroup(click.Group):
    """
    Custom Click Group that displays commands in organized categories.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_categories = {
            "Basic Commands": [],
            "Resize & Transform": [],
            "Color Adjustments": [],
            "AI-Powered Cleanup": [],
            "Advanced Editing": []
        }

    def add_to_category(self, category, cmd, name=None):
        """
        Add a command to a specific category.

        Args:
            category: Category name
            cmd: Command function
            name: Command name (optional)
        """
        cmd_name = name or cmd.name
        self.add_command(cmd, name=cmd_name)
        if category in self.command_categories:
            self.command_categories[category].append(cmd_name)

    def format_commands(self, ctx, formatter):
        """
        Format commands grouped by category.
        """
        for category, commands in self.command_categories.items():
            if not commands:
                continue

            with formatter.section(category):
                rows = []
                for cmd_name in sorted(commands):
                    cmd = self.commands.get(cmd_name)
                    if cmd is None:
                        continue
                    help_text = cmd.get_short_help_str(limit=60)
                    rows.append((cmd_name, help_text))

                if rows:
                    formatter.write_dl(rows)


@click.command(cls=OrderedGroup)
@click.version_option(version="0.1.0")
def cli():
    """
    pxForge - AI-powered image editing CLI tool.

    Upload images and apply various transformations including:
    - Resize, crop, and rotate
    - Color adjustments (B&W, RGB, contrast, brightness)
    - AI-powered cleanup (background removal, object removal, denoising)
    - Advanced editing (background replacement, prompt-based edits, watermarks)

    Use 'pxforge COMMAND --help' for more information on a command.
    """
    pass


# Register basic commands
cli.add_to_category("Basic Commands", basic.upload)
cli.add_to_category("Basic Commands", basic.list_images, name="list")
cli.add_to_category("Basic Commands", basic.delete)
cli.add_to_category("Basic Commands", basic.download)

# Register resize commands
cli.add_to_category("Resize & Transform", resize.resize)
cli.add_to_category("Resize & Transform", resize.aspect_ratio)
cli.add_to_category("Resize & Transform", resize.rotate)

# Register color adjustment commands
cli.add_to_category("Color Adjustments", color.to_bw)
cli.add_to_category("Color Adjustments", color.to_rgb)
cli.add_to_category("Color Adjustments", color.contrast)
cli.add_to_category("Color Adjustments", color.brightness)

# Register cleanup commands
cli.add_to_category("AI-Powered Cleanup", cleanup.remove_bg)
cli.add_to_category("AI-Powered Cleanup", cleanup.remove_object)
cli.add_to_category("AI-Powered Cleanup", cleanup.remove_noise)

# Register editing commands
cli.add_to_category("Advanced Editing", editing.replace_bg)
cli.add_to_category("Advanced Editing", editing.prompt_edit)
cli.add_to_category("Advanced Editing", editing.watermark)


if __name__ == "__main__":
    cli()
