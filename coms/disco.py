import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageOps

# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Set up the video capture source
video_object = cv2.VideoCapture(0)
video_object.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# LED Matrix setup
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 2
options.hardware_mapping = 'regular'
options.gpio_slowdown = 5
matrix = RGBMatrix(options=options)

# Define Mario Super Star colors
super_star_colors = [
    (255, 0, 0),    # Red
    (255, 255, 0),  # Yellow
    (0, 0, 255),    # Blue
    (0, 255, 0)     # Green
]
color_index = 0


while video_object.isOpened():
    ret, frame = video_object.read()
    if not ret:
        print("Ignoring empty camera frame.")
        continue

    # Resize and process frame with MediaPipe Segmentation
    results = segmentation.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    segmentation_mask = results.segmentation_mask

    # Threshold the mask to create a binary image
    _, binary_mask = cv2.threshold(segmentation_mask, 0.5, 255, cv2.THRESH_BINARY)

    # Convert the binary mask to a PIL image
    mask_image = Image.fromarray(binary_mask).convert('L')
    mask_image = mask_image.resize((64, 64), Image.NEAREST)

    # Apply current rainbow color to the mask
    colored_mask = ImageOps.colorize(mask_image, black="black", white=super_star_colors[color_index])
    color_index = (color_index + 1) % len(super_star_colors)  # Update color index

    # Display the result on the LED matrix
    matrix.SetImage(colored_mask.convert('RGB'))
    
    # Exit logic
    if cv2.waitKey(5) & 0xFF == 27:
        break


video_object.release()
matrix.Clear()
