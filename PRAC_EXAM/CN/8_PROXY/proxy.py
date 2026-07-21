import socket
import threading

HOST = '127.0.0.1'
PORT = 8888
BUFFER = 4096

def handle_client(client_socket):
    try:
        # Receive request from client
        request = client_socket.recv(BUFFER)
        if not request:
            client_socket.close()
            return
        
        print("Request received")
        
        # Parse request to get host
        request_text = request.decode(errors='ignore')
        first_line = request_text.split('\n')[0]
        parts = first_line.split()
        
        if len(parts) < 2:
            client_socket.close()
            return
        
        url = parts[1]
        host = url.split("://")[1].split('/')[0] if "://" in url else None
        
        # If no host in URL, get from Host header
        if not host:
            for line in request_text.split('\n'):
                if line.lower().startswith("host:"):
                    host = line.split(":")[1].strip()
                    break
        
        if not host:
            client_socket.close()
            return
        
        # Remove port from host if present
        host = host.split(":")[0]
        
        print(f"Connecting to: {host}")
        
        # Connect to server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, 80))
        
        # Forward request
        modified_request = request.replace(b'Proxy-Connection:', b'Connection:')
        server_socket.sendall(modified_request)
        
        # Forward response back to client
        server_socket.settimeout(2)
        try:
            while True:
                data = server_socket.recv(BUFFER)
                if data:
                    client_socket.sendall(data)
                else:
                    break
        except socket.timeout:
            pass
        
        print("Response sent")
        server_socket.close()
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind((HOST, PORT))
    proxy_socket.listen(10)
    
    print(f"Proxy running on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Client connected: {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    start_proxy()
