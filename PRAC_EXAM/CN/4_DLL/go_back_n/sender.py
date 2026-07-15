import socket


HOST = "127.0.0.1"
SENDER_PORT = 5100
RECEIVER_PORT = 5101


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SENDER_PORT))
    sock.settimeout(2)

    frames = ["A", "B", "C", "D", "E", "F", "G", "H"]
    base = 0
    next_seq = 0
    window_size = 4

    print("SENDER STARTED (GO-BACK-N)\n")

    while base < len(frames):
        while next_seq < base + window_size and next_seq < len(frames):
            frame = f"FRAME:{next_seq}:{frames[next_seq]}"
            print("SENDER: Sending ->", frame)
            sock.sendto(frame.encode(), (HOST, RECEIVER_PORT))
            next_seq += 1

        try:
            msg, _ = sock.recvfrom(1024)
        except socket.timeout:
            print("SENDER: Timeout, retransmitting window")
            for i in range(base, next_seq):
                frame = f"FRAME:{i}:{frames[i]}"
                print("SENDER: Retransmitting ->", frame)
                sock.sendto(frame.encode(), (HOST, RECEIVER_PORT))
            print()
            continue

        ack = int(msg.decode().split(":")[1])
        print("SENDER: Received ->", msg.decode())

        if ack >= base:
            base = ack + 1
            print("SENDER: Sliding window, new base =", base, "\n")

    print("ALL FRAMES SENT SUCCESSFULLY")
    sock.close()


if __name__ == "__main__":
    main()