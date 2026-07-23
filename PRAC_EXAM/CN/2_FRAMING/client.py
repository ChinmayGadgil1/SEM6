import socket

s = socket.socket()
s.connect(("localhost", 9091))

while True:
    print("\n1. Character Count")
    print("2. Byte Stuffing")
    print("3. Bit Stuffing")
    print("0. Exit")

    choice = input("Enter choice : ")

    if choice == "0":
        break

    if choice == "1":
        data = input("Enter data : ")
        frame_size = input("Enter frame size : ")
        msg = f"1|{data}|{frame_size}"

    elif choice == "2":
        data = input("Enter data : ")
        msg = f"2|{data}"

    elif choice == "3":
        data = input("Enter binary data : ")
        msg = f"3|{data}"

    else:
        continue

    s.send(msg.encode())

    print("Result :", s.recv(1024).decode())

s.close()