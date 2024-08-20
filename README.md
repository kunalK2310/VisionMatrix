# VisionMatrix

In this project, we developed Vision Matrix, an interactive art installation designed to engage users through dynamic visual representations. We utilized a combination of two Raspberry Pis, a PiTFT display, an LED matrix, and a camera to bring this concept to life. The installation captures the intersection of technology and art, transforming real-time video data into interactive displays on an LED matrix.
The Vision Matrix operates through a dual-system setup. The primary Raspberry Pi processes video inputs to create real-time art manifestations such as silhouettes and gesture drawings, which are then displayed on the LED matrix. The secondary Raspberry Pi serves as an interactive control panel via the PiTFT display, allowing uses to select between three mode:
Mirror Mode: Mirrors users' movements and gestures.
Art Mode: Allows users to draw freely and choose colors.
Gallery Mode: Displays a collection of previously saved drawings.


In order to get this done, we broke down our development process into three areas:
Front End: The user interface that facilitates mode selection, enhancing the accessibility and usability of the interactive features.
Back End Processing: Dedicated to the core functionalities of video processing, display outputs, and data storage, ensuring that the artistic representations are both visually appealing and promptly responsive.
Back End Communication Protocol: A framework that allows the communication between the front-end and back-end systems.

![image](https://github.com/user-attachments/assets/6dfdec4e-3196-4b39-8b8c-0e37c43fbdaa)


## Mirror Mode
In Mirror Mode, users can interact with our LED display, which offers a variety of user segmentation backgrounds captured by our camera. Users have the option to choose from a range of predefined backgrounds, and their image is displayed on the LED screen. This mode includes several features: a stick figure mode, a disco segmentation mode, and a standard segmentation mode.
![image](https://github.com/user-attachments/assets/fa39db93-e4b5-457c-81b0-73706c6246ba)

![image](https://github.com/user-attachments/assets/07f45789-ca9e-4cb5-b2fe-25ffb80d4dee)

## Stick Mode
![image](https://github.com/user-attachments/assets/08c9376d-deb8-4c2e-bd8d-36486dd2f2f9)

## Art Mode
In Art Mode, users can engage with an interactive drawing feature on our LED display. The mode intends to allow users to express themselves artistically by providing them a selection of colors. Users can browse through these colors and use them to draw directly onto the LED display.  Drawings created in this mode are stored and can be viewed later in the gallery, allowing users to illustrate their artwork at their convenience.
![image](https://github.com/user-attachments/assets/611d9cb3-eb43-4fcf-9bf5-e17e4183294a)
![image](https://github.com/user-attachments/assets/622ba30b-f1e6-4310-998e-74c5ccd74209)

## Masterpiece
![image](https://github.com/user-attachments/assets/1f46ca10-c7bc-45a3-99bc-2ec35437722e)

## Wiring
To provide a larger interactive canvas for the user, we connected two LED matrices. We achieved this by 3D printing small adapters that attached to the back of each LED display, enabling us to chain them together. Additionally, we designed a mount to conveniently position our camera at the top of the LED matrix.

The RGB LED matrix design involved wiring two 32x64 RGB matrices in a parallel chain to a Raspberry Pi, creating a 64x64 square panel for a better viewing experience. Parallel wiring was chosen over daisy-chaining to achieve a higher refresh rate and ease of displaying images. Although daisy-chaining would require splitting the image, vertical splitter mode in the rpi-rgb-led-matrix library by hzeller (https://github.com/hzeller/rpi-rgb-led-matrix) could facilitate this. However, parallel wiring offered a simpler solution with up to three parallel chains.

![image](https://github.com/user-attachments/assets/1067310a-70d4-45de-905a-5201a459608e)


