from socket import *

PORT = 8080

server = socket()
server.bind(("localhost", PORT))
server.listen(1)

print(f"Server running at http://localhost:{PORT}")

while True:
    conn, addr = server.accept()

    request = conn.recv(1024).decode()
    filename="index.html"

    with open(filename, "rb") as file:
        data = file.read()

    header = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(data)}\r\n"
        f"Content-Type: text/html\r\n\r\n"
    )
    conn.send( header.encode()+ data)
    print("200 OK")

    
    conn.close()