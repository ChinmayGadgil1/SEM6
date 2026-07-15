import random
import socket


HOST = "127.0.0.1"
RECEIVER_PORT = 5201
LOSS_RATE = 0.2
ACK_LOSS_RATE = 0.2


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, RECEIVER_PORT))

    base = 0
    window_size = 4
    received = {}

    print("RECEIVER STARTED (SELECTIVE REPEAT)\n")

    while True:
        data, sender_addr = sock.recvfrom(1024)
        frame_str = data.decode()
        print("RECEIVER: Frame arrived ->", frame_str)
        seq = int(frame_str.split(":")[1])

        if random.random() < LOSS_RATE:
            print("RECEIVER: Frame lost\n")
            continue

        if seq >= base and seq < base + window_size:
            if not received.get(seq, False):
                print(f"RECEIVER: Frame {seq} accepted and buffered")
                received[seq] = True
            else:
                print(f"RECEIVER: Duplicate frame {seq}")

            ack = f"ACK:{seq}"
            if random.random() < ACK_LOSS_RATE:
                print("RECEIVER: ACK lost\n")
                continue

            sock.sendto(ack.encode(), sender_addr)
            print("RECEIVER: ACK sent ->", ack)

            while received.get(base, False):
                print("RECEIVER: Delivering frame", base)
                base += 1

        elif seq < base:
            print("RECEIVER: Old frame received again")
            ack = f"ACK:{seq}"
            sock.sendto(ack.encode(), sender_addr)
            print("RECEIVER: Re-sent ACK ->", ack)

        else:
            print("RECEIVER: Frame outside window ignored")

        print()


if __name__ == "__main__":
    main()