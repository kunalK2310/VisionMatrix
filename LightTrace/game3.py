import pygame, pigame, sys
from buttons import Button
from pygame.locals import *
import datetime
import json
import os
import RPi.GPIO as GPIO
from time import sleep
import time
import socket


os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

receiver_ip = '10.49.88.187'
port = 5000

port_color = 5001





receiver_socket = socket.socket()
receiver_socket.connect((receiver_ip, port))
print("Connected to this IP: ", receiver_ip)


pygame.init()
pitft = pigame.PiTft()
screen = pygame.display.set_mode((320, 240))
BG = pygame.image.load("assets/background/background.png")
white = (255,255,255)
black= (0,0,0)
clock=pygame.time.Clock()
name_text = ""
window = None
save_data = {}
TimeOut=60
startTime = time.time()

pygame.mouse.set_visible(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_17(channel):
    print("Quit")
    GPIO.cleanup()
    sys.exit()

GPIO.add_event_detect(17, GPIO.FALLING, callback=button_17, bouncetime=300)

try:    
    with open('save_data.txt') as save_file:
        save_data=json.load(save_file)
except:
    print('No file created yet')


def get_font(size):
    return pygame.font.Font("assets/fonts/bronovo.ttf", size)


def preview(title):
    message = "gal_"+str(title)
    #message = "gal_art2"
    receiver_socket.send(message.encode())
    
    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        SAVE_CONFIRM_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Back", font=get_font(11), base_color=black)
        PREVIEW_TITLE = Button(image=None, pos=(160,122), text_input=title, font=get_font(22), base_color=black)

        #print(title)
        for button in [BACK_BUTTON, PREVIEW_TITLE]:
            button.update(screen)   

        for event in pygame.event.get():
            #if event.type == pygame.QUIT:
             #   pygame.quit()
              #  sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if BACK_BUTTON.checkForInput(SAVE_CONFIRM_MOUSE_POS):
                    gallery()

        pygame.display.update()

def gallery():
    global save_data
    sorted_data = sorted(save_data.items(), key=lambda item: item[1], reverse=True)
    
    # Page setup
    index = 0
    items_per_page = 5
    max_index = len(sorted_data) - items_per_page if len(sorted_data) > items_per_page else 0

    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        GALLERY_MOUSE_POS = pygame.mouse.get_pos()

        buttons = []
        title_buttons = []
        for i in range(items_per_page):
            data_index = index + i
            if data_index < len(sorted_data):
                title, date = sorted_data[data_index]
            else:
                # If there are no more entries, display empty slots
                title = "Empty"
                date = "Empty"

            date_button = Button(image=None, pos=(46, 85.5 + 28 * i), text_input=date, font=get_font(12), base_color=black)
            title_button = Button(image=pygame.image.load("assets/text_boxes/gallery.png"), pos=(163, 84.5 + 28 * i), text_input=title, font=get_font(12), base_color=black)
            buttons.extend([date_button, title_button])
            title_buttons.append(title_button)

        # Navigation buttons
        BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Exit", font=get_font(11), base_color=black)
        UP_BUTTON = Button(image=pygame.image.load("assets/buttons/up.png"), pos=(279.5, 115.5))
        DOWN_BUTTON = Button(image=pygame.image.load("assets/buttons/down.png"), pos=(279.5,155.5))
        NEWEST_BUTTON = Button(image=pygame.image.load("assets/buttons/skip.png"), pos=(279, 61.5), text_input="Newest", font=get_font(14), base_color=white)
        OLDEST_BUTTON = Button(image=pygame.image.load("assets/buttons/skip.png"), pos=(279,216.5), text_input="Oldest", font=get_font(14), base_color=white)
        GALLERY = Button(image=None, pos=(156, 33), text_input= "Gallery", font=get_font(18), base_color=black)
        buttons.extend([BACK_BUTTON, UP_BUTTON, DOWN_BUTTON, NEWEST_BUTTON, OLDEST_BUTTON, GALLERY])

        for button in buttons:
            button.update(screen)

        for event in pygame.event.get():
            #if event.type == pygame.QUIT:
             #   pygame.quit()
              #  sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(GALLERY_MOUSE_POS):
                    print("Main_Menu")
                    main_menu()
                elif UP_BUTTON.checkForInput(GALLERY_MOUSE_POS) and index > 0:
                    index -= 1
                elif DOWN_BUTTON.checkForInput(GALLERY_MOUSE_POS) and index < max_index:
                    index += 1
                elif NEWEST_BUTTON.checkForInput(GALLERY_MOUSE_POS):
                    index = 0
                elif OLDEST_BUTTON.checkForInput(GALLERY_MOUSE_POS):
                    index = max_index
                else:
                    for button in title_buttons:
                        if button.checkForInput(GALLERY_MOUSE_POS):
                            preview(button.text_input)
                            print("this is the gallery image")
                            print(button.text_input)

        pygame.display.update()


def name():
    global name_text, window
    window = "name"
    text_box_rect = pygame.Rect(50, 50, 220, 30)

    def handle_button_input(input_text):
        global name_text
        if input_text == "DEL":
            name_text = name_text[:-1]  # Remove the last character
        elif input_text == "SPACE":
            name_text += " "  # Add space
        elif input_text == "ENTER":
            save(name_text)  # Use the text to show user name
            name_text = ""  # Reset text after showing name
        else:
            if len(name_text) < 18:
                name_text += input_text 
        
    

    while True:
        pitft.update()
        time_delta = clock.tick(60)/1000.0
        screen.blit(BG, (0, 0))
        NAME_MOUSE_POS = pygame.mouse.get_pos()
        Q_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(34.5, 110.5), text_input="Q", font=get_font(17), base_color=white)
        W_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(61.5, 110.5), text_input="W", font=get_font(17), base_color=white)
        E_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(88.5, 110.5), text_input="E", font=get_font(17), base_color=white)
        R_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(115.5, 110.5), text_input="R", font=get_font(17), base_color=white)
        T_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(142.5, 110.5), text_input="T", font=get_font(17), base_color=white)
        Y_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(169.5, 110.5), text_input="Y", font=get_font(17), base_color=white)
        U_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(196.5, 110.5), text_input="U", font=get_font(17), base_color=white)
        I_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(223.5, 110.5), text_input="I", font=get_font(17), base_color=white)
        O_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(250.5, 110.5), text_input="O", font=get_font(17), base_color=white)
        P_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(277.5, 110.5), text_input="P", font=get_font(17), base_color=white)
        A_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(48.5, 144.5), text_input="A", font=get_font(17), base_color=white)
        S_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(75.5, 144.5), text_input="S", font=get_font(17), base_color=white)
        D_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(102.5, 144.5), text_input="D", font=get_font(17), base_color=white)
        F_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(129.5, 144.5), text_input="F", font=get_font(17), base_color=white)
        G_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(156.5, 144.5), text_input="G", font=get_font(17), base_color=white)
        H_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(183.5, 144.5), text_input="H", font=get_font(17), base_color=white)
        J_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(210.5, 144.5), text_input="J", font=get_font(17), base_color=white)
        K_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(237.5, 144.5), text_input="K", font=get_font(17), base_color=white)
        L_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(264.5, 144.5), text_input="L", font=get_font(17), base_color=white)
        Z_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(76.5, 179.5), text_input="Z", font=get_font(17), base_color=white)
        X_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(103.5, 179.5), text_input="X", font=get_font(17), base_color=white)
        C_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(130.5, 179.5), text_input="C", font=get_font(17), base_color=white)
        V_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(157.5, 179.5), text_input="V", font=get_font(17), base_color=white)
        B_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(184.5, 179.5), text_input="B", font=get_font(17), base_color=white)
        N_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(211.5, 179.5), text_input="N", font=get_font(17), base_color=white)
        M_BUTTON = Button(image=pygame.image.load("assets/text_boxes/key_text.png"), pos=(238.5, 179.5), text_input="M", font=get_font(17), base_color=white)
        SPACE_BUTTON = Button(image=pygame.image.load("assets/text_boxes/space_key.png"), pos=(154.5, 211.5), text_input="SPACE", font=get_font(19), base_color=white)
        ENTER_BUTTON = Button(image=pygame.image.load("assets/text_boxes/enter_key.png"), pos=(266.5, 211.5), text_input="ENTER", font=get_font(17), base_color=white)
        DEL_BUTTON = Button(image=pygame.image.load("assets/text_boxes/del_key.png"), pos=(279, 179.5), text_input="DEL", font=get_font(16), base_color=white)
        NAME = Button(image=None, pos=(159.5,24), text_input="Name", font=get_font(16), base_color=black)
        BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Back", font=get_font(11), base_color=black)
        
        
        button_list = [Q_BUTTON, W_BUTTON, E_BUTTON, R_BUTTON, T_BUTTON, Y_BUTTON, U_BUTTON, I_BUTTON, O_BUTTON, 
                       P_BUTTON, A_BUTTON, S_BUTTON, D_BUTTON, F_BUTTON, G_BUTTON, H_BUTTON, J_BUTTON, K_BUTTON, 
                       L_BUTTON, Z_BUTTON, X_BUTTON, C_BUTTON, V_BUTTON, B_BUTTON, N_BUTTON, M_BUTTON, SPACE_BUTTON,
                       DEL_BUTTON, ENTER_BUTTON]
        
        button_list2 = [NAME, BACK_BUTTON]
        
        for button in button_list:
            button.update(screen)
        for button in button_list2:
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in button_list:
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    if button.checkForInput(NAME_MOUSE_POS):
                        handle_button_input(button.text_input)
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if BACK_BUTTON.checkForInput(NAME_MOUSE_POS):
                    if len(name_text) == 0:
                        save(name_text)
                    else:
                        back_confirm()
        
        text_surface = get_font(24).render(name_text, True, pygame.Color('black'))
        screen.blit(text_surface, (text_box_rect.x + 5, text_box_rect.y + 5))  # Adjust text position inside the box
        pygame.draw.rect(screen, pygame.Color('white'), text_box_rect, 2) 

        pygame.display.update()
    
