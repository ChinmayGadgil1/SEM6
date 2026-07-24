import socket
import threading

HOST = "127.0.0.1"
PORT = 8888


def handle_client(client):
    request = client.recv(4096)
    text = request.decode()
    host = ""

    for line in text.split("\n"):
        if line.startswith("Host:"):
            host = line.split(":")[1].strip()
            break

    print("Connecting to:", host)
    server = socket.socket()
    server.connect((host, 80))
    server.send(request)
    while True:
        data = server.recv(4096)

        if not data:
            break

        client.send(data)

    server.close()
    client.close()

proxy = socket.socket()
proxy.bind((HOST, PORT))
proxy.listen(5)

print(f"Proxy running on {HOST}:{PORT}")

while True:
    client, addr = proxy.accept()
    print("Connected:", addr)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()