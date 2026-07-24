import socket
import random

HOST = "127.0.0.1"
PORT = 5100

LOSS_RATE = 0.2
ACK_LOSS_RATE = 0.2

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("RECEIVER STARTED\n")

conn, addr = server.accept()
print("Connected:", addr)

expected = 0

while True:

    data = conn.recv(1024)

    if not data:
        break

    frame = data.decode()
    print("Received:", frame)

    seq = int(frame.split(":")[1])

    # Simulate frame loss
    if random.random() < LOSS_RATE:
        print("Frame lost\n")
        continue

    if seq == expected:
        print("Accepted frame", seq)
        expected += 1
    else:
        print("Out-of-order frame discarded")

    ack = f"ACK:{expected-1}"

    # Simulate ACK loss
    if random.random() < ACK_LOSS_RATE:
        print("ACK lost\n")
        continue

    conn.send(ack.encode())
    print("Sent:", ack, "\n")

conn.close()
server.close()