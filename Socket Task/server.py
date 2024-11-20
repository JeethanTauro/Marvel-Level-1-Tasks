import socket
import threading

#AF_INET means ipv4
#SOCK_STREAM means TCP

host = '127.0.0.1' # local host on which the server is hosted
port = 1234 # the port getting used, the server listens through this port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating the server socket

server.bind((host,port)) # binding the host and the port to the server

server.listen() #listening to clients

clients  = [] # list of the client connected to the server
nicknames = []# list of the nickname of the clients connected to the server

# this is the function that sends the message to every client
def broadcast(message):
    for client in clients:
        client.send(message) #not encoding it because here we are sending to all the clients


def handle_client(client):
    while True:
        try:
            message = client.recv(1024) # Receive data from the client (up to 1024 bytes) and decode it
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)

def receive():
    while True:
        client_comm,address = server.accept()
        print(f"connected with the address : {address}")
        client_comm.send('Jeethan'.encode('ascii'))
        nickname = client_comm.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client_comm)

        print(f"name of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client_comm.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle_client,args=(client_comm,))
        thread.start()


print("Server is up and running")
receive()
