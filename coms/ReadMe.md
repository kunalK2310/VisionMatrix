This folder contains the communication code used to facilitate TCP/IP socket communication between the Raspberry Pi Zero 2W and the Raspberry Pi 4B. The RPi Zero 2W is configured with a daemon service that initiates a Python script on boot-up, but only after an internet connection is established to ensure that the server is correctly set up. Once this is ready, the RPi 4B runs receiver code that listens for messages sent from the RPi Zero 2W.

Additionally, this folder includes code for four different modes:

a*Mirror Mode: Managed by imageSegmentation.py
*Stick Mode: Handled by pose2Display.py
*Disco Mode: Operated by disco.py
*Art Mode: Controlled by drawWithGesture.py
These files correspond to the various functionalities offered by our setup.
