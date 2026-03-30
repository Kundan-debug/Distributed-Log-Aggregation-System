import socket
import time
import subprocess
import random
from cryptography.fernet import Fernet

SERVER_IP = "YOUR_SERVER_IP"
PORT = 9999

key = b'PASTE_YOUR_KEY_HERE'
cipher = Fernet(key)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_id = "WINDOWS_CLIENT"

commands = ["ls", "pwd", "whoami", "date", "uname"]

while True:
    command = random.choice(commands)
    
    try:
        output = subprocess.getoutput(command)
    except Exception as e:
        output = str(e)

    log = f"{time.time()} | {client_id} | {command} | {output}"
    
    encrypted_log = cipher.encrypt(log.encode())
    
    sock.sendto(encrypted_log, (SERVER_IP, PORT))
    
    print("Sent:", log)
    
    time.sleep(2)