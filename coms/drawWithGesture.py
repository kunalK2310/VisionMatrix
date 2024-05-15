import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
from gesture_recognizer import is_fist
import socket
import time

print("running")

# Setup socket for receiving color change messages
local_ip = ""
port = 5001

receiver_socket = socket.socket()
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.bind((local_ip, port))

receiver_socket.listen()
sender_socket, sender_address = receiver_socket.accept()
print("Connection established with: ", sender_address)

# Set up video capture
video_object = cv2.VideoCapture(0)
if not video_object.isOpened():
    print("Error opening video stream or file")

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands

# LED Matrix setup
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 2
options.hardware_mapping = 'regular'
options.gpio_slowdown = 5
matrix = RGBMatrix(options=options)

# Initialize an image for persistent drawing
persistent_image = Image.new("RGB", (64, 64))
draw_persistent = ImageDraw.Draw(persistent_image)

# Define brush size (radius)
brush_size = 1

# FrameDrop
frame_count = 0
process_frame_interval = 3  # Process every 3rd frame

# State variables
drawing = True  # Attempt to pause the drawing

# Non-blocking socket read
sender_socket.setblocking(0)
received_message = "black"

# Use MediaPipe Hands within a 'with' block
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while video_object.isOpened():
        try:
            received_data = sender_socket.recv(1024)
            received_message = received_data.decode().strip()
            print(received_message)
        except BlockingIOError:
            pass

        ret, frame = video_object.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        frame_count += 1
        if frame_count % process_frame_interval != 0:
            continue

        # Flip the image horizontally for a laterally correct display, and convert the image to RGB
        frame = cv2.resize(cv2.flip(frame, 1), (320, 240))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Copy the persistent image to the matrix image for displaying
        matrix_image = persistent_image.copy()
        draw = ImageDraw.Draw(matrix_image)

        possible_colors = ["red", "orange", "yellow", "green", "blue", "violet", "black", "white"]

        if received_message.startswith("at_name_"):
            matrix_image.save(f"{received_message[8:]}.png")
            time.sleep(2)
            received_message = "black"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Check for gestures
                if is_fist(hand_landmarks):
                    drawing = False
                else:
                    drawing = True

                if drawing:
                    # Highlight the index finger tip
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x_tip = int(index_tip.x * 64)
                    y_tip = int(index_tip.y * 64)

                    # Ensure received_message is a valid color
                    color = received_message if received_message in possible_colors else "black"

                    # Draw on the persistent image with specified color
                    draw_persistent.ellipse([(x_tip - brush_size, y_tip - brush_size), (x_tip + brush_size, y_tip + brush_size)], fill=color)

                    # Set crosshair color to white if drawing color is blue
                    crosshair_color = "white" if color == "blue" else "blue"
                    crosshair_size = 2
                    draw.line((x_tip - crosshair_size, y_tip, x_tip + crosshair_size, y_tip), fill=crosshair_color)
                    draw.line((x_tip, y_tip - crosshair_size, x_tip, y_tip + crosshair_size), fill=crosshair_color)

        # Update the matrix display with the updated matrix image
        matrix.SetImage(matrix_image.convert('RGB'))

        if cv2.waitKey(5) & 0xFF == 27:
            break

video_object.release()
cv2.destroyAllWindows()
matrix.Clear()
