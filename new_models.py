import time
import donkeycar as dk
import socket
import sys
class SENDSTEERINGPulse:
    LEFT_ANGLE = -1 
    RIGHT_ANGLE = 1

    def __init__(self, tcp_sender = None,
                       left_pulse=290,
                       right_pulse=490):

        # self.controller = controller
        self.tcp_sender = tcp_sender
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse


    def run(self, angle):
        #map absolute angle to angle that vehicle can implement.
        pulse = dk.utils.map_range(angle,
                                self.LEFT_ANGLE, self.RIGHT_ANGLE,
                                self.left_pulse, self.right_pulse)

        #print(pulse)
        pulse = str(pulse)
        self.tcp_sender.send_steering_data(pulse)

    def shutdown(self):
        self.run(0) #set steering straight

class SENDThrottlePulse:
    """
    Wrapper over a PWM motor cotnroller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE =  1

    def __init__(self, tcp_sender = None,
                       max_pulse=300,
                       min_pulse=490,
                       zero_pulse=350):
        self.tcp_sender = tcp_sender
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse


    def run(self, throttle):
        if throttle > 0:
            pulse = dk.utils.map_range(throttle,
                                    0, self.MAX_THROTTLE, 
                                    self.zero_pulse, self.max_pulse)
        else:
            pulse = dk.utils.map_range(throttle,
                                    self.MIN_THROTTLE, 0, 
                                    self.min_pulse, self.zero_pulse)

        #print(pulse)
        pulse=str(pulse)
        self.tcp_sender.send_throttle_data(pulse)
        
    def shutdown(self):
        self.run(0) #stop vehicle


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
