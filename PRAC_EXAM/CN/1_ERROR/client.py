import socket

s = socket.socket()
s.connect(("localhost", 9091))

print("Connected to Server")

while True:
    print("\n1-Parity")
    print("2-Block Parity")
    print("3-CRC")
    print("4-Hamming")
    print("5-Checksum")
    print("0-Exit")

    choice = input("Choice : ")

    if choice == "0":
        s.sendall(b"QUIT")
        break

    if choice == "1":
        bits = input("Enter bits : ")
        msg = f"1|{bits}"

    elif choice == "2":
        r = input("Rows : ")
        c = input("Cols : ")
        bits = input("Enter bits : ")
        msg = f"2|{r}|{c}|{bits}"

    elif choice == "3":
        data = input("Enter data : ")
        gen = input("Enter generator : ")
        msg = f"3|{data}|{gen}"

    elif choice == "4":
        bits = input("Enter bits : ")
        msg = f"4|{bits}"

    elif choice == "5":
        bits = input("Enter bits : ")
        msg = f"5|{bits}"

    else:
        continue

    s.sendall(msg.encode())

    result = s.recv(1024).decode()
    print("Server Response :", result)

s.close()