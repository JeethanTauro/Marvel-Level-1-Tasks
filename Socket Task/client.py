import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

nickname = input("Choose a nickname: ") # getting the user nickname

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Here we are creating a client socket
client.connect((HOST,PORT)) # Here we are connecting to the server using local host and port


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'Jeethan':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("an error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}' # ask for the nickname of the client
        client.send(message.encode('ascii')) # send the message to the server

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()