import socket

HOST = "127.0.0.1"
PORT = 5100

sock = socket.socket()
sock.connect((HOST, PORT))
sock.settimeout(2)

frames = ["A", "B", "C", "D", "E", "F", "G", "H"]

base = 0
next_seq = 0
window_size = 4

print("SENDER STARTED\n")

while base < len(frames):

    # Send frames in the current window
    while next_seq < base + window_size and next_seq < len(frames):
        frame = f"FRAME:{next_seq}:{frames[next_seq]}"
        print("Sending:", frame)
        sock.send(frame.encode())
        next_seq += 1

    try:
        msg = sock.recv(1024).decode()
        ack = int(msg.split(":")[1])

        print("Received:", msg)

        if ack >= base:
            base = ack + 1

    except socket.timeout:
        print("Timeout! Retransmitting window...")

        for i in range(base, next_seq):
            frame = f"FRAME:{i}:{frames[i]}"
            print("Retransmitting:", frame)
            sock.send(frame.encode())

print("\nAll frames sent successfully.")
sock.close()