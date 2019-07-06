from new_models import tcp
import time
import sys
input_ip = input("input the ip you want:")
str_ip = str(input_ip)
mytcp = tcp(SERVER_IP=str_ip)
mytcp.send_start()
while True:
    mytcp.send_steering_data('ok')
    time.sleep(1)