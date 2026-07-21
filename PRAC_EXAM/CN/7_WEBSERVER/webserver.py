from socket import *

PORT = 8080
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(("localhost", PORT))
server.listen(1)

print(f"Server running at http://localhost:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected: {addr}")
    
    try:
        request = conn.recv(1024).decode()
        filepath = request.split()[1][1:] or "index.html"
        
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            
            response = b"HTTP/1.1 200 OK\r\n"
            response += b"Content-Type: text/html\r\n"
            response += b"Content-Length: " + str(len(data)).encode() + b"\r\n"
            response += b"\r\n"
            conn.sendall(response + data)
            print("Sent 200 OK")
        
        except FileNotFoundError:
            error = b"<html><body><h1>404 Not Found</h1></body></html>"
            response = b"HTTP/1.1 404 Not Found\r\n"
            response += b"Content-Type: text/html\r\n"
            response += b"Content-Length: " + str(len(error)).encode() + b"\r\n"
            response += b"\r\n"
            conn.sendall(response + error)
            print("Sent 404 Not Found")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        conn.close()
