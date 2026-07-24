import socket

HOST = "127.0.0.1"
PORT = 12345

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)
print("Waiting for client...")
conn, addr = server.accept()
print("Connected by", addr)

while True:
    # Receive message from client
    message = conn.recv(1024).decode()

    if message == "close":
        print("Client disconnected.")
        conn.close()
        break

    print("Client:", message)

    # Send reply
    reply = input("Server: ")
    conn.send(reply.encode())

server.close()