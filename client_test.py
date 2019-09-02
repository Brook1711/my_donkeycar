from new_models import tcp
import time
import sys
#input_ip = input("input the ip you want:")
str_ip = "192.168.43.203"
mytcp = tcp(SERVER_IP=str_ip)
mytcp.send_start()
while True:
    send_data = input("input data:")
    mytcp.send_steering_data(send_data)
    time.sleep(1)