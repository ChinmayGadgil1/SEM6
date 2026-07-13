import socket
import threading
HOST = '127.0.0.1'
PORT = 8888
BUFFER_SIZE = 4096
def handle_client(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)

        if not request:
            client_socket.close()
            return

        print("\n========== REQUEST RECEIVED ==========")
        print(request.decode(errors='ignore'))
        request_text = request.decode(errors='ignore')
        first_line = request_text.split('\n')[0]
        parts = first_line.split()

        if len(parts) < 2:
            client_socket.close()
            return
        url = parts[1]
        host = ""
        if "://" in url:
            host = url.split("://")[1].split('/')[0]
        else:
            # Use Host header
            for line in request_text.split('\n'):
                if line.lower().startswith("host:"):
                    host = line.split(":")[1].strip()
                    break

        print(f"\n[CONNECTING TO HOST]: {host}")
        if ":" in host:
            host = host.split(":")[0]
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, 80))
        modified_request = request.replace(
            b'Proxy-Connection:',
            b'Connection:'
        )
        server_socket.sendall(modified_request)

        print("[REQUEST FORWARDED TO ORIGINAL SERVER]")
        while True:
            data = server_socket.recv(BUFFER_SIZE)
            if len(data) > 0:
                client_socket.send(data)
            else:
                break
        print("[RESPONSE SENT TO CLIENT]")
        server_socket.close()
    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        client_socket.close()
def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    proxy_socket.bind((HOST, PORT))
    proxy_socket.listen(10)

    print(f"\n[PROXY SERVER RUNNING ON {HOST}:{PORT}]")

    while True:
        client_socket, client_address = proxy_socket.accept()
        print(f"\n[NEW CONNECTION] {client_address}")
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket,)
        )

        client_thread.start()
start_proxy()
