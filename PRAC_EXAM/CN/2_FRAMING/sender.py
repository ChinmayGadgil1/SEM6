import socket
import struct


HOST = "127.0.0.1"
PORT = 9090
FLAG = "FLAG"
ESC = "ESC"
BIT_FLAG = "01111110"


def send_msg(sock, text):
    data = text.encode()
    sock.sendall(struct.pack("!I", len(data)) + data)


def char_count_encode(text, frame_size=5):
    if frame_size < 2:
        raise ValueError("frame_size must be at least 2")

    payload_size = frame_size - 1
    frames = []
    for i in range(0, len(text), payload_size):
        chunk = text[i:i + payload_size]
        frames.append(chr(len(chunk) + 1) + chunk)
    return frames


def byte_stuff(text):
    stuffed = text.replace(ESC, ESC + ESC)
    stuffed = stuffed.replace(FLAG, ESC + FLAG)
    return FLAG + stuffed + FLAG


def bit_stuff(bits):
    bits = bits.replace(" ", "")
    if set(bits) - {"0", "1"}:
        raise ValueError("bit data must contain only 0 and 1")

    stuffed = []
    ones = 0
    for bit in bits:
        stuffed.append(bit)
        if bit == "1":
            ones += 1
            if ones == 5:
                stuffed.append("0")
                ones = 0
        else:
            ones = 0
    return BIT_FLAG + "".join(stuffed) + BIT_FLAG


def menu():
    print("\n1. Character Count")
    print("2. Byte Stuffing")
    print("3. Bit Stuffing")
    print("4. Exit")
    return input("Choice: ")


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print(f"Connected to receiver at {HOST}:{PORT}")

    while True:
        choice = menu()

        try:
            if choice == "1":
                text = input("Text: ")
                size = int(input("Frame size (>=2): "))
                frames = char_count_encode(text, size)
                print("Frames:", " | ".join(frames))
                send_msg(sock, "CC|" + "".join(frames))

            elif choice == "2":
                text = input("Text: ")
                framed = byte_stuff(text)
                print("Framed:", framed)
                send_msg(sock, "BS|" + framed)

            elif choice == "3":
                bits = input("Bits: ")
                framed = bit_stuff(bits)
                print("Framed:", framed)
                send_msg(sock, "BT|" + framed)

            elif choice == "4":
                send_msg(sock, "QUIT")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print("Error:", e)

    sock.close()


if __name__ == "__main__":
    main()