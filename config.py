"""
Configuration settings for image generation
"""

# Default image settings
DEFAULT_WIDTH = 16000
DEFAULT_HEIGHT = 16000
DEFAULT_FORMAT = 'PNG'

# Deep Zoom settings
DZ_TILE_SIZE = 256
DZ_OVERLAP = 1
DZ_FORMAT = 'jpg'

# Output directories
OUTPUT_DIR = 'output'
DEEPZOOM_DIR = 'output/deepzoom_tiles'

# Image generation presets
PRESETS = {
    'small': (4000, 4000),
    'medium': (8000, 8000),
    'large': (16000, 16000),
    'xlarge': (20000, 20000),
    'xxlarge': (32000, 32000),
}

# Color palettes
COLOR_PALETTES = {
    'vibrant': [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255)],
    'pastel': [(255, 179, 186), (255, 223, 186), (255, 255, 186), (186, 255, 201), (186, 225, 255)],
    'monochrome': [(0, 0, 0), (64, 64, 64), (128, 128, 128), (192, 192, 192), (255, 255, 255)],
    'sunset': [(255, 94, 77), (255, 145, 77), (255, 195, 77), (255, 224, 130), (251, 236, 176)],
}
