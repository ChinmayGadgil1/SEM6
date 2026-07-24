import socket
import random
import time

HOST = "127.0.0.1"
PORT = 5000

LOSS_RATE = 0.2
CORRUPT_RATE = 0.2
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

    # Simulate corruption
    if random.random() < CORRUPT_RATE:
        nak = f"NAK:{seq}"
        conn.send(nak.encode())
        print("Frame corrupted")
        print("Sent:", nak, "\n")
        continue

    # Correct frame
    if seq == expected:

        print("Correct frame received")

        # Simulate delayed ACK
        if random.random() < 0.2:
            print("Delaying ACK...")
            time.sleep(3)

        ack = f"ACK:{seq}"

        # Simulate ACK loss
        if random.random() < ACK_LOSS_RATE:
            print("ACK lost\n")
            continue

        conn.send(ack.encode())
        print("Sent:", ack, "\n")

        expected = 1 - expected

    # Duplicate frame
    else:
        ack = f"ACK:{1 - expected}"
        conn.send(ack.encode())

        print("Duplicate frame")
        print("Re-sent:", ack, "\n")

conn.close()
server.close()