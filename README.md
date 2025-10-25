# High-Resolution Image Generator with Deep Zoom

Generate ultra-high-resolution images (up to 32000×32000 and beyond) with various patterns and automatically create Deep Zoom tiles for OpenSeadragon viewing.

## Features

- **Multiple Image Types**: Gradient, Perlin Noise, Geometric Patterns, Voronoi Diagrams, Fractals, Plasma
- **Custom Resolutions**: Generate images at any resolution (16000×16000 default)
- **Multiple Formats**: PNG, TIFF (uncompressed), JPEG
- **Deep Zoom Support**: Automatic tile generation for web viewing
- **Interactive CLI**: Easy-to-use command-line interface
- **Fast Processing**: Optional VIPS support for faster tile generation

## Installation

```shell
# Clone or download the project
cd high-res-image-generator

# Install dependencies
pip install -r requirements.txt

# Optional: Install VIPS for faster processing (recommended for large images)
pip install pyvips
```

## Quick Start

### Interactive Mode
```shell
python cli.py --interactive
```

### Command Line Examples

```shell
# Generate 16000×16000 gradient as TIFF
python cli.py --width 16000 --height 16000 --type gradient --format TIFF

# Generate geometric pattern with Deep Zoom tiles
python cli.py --type geometric --shape circles --num-shapes 200 --deepzoom

# Generate Voronoi diagram
python cli.py --width 20000 --height 20000 --type voronoi --format PNG

# Generate Mandelbrot fractal
python cli.py --type fractal --format JPG --deepzoom

# Generate plasma effect
python cli.py --type plasma --width 8000 --height 8000
```

## Usage

### 1. Generate High-Resolution Image

```shell
python cli.py --width 16000 --height 16000 --type gradient --format TIFF --output my_image
```

### 2. Generate Deep Zoom Tiles

```shell
python cli.py --type voronoi --deepzoom --dz-output output/my_tiles
```

### 3. View in Browser

```shell
# Start a local server
python -m http.server 8000

# Open viewer.html in browser
# Navigate to: http://localhost:8000/viewer.html
```

## Image Types

| Type | Description | Best For |
|------|-------------|----------|
| **gradient** | Smooth color transitions | Backgrounds, testing |
| **noise** | Perlin-like noise patterns | Textures, natural effects |
| **geometric** | Random shapes (circles, rectangles, polygons) | Abstract art, patterns |
| **voronoi** | Voronoi diagram with colored cells | Organic patterns, mosaics |
| **fractal** | Mandelbrot set visualization | Mathematical art, zoom exploration |
| **plasma** | Psychedelic plasma effect | Backgrounds, animations |

## File Structure

```
high-res-image-generator/
├── cli.py                    # Command-line interface
├── generator.py              # Image generation logic
├── deepzoom_generator.py     # Deep Zoom tile generator
├── config.py                 # Configuration settings
├── viewer.html               # OpenSeadragon viewer
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── output/                   # Generated images and tiles
    ├── *.png/tiff/jpg        # Generated images
    └── deepzoom_tiles/       # Tile pyramids
        ├── 0/                # Zoom level 0
        ├── 1/                # Zoom level 1
        └── ...
```

## Configuration

Edit `config.py` to change default settings:

```
DEFAULT_WIDTH = 16000
DEFAULT_HEIGHT = 16000
DZ_TILE_SIZE = 256
DZ_OVERLAP = 1
```

## Performance Tips

1. **Use VIPS for large images** (>16000×16000): `pip install pyvips`
2. **Use JPEG for tiles** to reduce file size
3. **Adjust tile size** based on your needs (256 is standard)
4. **Close other applications** when generating very large images

## Troubleshooting

**Out of memory error:**
- Reduce image dimensions
- Install pyvips for better memory management
- Use JPEG instead of PNG

**Tiles not displaying:**
- Check DZI file path in viewer.html
- Ensure local server is running
- Check browser console for errors

**Slow generation:**
- Install pyvips: `pip install pyvips`
- Reduce number of zoom levels
- Use JPEG format for tiles

## License

MIT License - Feel free to use in your projects!

## Credits

- OpenSeadragon for deep zoom viewing
- Pillow for image processing
- VIPS for high-performance tile generation
```

## Usage Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run interactive mode
python cli.py --interactive

# 3. Or use command line
python cli.py --width 16000 --height 16000 --type voronoi --deepzoom

# 4. View the result
python -m http.server 8000
# Then open http://localhost:8000/viewer.html
```

All files are now properly named and organized! 🎉