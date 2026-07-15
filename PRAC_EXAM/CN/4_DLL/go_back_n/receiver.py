import random
import socket


HOST = "127.0.0.1"
RECEIVER_PORT = 5101
LOSS_RATE = 0.2
ACK_LOSS_RATE = 0.2


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, RECEIVER_PORT))
    expected = 0

    print("RECEIVER STARTED (GO-BACK-N)\n")

    while True:
        data, sender_addr = sock.recvfrom(1024)
        frame = data.decode()
        print("RECEIVER: Frame arrived ->", frame)
        seq = int(frame.split(":")[1])

        if random.random() < LOSS_RATE:
            print("RECEIVER: Frame lost\n")
            continue

        if seq == expected:
            print("RECEIVER: Accepted frame", seq)
            expected += 1
            ack_num = expected - 1
        else:
            print("RECEIVER: Out-of-order frame discarded")
            ack_num = expected - 1

        ack = f"ACK:{ack_num}"
        if random.random() < ACK_LOSS_RATE:
            print("RECEIVER: ACK lost\n")
            continue

        sock.sendto(ack.encode(), sender_addr)
        print("RECEIVER: Sent cumulative ACK ->", ack, "\n")


if __name__ == "__main__":
    main()