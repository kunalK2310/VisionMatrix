import socket

receiver_ip = ''
port = 5000

receiver_socket = socket.socket()
receiver_socket.connect((receiver_ip, port))
print("Connected to this IP: ", receiver_ip)

while True:
    message = input("Type here: ")
    receiver_socket.send(message.encode())
