import random
import socket
import time


HOST = "127.0.0.1"
RECEIVER_PORT = 5001
LOSS_RATE = 0.2
CORRUPT_RATE = 0.2
ACK_LOSS_RATE = 0.2


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, RECEIVER_PORT))
    expected = 0

    print("RECEIVER STARTED (STOP AND WAIT)\n")

    while True:
        data, sender_addr = sock.recvfrom(1024)
        frame = data.decode()
        print("RECEIVER: Frame arrived ->", frame)

        seq = int(frame.split(":")[1])

        if random.random() < LOSS_RATE:
            print("RECEIVER: Frame lost\n")
            continue

        if random.random() < CORRUPT_RATE:
            nak = f"NAK:{seq}"
            print("RECEIVER: Frame corrupted")
            sock.sendto(nak.encode(), sender_addr)
            print("RECEIVER: NAK sent ->", nak, "\n")
            continue

        if seq == expected:
            print("RECEIVER: Correct frame received")

            if random.random() < 0.2:
                print("RECEIVER: Delaying ACK...")
                time.sleep(3)

            ack = f"ACK:{seq}"
            if random.random() < ACK_LOSS_RATE:
                print("RECEIVER: ACK lost\n")
                continue

            sock.sendto(ack.encode(), sender_addr)
            print("RECEIVER: ACK sent ->", ack, "\n")
            expected = 1 - expected
        else:
            ack = f"ACK:{1 - expected}"
            print("RECEIVER: Duplicate frame")
            sock.sendto(ack.encode(), sender_addr)
            print("RECEIVER: Re-sent ACK ->", ack, "\n")


if __name__ == "__main__":
    main()