import threading
from socket import *


client = socket(AF_INET, SOCK_STREAM)

server_ip = '127.0.0.1'
server_port = 4646

client.connect((server_ip,server_port))

ip, port = client.getsockname()

def receive():
    while True:
        try:

            message = client.recv(1234).decode('ascii')
            print(message)

        except:

            print('An error occurred')
            client.close()
            break

def write():
    while True:
        message = f'{ip},{port} : {input()}'.encode('ascii')
        client.send(message)

def create_thread(function_target):
    thread = threading.Thread(target=function_target)
    thread.start()

create_thread(receive)
create_thread(write)
