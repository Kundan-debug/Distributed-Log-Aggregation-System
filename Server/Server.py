import socket
import time
from cryptography.fernet import Fernet

SERVER_IP = "0.0.0.0"
PORT = 9999

key = b'PASTE_YOUR_KEY_HERE'
cipher = Fernet(key)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))

sock.settimeout(1)

print("Server listening...")

logs = []

count = 0
start = time.time()

MAX_LOGS = 100

while True:
    try:
        data, addr = sock.recvfrom(4096)
    except socket.timeout:
        continue

    try:
        message = cipher.decrypt(data).decode()
    except Exception as e:
        print(f"Decryption failed from {addr}: {e}")
        continue

    timestamp = time.time()
    logs.append((timestamp, message))

    if len(logs) > MAX_LOGS:
        logs.pop(0)

    if "error" in message.lower():
        print(f"ERROR LOG [{addr}] {message}")
    elif "ls" in message:
        print(f"FILE LOG [{addr}] {message}")
    else:
        print(f"[{addr}] {message}")

    count += 1

    if time.time() - start >= 1:
        print(f"Throughput: {count} logs/sec")
        count = 0
        start = time.time()