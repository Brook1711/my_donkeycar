from client_on_pi import tcp

mytcp = tcp()
mytcp.send_start()
while True:
    command = input("command is ")
    command = str(command)
    mytcp.send_steering_data(angle=command)