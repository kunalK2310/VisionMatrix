import cv2
import mediapipe as mp
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import sys
import time
#from receiver import received_message

# LED Matrix setup
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 2
options.hardware_mapping = 'regular'
options.gpio_slowdown = 5
matrix = RGBMatrix(options=options)

image_path = str(sys.argv[1])+'.png'

image = Image.open(image_path)

#image = image.resize((64,64), Image.LANCZOS)

matrix.SetImage(image.convert("RGB"))

time.sleep(10)


video_object.release()
cv2.destroyAllWindows()
matrix.Clear()