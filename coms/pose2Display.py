import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

# Initialize MediaPipe Pose and drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

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

#FrameDrop
frame_count = 0
process_frame_interval = 3  # Process every 2nd frame
    
with mp_pose.Pose(static_image_mode=False, 
                  min_detection_confidence=0.3, 
                  min_tracking_confidence=0.5) as pose:
    
    while video_object.isOpened():
        ret, frame = video_object.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue
            
        frame_count += 1
        if frame_count % process_frame_interval != 0:
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # Create a blank image for the LED matrix
        matrix_image = Image.new("RGB", (64, 64))
        draw = ImageDraw.Draw(matrix_image)

        # Draw the pose annotations on the LED matrix image
        if results.pose_landmarks:
            # Iterate through all connections
            for connection in mp_pose.POSE_CONNECTIONS:
                start_point = results.pose_landmarks.landmark[connection[0]]
                end_point = results.pose_landmarks.landmark[connection[1]]
                start_x, start_y = int(start_point.x * 64), int(start_point.y * 64)
                end_x, end_y = int(end_point.x * 64), int(end_point.y * 64)
                draw.line((start_x, start_y, end_x, end_y), fill="yellow", width=1)

        # Update the matrix display
        matrix.SetImage(matrix_image.convert('RGB'))

        # Exit logic
        if cv2.waitKey(5) & 0xFF == 27:
            break

video_object.release()
cv2.destroyAllWindows()
matrix.Clear()
