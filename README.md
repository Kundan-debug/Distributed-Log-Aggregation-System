# Distributed-Log-Aggregation-System
Course: Computer Networks – Socket Programming Mini Project

Students:
- Kundan V – PES1UG24CS243
- Kuncha Pranay Krishna – PES1UG24CS242
- Anusri Sharma – PES1UG25CS803

## Project Overview
This project implements a distributed log aggregation system using UDP socket programming for fast, connectionless communication suitable for real-time log transmission. Multiple clients execute system commands (such as ls, pwd, whoami, date, uname on Unix-based systems and dir, cd, whoami, date, ver on Windows) and send their outputs as encrypted log messages over the network to a centralized aggregation server. The server decrypts the logs, timestamps them upon arrival, orders them accordingly, and processes them in real time while supporting multiple concurrent clients, ensuring scalability.

The system evaluates performance using throughput measurement (logs per second) and incorporates basic optimization through backpressure handling by limiting the log queue size to prevent memory overload. It also considers failure scenarios inherent to UDP communication, such as packet loss, out-of-order delivery, and potential decryption errors. Basic log filtering is implemented at the server to categorize logs based on command type. Logs are derived from actual system command outputs, making the system more realistic compared to simulated logging approaches.

## Features
- UDP Socket Communication – Low-level socket implementation  
- Connectionless Communication – No handshake required between client and server  
- Cryptographic Security – Logs are encrypted at the client and decrypted at the server using symmetric key cryptography (Fernet)  
- Real-Time Log Streaming – Clients continuously send log data  
- Multi-Client Support – Multiple clients can send logs simultaneously  
- Time Ordering – Logs are ordered using timestamps generated at the server upon reception  
- Throughput Evaluation – Server measures logs received per second  
- Backpressure Handling – Server queue limit prevents overload  
- Basic Failure Handling – Decryption errors are handled and socket timeout is used to avoid blocking during data reception  
- Real System Logs – Logs are generated from actual command outputs instead of artificial messages  
- Log Filtering – Server categorizes logs based on command type or content  

## System Architecture
<p align="center">
  <img src="Architecture/Architecture.png" width="50%">
</p>

Clients execute system commands and send their outputs as logs to the server through the network using UDP sockets.  
Clients support cross-platform command execution, adapting commands based on the operating system (Windows or Unix-based systems).  
The aggregation server receives, decrypts, and processes logs in real time.

Logs are encrypted at the client and decrypted at the server using symmetric key cryptography (Fernet) to ensure secure transmission.

## Communication Model
Client sends log message:  
`timestamp | client_id | command | output`  

Example:  
```1717578803.7720332 | Windows_4832 | ls | file1.txt file2.txt```  

Each log message is sent as a UDP datagram from the client to the server without establishing a connection, and without any guarantee of delivery or ordering.  
Server receives, decrypts, and processes logs while maintaining time ordering based on timestamps generated at the server upon reception.  
No retransmission or acknowledgment mechanism is implemented, making the system lightweight but unreliable.

## Installation & Setup
Prerequisites:
- Python 3
- Devices connected to the same network
- Cryptography library (Fernet-based encryption) installed

Both client and server must be connected to the same local network for UDP communication.

Setup Steps:  
Clone the Repository
```bash
git clone <your-repo-url>
cd Distributed-Log-Aggregation-System
```
Ensure Python is Installed
```bash
python3 --version
```
Install Required Libraries
```bash
pip install cryptography
```
This library is used for encrypting logs at the client and decrypting them at the server using symmetric key cryptography (Fernet).

Generate a Secret Key (Run Once)
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
```
Update the Secret Key in Client.py and Server.py  
The same key must be used in both client and server for successful encryption and decryption.
```python
key = b'PASTE_YOUR_KEY_HERE'
```
Find Server IP Address  
Mac:
```bash
ipconfig getifaddr en0
```
Linux:
```bash
hostname -I
```
Windows:
```bash
ipconfig
```
Update the server IP in Client.py
```python
SERVER_IP = "YOUR_SERVER_IP"
```
Ensure the client uses the correct server IP address; otherwise, logs will not be received.

## Usage
Start the Server:
```bash
python3 Server.py
```
Expected output  

```
Server listening...  
NORMAL LOG [('IP', port)] ...  
FILE LOG [('IP', port)] ...  
Throughput: X logs/sec | Dropped: Y
```

Ensure the server is running before starting any clients.

Start the Client:
```bash
python3 client.py
```
Clients will start sending log messages continuously to the server.  
Each client generates a unique client ID based on the operating system and a random identifier.

Multi-Client Execution:  
Run multiple clients on different systems or multiple terminals on the same system.  

Example:
```bash
python3 client.py
python3 client.py
python3 client.py
```
The server will receive, decrypt, order, and process logs from all clients simultaneously in real time.

## Performance Evaluation
The server measures performance using throughput and drop rate as:  
```Throughput: XX logs/sec | Dropped: YY```  

Throughput indicates how many logs the server can process per second under continuous load, while the dropped log count reflects how many logs were discarded due to backpressure when the server is overloaded.  
These metrics are used to evaluate system performance, scalability, and behavior under high traffic conditions.

## Backpressure Handling
To prevent memory overload:
- Server log queue is limited to 100 logs  
- New incoming logs are dropped when the queue limit is reached  
- The number of dropped logs is tracked for performance analysis

This ensures stable performance and prevents unbounded memory growth during high log traffic.

## Sample Output
Example server output:
```
FILE LOG [('10.x.x.x', 56672)] Windows_4832 | ls | file1.txt file2.txt
NORMAL LOG [('10.x.x.x', 56672)] Windows_4832 | pwd | /home/user
Throughput: 25 logs/sec | Dropped: 2
```

The output displays the client IP, port, command executed, corresponding output, log category, and real-time performance metrics.  
Each entry represents a log received as a UDP datagram from a client.  
Logs are decrypted at the server before processing and display, and are categorized based on command type or content.

## Technologies Used
Language: Python  
Networking: UDP Sockets  
Libraries: socket, time, random, subprocess, platform, cryptography  
Cryptography: Fernet (symmetric key encryption)  
Operating Systems: Cross-platform (Windows, Linux, macOS)

## Project Structure
```
Distributed-Log-Aggregation-System/
│
├── Architecture/
│   └── Architecture.png
├── Client/
│   └── Client.py
├── Output/
│   ├── Client.png
│   └── Server.png
├── Server/
│   └── Server.py
├── .gitignore
└── README.md
```

## Future Improvements
Secure communication using DTLS (Datagram Transport Layer Security) for secure and authenticated UDP communication  
Key management and secure key exchange mechanisms  
Log storage in database  
Advanced log filtering and search capabilities using indexing and pattern matching  
Web dashboard for monitoring  
Visualization of log statistics  
Reliable delivery mechanisms (acknowledgment and retransmission)  
Load balancing for handling high-volume log traffic  
Enhanced failure handling and retry mechanisms for improved reliability

## License
This project is created for educational purposes as part of a Computer Networks mini project.
