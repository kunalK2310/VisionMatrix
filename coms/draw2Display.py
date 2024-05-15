import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import sys
import time
#from receiver import received_message


import socket
import subprocess

print("running")

local_ip = ""
port = 5001

receiver_socket = socket.socket()
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.bind((local_ip, port))

receiver_socket.listen()
sender_socket, sender_address = receiver_socket.accept()
print("Connection established with: ", sender_address)



#received_data = sender_socket.recv(1024)


#mes = received_message
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


sender_socket.setblocking(0)
received_message = "black"
# Use MediaPipe Hands within a 'with' block
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while video_object.isOpened():
        
        try:
            received_data = sender_socket.recv(1024)
            received_message = received_data.decode()
            print(received_message)
            
        except:
            None
            
        
        ret, frame = video_object.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a laterally correct display, and convert the image to RGB
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Start each frame by copying the persistent image
        matrix_image = persistent_image.copy()
        draw = ImageDraw.Draw(matrix_image)
        
        possible_colors = ["red","orange", "yellow","green","blue","purple","black","white"]

        if received_message.startswith("at_name_"):
            matrix_image.save(str(received_message[8:])+".png")
            time.sleep(2)
            #persistent_image = Image.new("RGB", (64, 64))
            
            
            #receiver_socket.shutdown()
            #receiver_socket.close()
            received_message = "black"
        
        
        if results.multi_hand_landmarks:
            
            #print("this is the received message: " + str(received_message))
            
            #if received_message not in possible_colors:
            #    matrix_image.save(str(received_message)+".png")
            #    time.sleep(2)
            #    persistent_image = Image.new("RGB", (64, 64))
            #    received_message = "black"
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Highlight the index finger tip
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x_tip = int(index_tip.x * 64)
                y_tip = int(index_tip.y * 64)
                
                # Draw on the persistent image
                #draw_persistent.point((x_tip, y_tip), fill=str(sys.argv[1]))
                draw_persistent.point((x_tip, y_tip), fill=str(received_message))
                #draw_persistent.point((x_tip, y_tip), fill=str("red"))
                #print(sys.argv[1]))

                # Draw a crosshair at the current finger tip position
                crosshair_color = "blue"
                crosshair_size = 2
                draw.line((x_tip - crosshair_size, y_tip, x_tip + crosshair_size, y_tip), fill=crosshair_color)
                draw.line((x_tip, y_tip - crosshair_size, x_tip, y_tip + crosshair_size), fill=crosshair_color)

        # Update the matrix display with the updated matrix image
        matrix.SetImage(matrix_image.convert('RGB'))
        
        
        #matrix_image.save("art"+str(sys.argv[1])+".png")
        
        
        #print(type(matrix_image.convert('RGB').data))
        
        

        if cv2.waitKey(5) & 0xFF == 27:
            break

video_object.release()
cv2.destroyAllWindows()
matrix.Clear()