def back_confirm():
    global window, name_text
    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        SAVE_CONFIRM_MOUSE_POS = pygame.mouse.get_pos()
        YES_BUTTON = Button(image=pygame.image.load("assets/buttons/yes.png"), pos=(103,140), text_input="Yes", font=get_font(14), base_color=black)
        CANCEL_BUTTON = Button(image=pygame.image.load("assets/buttons/cancel.png"), pos=(215,140), text_input="Cancel", font=get_font(13), base_color=black)
        TEXT = Button(image=None, pos=(160,86), text_input="Are you sure that you dont want to save?", font=get_font(14), base_color=black)

        for button in [YES_BUTTON, CANCEL_BUTTON, TEXT]:
            button.update(screen)   

        for event in pygame.event.get():
          #  if event.type == pygame.QUIT:
           #     pygame.quit()
            #    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if YES_BUTTON.checkForInput(SAVE_CONFIRM_MOUSE_POS):
                    if window == "artmode":
                        #color_socket.close()
                        main_menu()
                    elif window == "save":
                        name_text=""
                        art_mode()
                    elif window == "name":
                        name_text=""
                        save(name_text)
                if CANCEL_BUTTON.checkForInput(SAVE_CONFIRM_MOUSE_POS):
                    if window == "artmode":
                        art_mode()
                    if window == "save":
                        save(name_text)
                    if window == "name":
                        name()

        pygame.display.update()

