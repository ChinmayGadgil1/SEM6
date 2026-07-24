import socket

s=socket.socket()
s.connect(("localhost",8888))

while True:
    print("\n1-Parity")
    print("2-Block Parity")
    print("3-CRC")
    print("4-Hamming")
    print("5-Checksum")
    print("0-Exit")
    
    choice=int(input())
    
    if choice==1:
        data=input("Enter bits:")
        msg=f"{choice}|{data}"
    if choice==2:
        row=int(input("enter num rows:"))
        col=int(input("enter num col:"))
        data=input("Enter bits:")
        msg=f"{choice}|{row}|{col}|{data}"
    if choice==3:
        data=input("Enter bits:")
        gen=input("enter generator:")
        msg=f"{choice}|{data}|{gen}"
    if choice==4:
        data=input("Enter bits:")
        msg=f"{choice}|{data}"
    if choice==5:
        data=input("Enter bits:")
        msg=f"{choice}|{data}"
    if choice==0:
        msg="QUIT"
    
    
    s.sendall(msg.encode())
    
    resp=s.recv(1024).decode()
    
    print(resp)
    
    