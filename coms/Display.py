from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

def main():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 2
    options.hardware_mapping = 'regular'
    options.gpio_slowdown = 5
    matrix = RGBMatrix(options=options)

    # Create RGBMatrix object with the above options
    matrix = RGBMatrix(options=options)

    # Load the image
    image_path = "path/to/your/image.png"  # Specify the path to your 64x64 PNG image
    image = Image.open(image_path).convert('RGB')  # Convert image to RGB

    # Check if image needs resizing
    if image.size != (64, 64):
        image = image.resize((64, 64), Image.ANTIALIAS)

    # Display the image
    matrix.SetImage(image)

    # Usually, you'd want to keep the program running to keep the image on the display.
    # This can be done with a try-except block or other control flow.
    try:
        print("Press CTRL-C to stop.")
        while True:
            continue
    except KeyboardInterrupt:
        print("Exiting...")
        matrix.Clear()

if __name__ == "__main__":
    main()
