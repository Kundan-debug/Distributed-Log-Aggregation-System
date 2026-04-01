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

MAX_LOGS = 100
DROP_COUNT = 0

count = 0
start = time.time()

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

    if len(logs) >= MAX_LOGS:
        DROP_COUNT += 1
        print("Server overloaded! Dropping logs...")
        continue

    logs.append((timestamp, message))

    logs.sort(key=lambda x: x[0])

    msg_lower = message.lower()

    if "error" in msg_lower:
        print(f"ERROR LOG [{addr}] {message}")
    elif any(cmd in msg_lower for cmd in ["dir", "ls"]):
        print(f"FILE LOG [{addr}] {message}")
    else:
        print(f"NORMAL LOG [{addr}] {message}")

    count += 1

    if time.time() - start >= 1:
        print(f"\nThroughput: {count} logs/sec | Dropped: {DROP_COUNT}\n")
        count = 0
        DROP_COUNT = 0
        start = time.time()