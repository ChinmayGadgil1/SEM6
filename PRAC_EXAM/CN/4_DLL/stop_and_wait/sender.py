import socket

HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket()
sock.connect((HOST, PORT))
sock.settimeout(2)

frames = ["Hello", "World", "Stop", "Wait", "ARQ"]
seq = 0

print("SENDER STARTED\n")

for payload in frames:

    while True:

        frame = f"FRAME:{seq}:{payload}"
        print("Sending:", frame)
        sock.send(frame.encode())

        try:
            ack = sock.recv(1024).decode()
            print("Received:", ack)

        except socket.timeout:
            print("Timeout! Retransmitting...\n")
            continue

        if ack == f"ACK:{seq}":
            print("Correct ACK\n")
            seq = 1 - seq
            break

        elif ack.startswith("NAK"):
            print("NAK received. Retransmitting...\n")

        else:
            print("Wrong ACK. Retransmitting...\n")


print("All frames sent successfully.")
sock.close()