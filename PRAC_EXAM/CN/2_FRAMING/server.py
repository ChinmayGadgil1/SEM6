import socket

FLAG = "FLAG"
ESC = "ESC"


# Character Count
def char_count_encode(text, frame_size=5):
    payload_size = frame_size - 1
    frames = []

    for i in range(0, len(text), payload_size):
        chunk = text[i:i + payload_size]
        count = len(chunk) + 1
        frames.append(str(count) + chunk)

    return "".join(frames)


# Byte Stuffing
def byte_stuffing(data):
    out = FLAG
    i = 0

    while i < len(data):
        if data.startswith(FLAG, i):
            out += ESC + FLAG
            i += len(FLAG)

        elif data.startswith(ESC, i):
            out += ESC + ESC
            i += len(ESC)

        else:
            out += data[i]
            i += 1

    out += FLAG
    return out


# Bit Stuffing
def bit_stuffing(data):
    stuffed = ""
    count = 0

    for bit in data:
        stuffed += bit

        if bit == "1":
            count += 1

            if count == 5:
                stuffed += "0"
                count = 0
        else:
            count = 0

    return stuffed


# SERVER CODE
server = socket.socket()
server.bind(("localhost", 9091))
server.listen(1)

print("Waiting for client...")

conn, addr = server.accept()
print("Client Connected")

while True:

    msg = conn.recv(1024).decode()

    if not msg:
        break

    parts = msg.split("|")
    choice = parts[0]

    if choice == "1":
        data = parts[1]
        frame_size = int(parts[2])

        result = char_count_encode(data, frame_size)

    elif choice == "2":
        data = parts[1]

        result = byte_stuffing(data)

    elif choice == "3":
        data = parts[1]

        result = bit_stuffing(data)

    else:
        result = "Invalid Choice"

    conn.send(result.encode())

conn.close()
server.close()