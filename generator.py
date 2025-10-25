"""
High-Resolution Image Generator
Generates various types of high-resolution images
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random
import os
from datetime import datetime
import colorsys

class HighResImageGenerator:
    def __init__(self, width=16000, height=16000):
        """
        Initialize high-resolution image generator

        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height

    def generate_gradient(self, direction='horizontal', colors=None):
        """Generate gradient image"""
        print(f"Generating {self.width}x{self.height} gradient image...")

        if colors is None:
            colors = [
                tuple(random.randint(0, 255) for _ in range(3)),
                tuple(random.randint(0, 255) for _ in range(3))
            ]

        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        if direction == 'horizontal':
            for x in range(self.width):
                ratio = x / self.width
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                draw.line([(x, 0), (x, self.height)], fill=(r, g, b))
        else:  # vertical
            for y in range(self.height):
                ratio = y / self.height
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        return img

    def generate_perlin_noise(self, scale=100, octaves=6):
        """Generate Perlin-like noise pattern"""
        print(f"Generating {self.width}x{self.height} noise pattern...")

        noise = np.zeros((self.height, self.width, 3), dtype=np.float32)

        for octave in range(octaves):
            freq = 2 ** octave
            amp = 1.0 / freq

            h = self.height // freq + 1
            w = self.width // freq + 1
            octave_noise = np.random.rand(h, w, 3) * 255 * amp

            octave_img = Image.fromarray(octave_noise.astype(np.uint8))
            octave_img = octave_img.resize((self.width, self.height), Image.BILINEAR)

            noise += np.array(octave_img)

        noise = np.clip(noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noise)

    def generate_geometric(self, shape_type='circles', num_shapes=100):
        """Generate random geometric patterns"""
        print(f"Generating {self.width}x{self.height} geometric pattern...")

        bg_color = tuple(random.randint(0, 255) for _ in range(3))
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)

        for _ in range(num_shapes):
            color = tuple(random.randint(0, 255) for _ in range(3))

            if shape_type == 'circles':
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                radius = random.randint(50, 500)
                draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                             fill=color, outline=color)

            elif shape_type == 'rectangles':
                x1 = random.randint(0, self.width - 100)
                y1 = random.randint(0, self.height - 100)
                x2 = x1 + random.randint(100, 1000)
                y2 = y1 + random.randint(100, 1000)
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)

            elif shape_type == 'polygons':
                num_points = random.randint(3, 8)
                points = [(random.randint(0, self.width),
                           random.randint(0, self.height))
                          for _ in range(num_points)]
                draw.polygon(points, fill=color, outline=color)

        return img

    def generate_voronoi(self, num_points=100):
        """Generate Voronoi diagram"""
        print(f"Generating {self.width}x{self.height} Voronoi pattern...")

        points = [(random.randint(0, self.width),
                   random.randint(0, self.height),
                   tuple(random.randint(0, 255) for _ in range(3)))
                  for _ in range(num_points)]

        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        chunk_size = 1000

        for y_start in range(0, self.height, chunk_size):
            y_end = min(y_start + chunk_size, self.height)
            for x_start in range(0, self.width, chunk_size):
                x_end = min(x_start + chunk_size, self.width)

                for y in range(y_start, y_end):
                    for x in range(x_start, x_end):
                        min_dist = float('inf')
                        closest_color = (0, 0, 0)

                        for px, py, color in points:
                            dist = (x - px) ** 2 + (y - py) ** 2
                            if dist < min_dist:
                                min_dist = dist
                                closest_color = color

                        img_array[y, x] = closest_color

            progress = ((y_end / self.height) * 100)
            print(f"Progress: {progress:.1f}%", end='\r')

        print("\nVoronoi generation complete!")
        return Image.fromarray(img_array)

    def generate_fractal(self, fractal_type='mandelbrot'):
        """Generate fractal patterns"""
        print(f"Generating {self.width}x{self.height} {fractal_type} fractal...")

        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        if fractal_type == 'mandelbrot':
            x_min, x_max = -2.5, 1.5
            y_min, y_max = -2.0, 2.0
            max_iter = 256

            for py in range(self.height):
                for px in range(self.width):
                    x0 = x_min + (x_max - x_min) * px / self.width
                    y0 = y_min + (y_max - y_min) * py / self.height

                    x, y = 0, 0
                    iteration = 0

                    while x*x + y*y <= 4 and iteration < max_iter:
                        xtemp = x*x - y*y + x0
                        y = 2*x*y + y0
                        x = xtemp
                        iteration += 1

                    if iteration == max_iter:
                        color = (0, 0, 0)
                    else:
                        hue = iteration / max_iter
                        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                        color = tuple(int(c * 255) for c in rgb)

                    img_array[py, px] = color

                if py % 100 == 0:
                    print(f"Progress: {(py/self.height)*100:.1f}%", end='\r')

        print("\nFractal generation complete!")
        return Image.fromarray(img_array)

    def generate_plasma(self):
        """Generate plasma effect"""
        print(f"Generating {self.width}x{self.height} plasma pattern...")

        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for y in range(self.height):
            for x in range(self.width):
                value = (
                        np.sin(x / 50.0) +
                        np.sin(y / 50.0) +
                        np.sin((x + y) / 50.0) +
                        np.sin(np.sqrt(x*x + y*y) / 50.0)
                )

                value = (value + 4) / 8

                hue = value
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                img_array[y, x] = tuple(int(c * 255) for c in rgb)

            if y % 100 == 0:
                print(f"Progress: {(y/self.height)*100:.1f}%", end='\r')

        print("\nPlasma generation complete!")
        return Image.fromarray(img_array)

    def save_image(self, img, filename=None, format='PNG', compress=False):
        """Save generated image"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{self.width}x{self.height}_{timestamp}"

        os.makedirs('output', exist_ok=True)

        if format.upper() == 'TIFF' and not compress:
            filepath = f"output/{filename}.tiff"
            img.save(filepath, compression=None)
        elif format.upper() == 'PNG':
            filepath = f"output/{filename}.png"
            img.save(filepath, optimize=not compress)
        elif format.upper() == 'JPG' or format.upper() == 'JPEG':
            filepath = f"output/{filename}.jpg"
            img.save(filepath, quality=95)

        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        print(f"✓ Image saved: {filepath} ({file_size:.2f} MB)")
        return filepath
