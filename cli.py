"""
Command Line Interface for Image Generation
"""

import argparse
import sys
from generator import HighResImageGenerator
from deepzoom_generator import DeepZoomGenerator, generate_deepzoom_vips


def interactive_menu():
    """Interactive menu for image generation"""
    print("\n" + "="*60)
    print("HIGH RESOLUTION IMAGE GENERATOR")
    print("="*60 + "\n")

    width = int(input("Enter width (default 16000): ") or "16000")
    height = int(input("Enter height (default 16000): ") or "16000")

    generator = HighResImageGenerator(width, height)

    print("\nChoose image type:")
    print("1. Gradient")
    print("2. Perlin Noise")
    print("3. Geometric Patterns")
    print("4. Voronoi Diagram")
    print("5. Mandelbrot Fractal")
    print("6. Plasma Effect")

    choice = input("\nEnter choice (1-6): ")

    img = None
    if choice == '1':
        direction = input("Direction (horizontal/vertical, default horizontal): ") or "horizontal"
        img = generator.generate_gradient(direction)
    elif choice == '2':
        img = generator.generate_perlin_noise()
    elif choice == '3':
        shape = input("Shape (circles/rectangles/polygons, default circles): ") or "circles"
        num = int(input("Number of shapes (default 100): ") or "100")
        img = generator.generate_geometric(shape, num)
    elif choice == '4':
        points = int(input("Number of points (default 100): ") or "100")
        img = generator.generate_voronoi(points)
    elif choice == '5':
        img = generator.generate_fractal('mandelbrot')
    elif choice == '6':
        img = generator.generate_plasma()
    else:
        print("Invalid choice!")
        return

    if img:
        format_choice = input("\nFormat (PNG/TIFF/JPG, default PNG): ").upper() or "PNG"
        filename = input("Filename (press Enter for auto): ") or None

        filepath = generator.save_image(img, filename, format_choice)

        generate_dz = input("\nGenerate Deep Zoom tiles? (y/n): ").lower()
        if generate_dz == 'y':
            output_dir = input("Output directory (default: output/deepzoom_tiles): ") or "output/deepzoom_tiles"
            print("\nGenerating Deep Zoom tiles...")
            dz = DeepZoomGenerator(filepath, output_dir)
            dz.generate_tiles()


def main():
    parser = argparse.ArgumentParser(
        description='Generate high-resolution random images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --interactive
  python cli.py --width 16000 --height 16000 --type gradient --format TIFF
  python cli.py --type geometric --shape circles --num-shapes 200
  python cli.py --type voronoi --deepzoom
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('--width', type=int, default=16000,
                        help='Image width (default: 16000)')
    parser.add_argument('--height', type=int, default=16000,
                        help='Image height (default: 16000)')
    parser.add_argument('--type', '-t',
                        choices=['gradient', 'noise', 'geometric', 'voronoi', 'fractal', 'plasma'],
                        default='gradient',
                        help='Image type (default: gradient)')
    parser.add_argument('--format', '-f',
                        choices=['PNG', 'TIFF', 'JPG'],
                        default='PNG',
                        help='Output format (default: PNG)')
    parser.add_argument('--output', '-o', type=str,
                        help='Output filename (without extension)')
    parser.add_argument('--shape',
                        choices=['circles', 'rectangles', 'polygons'],
                        default='circles',
                        help='Shape type for geometric patterns')
    parser.add_argument('--num-shapes', type=int, default=100,
                        help='Number of shapes for geometric patterns')
    parser.add_argument('--deepzoom', '-dz', action='store_true',
                        help='Generate Deep Zoom tiles after image generation')
    parser.add_argument('--dz-output', type=str, default='output/deepzoom_tiles',
                        help='Deep Zoom output directory')

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        interactive_menu()
        return

    # Generate image
    print(f"\n{'='*60}")
    print(f"Generating {args.type} image at {args.width}x{args.height}")
    print(f"{'='*60}\n")

    generator = HighResImageGenerator(args.width, args.height)

    if args.type == 'gradient':
        img = generator.generate_gradient()
    elif args.type == 'noise':
        img = generator.generate_perlin_noise()
    elif args.type == 'geometric':
        img = generator.generate_geometric(args.shape, args.num_shapes)
    elif args.type == 'voronoi':
        img = generator.generate_voronoi(num_points=100)
    elif args.type == 'fractal':
        img = generator.generate_fractal('mandelbrot')
    elif args.type == 'plasma':
        img = generator.generate_plasma()

    filepath = generator.save_image(img, args.output, args.format)

    if args.deepzoom:
        print("\nGenerating Deep Zoom tiles...")
        dz = DeepZoomGenerator(filepath, args.dz_output)
        dz.generate_tiles()

    print(f"\n{'='*60}")
    print("Generation complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
