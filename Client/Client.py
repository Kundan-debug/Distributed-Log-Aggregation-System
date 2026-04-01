import socket
import time
import subprocess
import random
import platform
from cryptography.fernet import Fernet

SERVER_IP = "YOUR_SERVER_IP"
PORT = 9999

key = b'PASTE_YOUR_KEY_HERE'
cipher = Fernet(key)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

system_name = platform.system()
client_id = f"{system_name}_{random.randint(1000,9999)}"

if system_name == "Windows":
    commands = ["dir", "cd", "whoami", "date", "ver"]
else:
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

    print(f"[{client_id}] Sent:", log)

    time.sleep(random.uniform(1, 3))