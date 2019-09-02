from client_on_pi import tcp

the_ip = input("the ip : ")
mytcp = tcp(SERVER_IP='192.168.137.190')
mytcp.send_start()

while True:
    #command = input("command is ")
    #command = str(command)
    mytcp.send_steering_data(angle='X1')
    mytcp.send_steering_data(angle='Y2')
    mytcp.send_steering_data(angle='A3')
    mytcp.send_steering_data(angle='B4')