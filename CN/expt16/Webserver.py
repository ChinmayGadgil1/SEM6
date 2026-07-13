from socket import *
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print(f"Server running at http://localhost:{serverPort}")
while True:
    print("\nWaiting for connection...")
    connectionSocket, addr = serverSocket.accept()
    print("Connected by:", addr)
    try:
        message = connectionSocket.recv(1024).decode()
        print("\nREQUEST:\n")
        print(message)
        filename = message.split()[1]
        filepath = filename[1:]
        if filepath == "":
            filepath = "c:/Users/chinm/SEM6/CN/expt16/index.html"
        print("Opening file:", filepath)
        with open(filepath, "rb") as f:
            outputdata = f.read()
        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html; charset=utf-8\r\n"
        response += b"Content-Length: " + str(len(outputdata)).encode() + b"\r\n"
        response += b"Connection: close\r\n"
        response += b"\r\n"
        connectionSocket.sendall(response)
        connectionSocket.sendall(outputdata)
        print("Response sent successfully")
    except FileNotFoundError:
        print("404 File Not Found")

        error_html = b"""
<html>
<head><title>404 Error</title></head>
<body>
<h1>404 Not Found</h1>
</body>
</html>
"""
        response = b"HTTP/1.1 404 Not Found\r\n"
        response += b"Content-Type: text/html\r\n"
        response += b"Content-Length: " + str(len(error_html)).encode() + b"\r\n"
        response += b"Connection: close\r\n"
        response += b"\r\n"
        connectionSocket.sendall(response)
        connectionSocket.sendall(error_html)
    except Exception as e:
        print("ERROR:", e)
    finally:
        connectionSocket.close()
        print("Connection closed")