def save_confirm():
    global window, name_text
    current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        SAVE_CONFIRM_MOUSE_POS = pygame.mouse.get_pos()
        YES_BUTTON = Button(image=pygame.image.load("assets/buttons/yes.png"), pos=(113,179), text_input="Yes", font=get_font(14), base_color=black)
        CANCEL_BUTTON = Button(image=pygame.image.load("assets/buttons/cancel.png"), pos=(215,179), text_input="Cancel", font=get_font(13), base_color=black)
        TEXT = Button(image=None, pos=(160,59), text_input="Confirm Save?", font=get_font(14), base_color=black)
        NAME = Button(image=None, pos=(160.5,99), text_input=name_text, font=get_font(14), base_color=black)
        DATE = Button(image=None, pos=(160.5,119), text_input=current_date, font=get_font(14), base_color=black)

        for button in [YES_BUTTON, CANCEL_BUTTON, TEXT, NAME, DATE]:
            button.update(screen)   

        for event in pygame.event.get():
           # if event.type == pygame.QUIT:
            #    pygame.quit()
             #   sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if YES_BUTTON.checkForInput(SAVE_CONFIRM_MOUSE_POS):
                    save_data[name_text]=current_date
                    with open('save_data.txt','w') as save_file:
                        json.dump(save_data,save_file)
                    print(name_text)
                    message = "at_name_"+name_text
                    color_socket.send(message.encode())
                    
                    name_text=""
                    #print(name_text)
                    gallery()
                if CANCEL_BUTTON.checkForInput(SAVE_CONFIRM_MOUSE_POS):
                    save(name_text)

        pygame.display.update()

