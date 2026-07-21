import socket
HOST = '127.0.0.1'
PORT = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connected to server!")
while True:
    # Send message
    message = input("Client: ")
    if(message=='close'):
        client.send(message.encode())
        client.close()
        break
    client.send(message.encode())
    # Receive reply
    server_reply = client.recv(1024).decode()
    print("Server:", server_reply)
