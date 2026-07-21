
FLAG = "FLAG"
ESC = "ESC"


def char_count_encode(text: str, frame_size: int = 5) -> str:
    if frame_size < 2:
        raise ValueError("frame_size must be at least 2")

    payload_size = frame_size - 1
    frames = []

    for i in range(0, len(text), payload_size):
        chunk = text[i:i + payload_size]

        # Actual frame length = count digit + chunk length
        count = len(chunk) + 1

        frames.append(str(count) + chunk)

    return "".join(frames)
def char_count_decode(raw: str) -> str:
    result = []
    i = 0

    while i < len(raw):
        if not raw[i].isdigit():
            raise ValueError("Bad frame header")

        count = int(raw[i])

        if count < 2:
            raise ValueError("Invalid count")

        if i + count > len(raw):
            raise ValueError("Incomplete frame")

        result.append(raw[i + 1:i + count])

        i += count

    return "".join(result)

def byte_stuffing(data: str) -> str:
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


def byte_unstuffing(data: str) -> str:
    if data.startswith(FLAG):
        data = data[len(FLAG):]
    if data.endswith(FLAG):
        data = data[:-len(FLAG)]

    result = []
    i = 0
    while i < len(data):
        if data.startswith(ESC, i):
            i += len(ESC)
            if i >= len(data):
                raise ValueError("bad ESC sequence")
            if data.startswith(FLAG, i):
                result.append(FLAG)
                i += len(FLAG)
            elif data.startswith(ESC, i):
                result.append(ESC)
                i += len(ESC)
            else:
                result.append(data[i])
                i += 1
        else:
            result.append(data[i])
            i += 1
    return "".join(result)


def bit_stuffing(data: str) -> str:
    if any(bit not in "01" for bit in data):
        raise ValueError("bit data must contain only 0 and 1")

    stuffed = []
    count_ones = 0
    for bit in data:
        stuffed.append(bit)
        if bit == "1":
            count_ones += 1
            if count_ones == 5:
                stuffed.append("0")
                count_ones = 0
        else:
            count_ones = 0
    return "".join(stuffed)


def bit_unstuffing(data: str) -> str:
    if any(bit not in "01" for bit in data):
        raise ValueError("bit data must contain only 0 and 1")

    result = []
    count_ones = 0
    i = 0
    while i < len(data):
        bit = data[i]
        result.append(bit)
        if bit == "1":
            count_ones += 1
            if count_ones == 5:
                if i + 1 < len(data) and data[i + 1] == "0":
                    i += 1
                else:
                    raise ValueError("expected stuffed 0")
                count_ones = 0
        else:
            count_ones = 0
        i += 1
    return "".join(result)


def transmitter():
    print("Choose framing method:")
    print("1. Character Count")
    print("2. Byte Stuffing")
    print("3. Bit Stuffing")
    method = input("Enter method: ").strip()

    if method == "1":
        data = input("Enter data: ").strip()
        frame_size = int(input("Enter frame size: "))
        frames = char_count_encode(data, frame_size)
        print("Transmitted Frames:")
        print(frames)
    elif method == "2":
        data = input("Enter data: ").strip()
        print("Transmitted Data:")
        print(byte_stuffing(data))
    elif method == "3":
        data = input("Enter binary data: ").strip()
        print("Transmitted Data:")
        print(bit_stuffing(data))
    else:
        print("Invalid method")


def receiver():
    print("Choose framing method:")
    print("1. Character Count")
    print("2. Byte Stuffing")
    print("3. Bit Stuffing")
    method = input("Enter method: ").strip()

    if method == "1":
        frames = input("Enter transmitted frames: ").strip()
        print("Received Data:")
        print(char_count_decode(frames))
    elif method == "2":
        data = input("Enter received data: ").strip()
        print("Received Data:")
        print(byte_unstuffing(data))
    elif method == "3":
        data = input("Enter received data: ").strip()
        print("Received Data:")
        print(bit_unstuffing(data))
    else:
        print("Invalid method")


def main():
    while True:
        print("Menu:")
        print("1. Transmitter")
        print("2. Receiver")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            transmitter()
        elif choice == "2":
            receiver()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

