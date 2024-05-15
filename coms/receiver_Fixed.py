import socket
import subprocess
import signal
import os

local_ip = ""
port = 5000

receiver_socket = socket.socket()
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.bind((local_ip, port))

receiver_socket.listen()
sender_socket, sender_address = receiver_socket.accept()
print("Connection established with:", sender_address)

current_process = None

def kill_current_process():
    global current_process
    if current_process is not None:
        os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
        current_process.wait()
        current_process = None

try:
    while True:
        received_data = sender_socket.recv(1024)
        if not received_data:
            break
        received_message = received_data.decode().strip()
        
        print(f"Received message: {received_message}")
        
        # Kill current process if there is one
        kill_current_process()

        # Start new process based on the received message
        if received_message.startswith('art'):
            current_process = subprocess.Popen("sudo -E python3 drawWithGesture.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        elif received_message == "seg":
            current_process = subprocess.Popen("sudo -E python3 imageSegmentation.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        elif received_message == "pose":
            current_process = subprocess.Popen("sudo -E python3 pose2Display.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        elif received_message == "disco":
            current_process = subprocess.Popen("sudo -E python3 disco.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        elif received_message.startswith("gal_"):
            image_name = received_message.split('_')[1]
            current_process = subprocess.Popen(f"sudo -E python3 saved.py {image_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        elif received_message == "kill":
            subprocess.Popen("sudo reboot", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            break

        if current_process:
            print(f"Started process with PID: {current_process.pid}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    kill_current_process()
    print("Connection closed. Exiting.")
    receiver_socket.close()
    sender_socket.close()
