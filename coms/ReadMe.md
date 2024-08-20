This folder contains the communication code used to facilitate TCP/IP socket communication between the Raspberry Pi Zero 2W and the Raspberry Pi 4B. The RPi Zero 2W is configured with a daemon service that initiates a Python script on boot-up, but only after an internet connection is established to ensure that the server is correctly set up. Once this is ready, the RPi 4B runs receiver code that listens for messages sent from the RPi Zero 2W.

Additionally, this folder includes code for four different modes:

1. Mirror Mode: Managed by "imageSegmentation.py"
2. Stick Mode: Handled by "pose2Display.py"
3. Disco Mode: Operated by "disco.py"
4. Art Mode: Controlled by "drawWithGesture.py"

These files correspond to the various functionalities offered by our setup.

## Mediapipe models
For the image processing, I used mediapipe library to have four modes- Mirror mode, Stick mode, Disco mode, and the Art mode. The Mirror Mode used the selfie segmentation model from the Mediapipe library, performing well for solo individuals with minimal latency but struggling with multiple people or close-up shots. Disco Mode employed the same mask as Mirror Mode, looping through rainbow colors for each frame. Stick Mode used the pose landmarks model to track 33 connections, showing poses on the screen with some latency. Art Mode leveraged the hand landmarks model to track the index tip for drawing, improving drawing smoothness by increasing the brush size, drawing every third frame, and reducing the resolution to 320x240 for faster processing. Additional features included an eraser, image saving, and color changes via the piTFT attached to the wrist.

## Backend Communication 
We approached communication between the Pi 0 and the RPi 4 using Python sockets. We utilized two ports, 5000 and 5001, to send messages from the Pi 0 to the RPi 4.
Port 5000 was dedicated to executing code scripts. These messages were used to run Mirror Mode, Draw Mode, or Gallery Mode. Once the Pi 0 sent the command, the receiver script, in the RPi 4, parsed it and executed the appropriate script file using the OS library and sudo -E command. Additionally, the receiver script tracked the running process and terminated it when switching modes.
Port 5001 handled all information related to selecting colors or naming the canvas when saving. This port was created and listened to by the drawing script, ensuring that all messages were directed to it. This also created a separation between the port that should only be listened to by the execution file, and the one that should only be listened to by the drawing file.

