"""
Deep Zoom Tile Generator
Generates OpenSeadragon-compatible tile pyramids
"""

import os
from PIL import Image
import math

class DeepZoomGenerator:
    def __init__(self, image_path, output_dir, tile_size=256, overlap=1, image_format='jpg'):
        """
        Initialize Deep Zoom tile generator

        Args:
            image_path: Path to source high-resolution image
            output_dir: Directory to save tiles
            tile_size: Size of each tile (default 256)
            overlap: Pixel overlap between tiles (default 1)
            image_format: Output format ('jpg' or 'png')
        """
        self.image_path = image_path
        self.output_dir = output_dir
        self.tile_size = tile_size
        self.overlap = overlap
        self.image_format = image_format
        self.img = Image.open(image_path)
        self.width, self.height = self.img.size

    def get_num_levels(self):
        """Calculate number of zoom levels needed"""
        max_dimension = max(self.width, self.height)
        return math.ceil(math.log2(max_dimension)) + 1

    def get_scale_dimensions(self, level):
        """Get dimensions for a specific level"""
        max_level = self.get_num_levels() - 1
        scale = 2 ** (max_level - level)
        width = math.ceil(self.width / scale)
        height = math.ceil(self.height / scale)
        return width, height

    def generate_tiles(self):
        """Generate all tiles for all zoom levels"""
        num_levels = self.get_num_levels()

        print(f"\n{'='*60}")
        print(f"DEEP ZOOM TILE GENERATION")
        print(f"{'='*60}")
        print(f"Source: {self.image_path}")
        print(f"Original size: {self.width}x{self.height}")
        print(f"Generating {num_levels} zoom levels...")
        print(f"{'='*60}\n")

        for level in range(num_levels):
            self.generate_level(level)

        self.generate_dzi_descriptor()
        print(f"\n{'='*60}")
        print("✓ Deep Zoom generation complete!")
        print(f"{'='*60}\n")

    def generate_level(self, level):
        """Generate tiles for a specific zoom level"""
        level_width, level_height = self.get_scale_dimensions(level)

        scaled_img = self.img.resize((level_width, level_height), Image.Resampling.LANCZOS)

        cols = math.ceil(level_width / self.tile_size)
        rows = math.ceil(level_height / self.tile_size)

        print(f"Level {level:2d}: {level_width:5d}x{level_height:5d} ({cols:3d}x{rows:3d} tiles)")

        level_dir = os.path.join(self.output_dir, str(level))
        os.makedirs(level_dir, exist_ok=True)

        for col in range(cols):
            for row in range(rows):
                self.save_tile(scaled_img, level, col, row, level_width, level_height)

    def save_tile(self, img, level, col, row, level_width, level_height):
        """Save a single tile"""
        x = col * self.tile_size
        y = row * self.tile_size

        x1 = max(0, x - self.overlap)
        y1 = max(0, y - self.overlap)
        x2 = min(level_width, x + self.tile_size + self.overlap)
        y2 = min(level_height, y + self.tile_size + self.overlap)

        tile = img.crop((x1, y1, x2, y2))

        tile_path = os.path.join(self.output_dir, str(level), f"{col}_{row}.{self.image_format}")

        if self.image_format == 'jpg':
            tile.save(tile_path, 'JPEG', quality=90, optimize=True)
        else:
            tile.save(tile_path, 'PNG', optimize=True)

    def generate_dzi_descriptor(self):
        """Generate DZI XML descriptor file"""
        dzi_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Image xmlns="http://schemas.microsoft.com/deepzoom/2008"
       Format="{self.image_format}"
       Overlap="{self.overlap}"
       TileSize="{self.tile_size}">
    <Size Width="{self.width}" Height="{self.height}"/>
</Image>"""

        dzi_filename = os.path.basename(self.output_dir) + '.dzi'
        dzi_path = os.path.join(os.path.dirname(self.output_dir), dzi_filename)

        with open(dzi_path, 'w') as f:
            f.write(dzi_content)

        print(f"\n✓ DZI descriptor saved: {dzi_path}")


def generate_deepzoom_vips(input_path, output_dir):
    """
    Generate Deep Zoom tiles using VIPS (faster for huge images)
    Requires: pip install pyvips
    """
    try:
        import pyvips

        print(f"\n{'='*60}")
        print("DEEP ZOOM GENERATION (VIPS - Fast Mode)")
        print(f"{'='*60}\n")

        image = pyvips.Image.new_from_file(input_path)

        print(f"Source: {input_path}")
        print(f"Size: {image.width}x{image.height}")
        print("Generating tiles...")

        image.dzsave(
            output_dir,
            suffix='.jpg[Q=90]',
            tile_size=256,
            overlap=1,
            depth='onetile'
        )

        print(f"\n✓ Deep Zoom tiles generated in {output_dir}")
        print(f"{'='*60}\n")

    except ImportError:
        print("Error: pyvips not installed. Install with: pip install pyvips")
        print("Falling back to PIL method...")
        return False

    return True