def save(name_text):
    global window
    window = "save"
    display_error = False
    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        SAVE_MOUSE_POS = pygame.mouse.get_pos()

        if display_error:
            title_input = "Name is Required"
            title_color = (255,0,0)
        else:
            title_input = name_text if name_text else ""
            title_color = black

        TITLE_BUTTON = Button(image=pygame.image.load("assets/text_boxes/save.png"), pos=(192,126), text_input=title_input, font=get_font(14), base_color=title_color)
        DATE_BUTTON = Button(image=None, pos=(134,166), text_input=datetime.datetime.now().date().strftime("%Y-%m-%d"), font=get_font(14), base_color=black)
        NAME = Button(image=None, pos=(52,126), text_input="Name:", font=get_font(14), base_color=black)
        DATE = Button(image=None, pos=(55,166), text_input="Date:", font=get_font(15), base_color=black)
        TEXT = Button(image=None, pos=(166,63), text_input="Save", font=get_font(16), base_color=black)
        BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Back", font=get_font(11), base_color=black)
        SAVE_BUTTON = Button(image=pygame.image.load("assets/buttons/save.png"), pos=(260,185), text_input="Save", font=get_font(13), base_color=black)

        for button in [TITLE_BUTTON, DATE_BUTTON, NAME, DATE_BUTTON, DATE, TEXT, BACK_BUTTON, SAVE_BUTTON]:
            button.update(screen)   

        for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
         #       pygame.quit()
          #      sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if BACK_BUTTON.checkForInput(SAVE_MOUSE_POS):
                    if len(name_text) == 0:
                        art_mode()
                    back_confirm()
                if TITLE_BUTTON.checkForInput(SAVE_MOUSE_POS):
                    name()
                if SAVE_BUTTON.checkForInput(SAVE_MOUSE_POS):
                    if len(name_text) == 0:
                        display_error = True  
                    else:
                        display_error = False  
                        save_confirm()

        pygame.display.update()

