import socket
import time
import sys

class tcp:


    def __init__(self, SERVER_IP = "192.168.43.7",SERVER_PORT = 8888):
        self.server_addr = (SERVER_IP, SERVER_PORT)
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_start(self):
        self.socket_tcp.connect(self.server_addr)
    def send_steering_data(self, angle = '270'):
        self.socket_tcp.send(angle.encode("utf-8"))
    def send_throttle_data(self, throttle = '0'):
        self.socket_tcp.send(throttle.encode("utf-8"))
    def send_stop(self):
        self.socket_tcp.close()