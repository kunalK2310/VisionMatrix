import socket


def parse_message(message):
    if message.startswith('art_'):
        color = message.split('_')[1]
        color_code = {'red': 'AR', 'orange': 'AO', 'yellow': 'AY', 'green': 'AG',
                      'blue': 'AB', 'purple': 'AP', 'black': 'ABk', 'white': 'AW'}
        return color_code.get(color, '')
    elif message.startswith('mirror_'):
        number = message.split('_')[1]
        return 'M' + number
    elif message.startswith('gallery_'):
        imagename = message.split('_')[1]
        return 'G' + imagename.capitalize()
    return False  # this will never occurs, just for testing purposes


receiver_ip = ''  # receiver
port = 5000

receiver_socket = socket.socket()
receiver_socket.connect((receiver_ip, port))
print("Connected to this IP: ", receiver_ip)

while True:
    message = input("Type here: ")
    parsed_message = parse_message(message)
    if parsed_message:
        receiver_socket.send(parsed_message.encode())
    else:
        print("Invalid input")
