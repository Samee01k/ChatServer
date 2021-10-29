import socket
import threading
import datetime


host = socket.gethostname()
port = 65535

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host,port))
s.listen()

clients = []
users = []

def broadcast(message):     #broadcasts the message to all the clients
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = users[index] 
            broadcast(f'{user} left the chat!'.encode('ascii'))
            users.remove(user)
            break
    
def receive(): 
    while True:
        client, address = s.accept() #accepts the clients
        print(f'Connected with {str(address)}')
        
        client.send('user'.encode('ascii')) #requests for the user's name
        user = client.recv(1024).decode('ascii') #receives the user's name
        users.append(user) #adds the user
        clients.append(client)

        print(f"The user's name is {user}")
        broadcast(f"{user} joined the chat!".encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is active...")
receive()            
