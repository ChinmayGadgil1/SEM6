import socket
import struct


PORT = 9090
FLAG = "FLAG"
ESC = "ESC"
BIT_FLAG = "01111110"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def recv_msg(sock):
    header = recv_exact(sock, 4)
    if not header:
        return None
    size = struct.unpack("!I", header)[0]
    payload = recv_exact(sock, size)
    if payload is None:
        return None
    return payload.decode()


def char_count_decode(raw):
    result = []
    i = 0
    while i < len(raw):
        count = ord(raw[i])
        if count < 1 or i + count > len(raw):
            raise ValueError("bad character count frame")
        result.append(raw[i + 1:i + count])
        i += count
    return "".join(result)


def byte_unstuff(framed):
    if not framed.startswith(FLAG) or not framed.endswith(FLAG):
        raise ValueError("missing FLAG delimiters")

    inner = framed[len(FLAG):-len(FLAG)]
    result = []
    i = 0
    while i < len(inner):
        if inner.startswith(ESC, i):
            i += len(ESC)
            if inner.startswith(ESC, i):
                result.append(ESC)
                i += len(ESC)
            elif inner.startswith(FLAG, i):
                result.append(FLAG)
                i += len(FLAG)
            else:
                raise ValueError("bad ESC sequence")
        else:
            result.append(inner[i])
            i += 1
    return "".join(result)


def bit_unstuff(framed):
    if not framed.startswith(BIT_FLAG) or not framed.endswith(BIT_FLAG):
        raise ValueError("missing bit flags")

    inner = framed[len(BIT_FLAG):-len(BIT_FLAG)]
    result = []
    ones = 0
    i = 0
    while i < len(inner):
        bit = inner[i]
        result.append(bit)
        if bit == "1":
            ones += 1
            if ones == 5:
                i += 1
                if i < len(inner) and inner[i] != "0":
                    raise ValueError("expected stuffed 0")
                ones = 0
        else:
            ones = 0
        i += 1
    return "".join(result)


def show_cc_frames(raw):
    i = 0
    idx = 1
    while i < len(raw):
        count = ord(raw[i])
        frame = raw[i:i + count]
        print(f"Frame {idx}: [{count}]" + "".join(f"[{ch}]" for ch in frame[1:]))
        i += count
        idx += 1


def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", PORT))
    server.listen(1)
    print(f"Receiver listening on port {PORT}")

    conn, addr = server.accept()
    print("Sender connected from", addr[0])

    while True:
        msg = recv_msg(conn)
        if not msg or msg == "QUIT":
            break

        if len(msg) < 3 or msg[2] != "|":
            print("Bad message format")
            continue

        tag, payload = msg[:2], msg[3:]
        print("\n" + "=" * 40)

        try:
            if tag == "CC":
                print("Character Count")
                show_cc_frames(payload)
                print("Decoded:", char_count_decode(payload))
            elif tag == "BS":
                print("Byte Stuffing")
                print("Framed :", payload)
                print("Decoded:", byte_unstuff(payload))
            elif tag == "BT":
                print("Bit Stuffing")
                print("Framed :", payload)
                print("Decoded:", bit_unstuff(payload))
            else:
                print("Unknown type")
        except Exception as e:
            print("Error:", e)

    conn.close()
    server.close()


if __name__ == "__main__":
    main()