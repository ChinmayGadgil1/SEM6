import socket
import time


HOST = "127.0.0.1"
SENDER_PORT = 5000
RECEIVER_PORT = 5001


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SENDER_PORT))
    sock.settimeout(2)

    frames = ["Hello", "World", "Stop", "Wait", "ARQ"]
    seq = 0

    print("SENDER STARTED (STOP AND WAIT)\n")

    for payload in frames:
        while True:
            frame = f"FRAME:{seq}:{payload}"
            print("SENDER: Sending ->", frame)
            sock.sendto(frame.encode(), (HOST, RECEIVER_PORT))

            try:
                msg, _ = sock.recvfrom(1024)
            except socket.timeout:
                print("SENDER: Timeout, retransmitting\n")
                time.sleep(1)
                continue

            ack = msg.decode()
            print("SENDER: Received ->", ack)

            if ack == f"ACK:{seq}":
                print("SENDER: Correct ACK, moving to next frame\n")
                seq = 1 - seq
                break

            if ack.startswith("NAK"):
                print("SENDER: NAK received, retransmitting\n")
            else:
                print("SENDER: Wrong ACK, retransmitting\n")

    print("ALL FRAMES SENT SUCCESSFULLY")
    sock.close()


if __name__ == "__main__":
    main()