def art_mode():
    
    time.sleep(10)
    
    global color_socket
    color_socket = socket.socket()
    color_socket.connect((receiver_ip, port_color))
    print("Connected to color port: ", receiver_ip)
    
    #now = time.time()
    #elapsedTime = now - startTime
    #if elapsedTime > TimeOut:
    #    pygame.quit()
    #    sys.exit()
    global window
    window = "artmode"

    BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Back", font=get_font(11), base_color=black)
    SAVE_BUTTON = Button(image=pygame.image.load("assets/buttons/save.png"), pos=(260,185), text_input="Save", font=get_font(13), base_color=black)
    TITLE = Button(image=None, pos=(42,13), text_input="Art Mode", font=get_font(12), base_color=black)

    YELLOW = Button(image=pygame.image.load("assets/circles/yellow.png"), pos=(52,86))
    YELLOW_CLICKED = Button(image=pygame.image.load("assets/circles/yellow_clicked.png"), pos=(52,86))
    RED = Button(image=pygame.image.load("assets/circles/red.png"), pos=(145,33))
    RED_CLICKED = Button(image=pygame.image.load("assets/circles/red_clicked.png"), pos=(145,33))
    BLUE_CLICKED = Button(image=pygame.image.load("assets/circles/blue_clicked.png"), pos=(46,187))
    BLUE = Button(image=pygame.image.load("assets/circles/blue.png"), pos=(46,187))
    VIOLET_CLICKED = Button(image=pygame.image.load("assets/circles/violet_clicked.png"), pos=(96,210))
    VIOLET = Button(image=pygame.image.load("assets/circles/violet.png"), pos=(96,210))
    WHITE_CLICKED = Button(image=pygame.image.load("assets/circles/white_clicked.png"), pos=(152,197))
    WHITE = Button(image=pygame.image.load("assets/circles/white.png"), pos=(152,197))
    ORANGE_CLICKED = Button(image=pygame.image.load("assets/circles/orange_clicked.png"), pos=(94,53))
    ORANGE = Button(image=pygame.image.load("assets/circles/orange.png"), pos=(94,53))
    GREEN_CLICKED = Button(image=pygame.image.load("assets/circles/green_clicked.png"), pos=(34,136))
    GREEN = Button(image=pygame.image.load("assets/circles/green.png"), pos=(34,136))
    ERASE = Button(image=pygame.image.load("assets/buttons/erase.png"), pos=(256,98), text_input="Erase", font=get_font(15), base_color=black)
    ERASE_CLICKED = Button(image=pygame.image.load("assets/buttons/erase_clicked.png"), pos=(256,98), text_input="Erase", font=get_font(15), base_color=(213,212,217))

    button_on = ["ERASE"]

    colors = {"YELLOW" : {"state": False, "clicked": YELLOW_CLICKED, "unclicked": YELLOW}, 
               "RED" : {"state": False, "clicked": RED_CLICKED, "unclicked": RED},
               "BLUE" : {"state": False, "clicked": BLUE_CLICKED, "unclicked": BLUE},
               "VIOLET" : {"state": False, "clicked": VIOLET_CLICKED, "unclicked": VIOLET},
               "WHITE" : {"state": False, "clicked": WHITE_CLICKED, "unclicked": WHITE},
               "ORANGE" : {"state": False, "clicked": ORANGE_CLICKED, "unclicked": ORANGE},
               "GREEN" : {"state": False, "clicked": GREEN_CLICKED, "unclicked": GREEN},
               "BLACK": {"state": False, "clicked": ERASE_CLICKED, "unclicked": ERASE}}
    
    def is_any_color_active():
        return any(value['state'] for key, value in colors.items() if key != "ERASE")

    def update_buttons(button_dict, screen):
        for key, value in button_dict.items():
            if value['state']:
                value['clicked'].update(screen)
            else:
                value['unclicked'].update(screen)

    def check_clicked(button_dict):
        nonlocal button_on
        for key, value in button_dict.items():
            if value['unclicked'].checkForInput(ART_MOUSE_POS) or value['clicked'].checkForInput(ART_MOUSE_POS):
                if button_on[0] != key:
                    if button_on[0] in button_dict:
                        button_dict[button_on[0]]['state'] = False
                    button_on[0] = key
                value['state'] = not value['state']
                message = str(key.lower())
                print(message)
                color_socket.send(message.encode())

    while True:
        pitft.update()
        screen.blit(BG, (0, 0))
        ART_MOUSE_POS = pygame.mouse.get_pos()

        update_buttons(colors, screen)
        
        for button in [BACK_BUTTON, SAVE_BUTTON, TITLE]:
            button.update(screen)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_clicked(colors)
                if BACK_BUTTON.checkForInput(ART_MOUSE_POS):
                    if is_any_color_active():
                        back_confirm()
                    color_socket.close()
                    main_menu()
                if SAVE_BUTTON.checkForInput(ART_MOUSE_POS):
                    save(name_text)

        pygame.display.update()


