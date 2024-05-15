import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

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

while video_object.isOpened():
    ret, frame = video_object.read()
    if not ret:
        print("Ignoring empty camera frame.")
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    frame.flags.writeable = False
    # Process frame with MediaPipe Segmentation
    results = segmentation.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    segmentation_mask = results.segmentation_mask

    # Threshold the mask to create a binary image
    _, binary_mask = cv2.threshold(segmentation_mask, 0.5, 255, cv2.THRESH_BINARY)

    # Convert the binary mask to a PIL image
    mask_image = Image.fromarray(binary_mask).convert('L')
    mask_image = mask_image.resize((64, 64), Image.NEAREST)

    # Convert to RGB mode before displaying
    rgb_image = mask_image.convert('RGB')

    # Display the result on the LED matrix
    matrix.SetImage(rgb_image)
    
    # Exit logic
    if cv2.waitKey(5) & 0xFF == 27:
        break


video_object.release()
matrix.Clear()

