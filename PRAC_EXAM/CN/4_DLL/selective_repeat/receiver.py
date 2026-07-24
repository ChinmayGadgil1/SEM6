import socket
import random

HOST = "127.0.0.1"
PORT = 5200

LOSS_RATE = 0.2
ACK_LOSS_RATE = 0.2
WINDOW_SIZE = 4

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("RECEIVER STARTED\n")

conn, addr = server.accept()
print("Connected:", addr)

base = 0
received = {}

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

    # Frame within the receiver's window
    if base <= seq < base + WINDOW_SIZE:

        if not received.get(seq, False):
            print("Buffered frame", seq)
            received[seq] = True

        ack = f"ACK:{seq}"

        # Simulate ACK loss
        if random.random() < ACK_LOSS_RATE:
            print("ACK lost\n")
            continue

        conn.send(ack.encode())
        print("Sent:", ack)

        # Deliver all consecutive frames
        while received.get(base, False):
            print("Delivered frame", base)
            base += 1

    # Duplicate frame
    elif seq < base:
        ack = f"ACK:{seq}"
        conn.send(ack.encode())
        print("Re-sent:", ack)

    print()

conn.close()
server.close()