def mirror_mode():
    while True:
        pitft.update()
        screen.blit(BG, (0,0))
        MIRROR_MODE_MOUSE_POS = pygame.mouse.get_pos()
        BACKGROUND_1 = Button(image=pygame.image.load("assets/buttons/background.png"), pos=(161,66), text_input="Mirror", font=get_font(16), base_color=black)
        BACKGROUND_2 = Button(image=pygame.image.load("assets/buttons/background.png"), pos=(161,131), text_input="Stick", font=get_font(16), base_color=black)
        BACKGROUND_3 = Button (image=pygame.image.load("assets/buttons/background.png"), pos=(161,196), text_input="Disco", font=get_font(16), base_color=black)
        BACK_BUTTON = Button(image=pygame.image.load("assets/buttons/back.png"), pos=(282,20), text_input="Back", font=get_font(11), base_color=black)
        TITLE = Button(image=None, pos=(45,13), text_input="Mirror Mode", font=get_font(12), base_color=black)
 

        for button in [BACKGROUND_1, BACKGROUND_2, BACKGROUND_3, BACK_BUTTON, TITLE]:
            button.update(screen)  
            

        for event in pygame.event.get():
         #   if event.type == pygame.QUIT:
          #      pygame.quit()
           #     sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if BACKGROUND_1.checkForInput(MIRROR_MODE_MOUSE_POS):
                    print("BACKGROUND 1")
                    message = "seg"
                    receiver_socket.send(message.encode())
                if BACKGROUND_2.checkForInput(MIRROR_MODE_MOUSE_POS):
                    print("BACKGROUND 2")
                    message = "pose"
                    receiver_socket.send(message.encode())
                if BACKGROUND_3.checkForInput(MIRROR_MODE_MOUSE_POS):
                    print("BACKGROUND 3")
                    message = "disco"
                    receiver_socket.send(message.encode())
                if BACK_BUTTON.checkForInput(MIRROR_MODE_MOUSE_POS):
                    print("back")
                    main_menu()
        pygame.display.update()

def main_menu(): # main menu screen

    message_sent = False  # Flag to track if the message has been sent

    while True:
        if not message_sent:
            message = "menu"
            receiver_socket.send(message.encode())
            message_sent = True

        pitft.update()
        screen.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MIRROR_BUTTON = Button(image=pygame.image.load("assets/buttons/mirror.png"), pos=(88,146), text_input="Mirror Mode", font=get_font(15), base_color=black)
        ART_BUTTON = Button(image=pygame.image.load("assets/buttons/art.png"), pos=(228,146), text_input="Art Mode", font=get_font(15), base_color=black)
        GALLERY_BUTTON = Button (image=pygame.image.load("assets/buttons/gallery.png"), pos=(159.5,202), text_input="Enter the Gallery", font=get_font(15), base_color=black)
        TITLE = Button (image=pygame.image.load("assets/text/title.png"), pos=(162,63))
        QUIT = Button (image=pygame.image.load("assets/buttons/quit.png"), pos=(20,20))


        for button in [MIRROR_BUTTON, ART_BUTTON, GALLERY_BUTTON, TITLE, QUIT]:
            button.update(screen) 

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if MIRROR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mirror_mode()
                if ART_BUTTON.checkForInput(MENU_MOUSE_POS):
                    message = "art"
                    receiver_socket.send(message.encode())
                    art_mode()
                if GALLERY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    gallery()
                if QUIT.checkForInput(MENU_MOUSE_POS): 
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

main_menu()

