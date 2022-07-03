import threading
from socket import *


server = socket(AF_INET, SOCK_STREAM)
# localhost
host_ip = '127.0.0.1'
# don't choose a port between 0 and 1024
host_port = 4646

server.bind((host_ip, host_port))

server.listen()

print('Server is listening...')

clients = []
addresses = []

# send a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# manage client connection
def manage(client):
    while True:
        try:
            message = client.recv(1234)

            # if client wants to leave the chat room
            if str(message.decode('ascii'))[-5:].lower() == 'leave':
                remove_client(client)
                break

            broadcast(message)
        except:
            remove_client(client)
            break

# remove client from clients list and broadcast it to other clients 
def remove_client(client):
    index = clients.index(client)
    address = addresses[index]
    message = f'{address} has left chat room.'.encode('ascii')

    # remove client and it's address
    addresses.remove(address)
    clients.remove(client)

    # broadcast it
    broadcast(message)

    client.close()

def receive():
    while True:
        # new client has connected
        client, address = server.accept()
        print(f'Connected with {address}')

        # save client and it's address
        clients.append(client)
        addresses.append(address)

        # tell clients that new client has joined
        broadcast(f'{address} has joined to the server.'.encode('ascii'))

        # tell client that connected to server
        client.send(f'Connected to the server.'.encode('ascii'))

        # create thread for each client
        create_thread(client)


# create a new thread for new client
def create_thread(client):
    thread = threading.Thread(target=manage, args=(client,))
    thread.start()

receive()