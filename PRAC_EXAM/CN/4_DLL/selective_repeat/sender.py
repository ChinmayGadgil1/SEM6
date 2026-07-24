import socket

HOST = "127.0.0.1"
PORT = 5200

sock = socket.socket()
sock.connect((HOST, PORT))
sock.settimeout(2)

frames = ["A", "B", "C", "D", "E", "F", "G", "H"]
window_size = 4

base = 0
next_seq = 0
acked = [False] * len(frames)

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
        acked[ack] = True

        # Slide the window
        while base < len(frames) and acked[base]:
            base += 1

    except socket.timeout:
        print("Timeout! Retransmitting unACKed frames...")

        for i in range(base, next_seq):
            if not acked[i]:
                frame = f"FRAME:{i}:{frames[i]}"
                print("Retransmitting:", frame)
                sock.send(frame.encode())

print("\nAll frames sent successfully.")
sock.close()