import socket
HOST = '127.0.0.1'
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected by", addr)
while True:
    # Receive from client
    client_message = conn.recv(1024).decode()
    if not client_message:
        break
    print("Client:", client_message)
    # Send reply to client
    reply = input("Server: ")
    conn.send(reply.encode())
conn.close()
server.close()
