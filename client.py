import socket
import time
import sys
#RPi's IP
SERVER_IP = "192.168.43.7"
SERVER_PORT = 8888

print("Starting socket: TCP...")
server_addr = (SERVER_IP, SERVER_PORT)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
        socket_tcp.connect(server_addr)
        break
    except Exception:
        print("Can't connect to server,try it latter!")
        time.sleep(1)
        continue
print("Please input 1 or 0 to turn on/off the led!")
while True:
    try:
        data = socket_tcp.recv(512)
        if len(data)>0:
            print("Received: %s" % data)
            command = input("command is ")
            command = str(command)
            socket_tcp.send(command.encode("utf-8"))
            time.sleep(1)
            continue
    except Exception:
        socket_tcp.close()
        socket_tcp=None
        sys.exit(1)
