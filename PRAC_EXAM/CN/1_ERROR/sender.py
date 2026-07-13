import socket

# PARITY
def parity(bits):
    ones = bits.count('1')
    p = str(ones % 2)
    return bits, p

# BLOCK PARITY
def block_par(bits, r, c):
    g = [[int(bits[i*c+j]) for j in range(c)] for i in range(r)]
    rp = [sum(g[i])%2 for i in range(r)]
    cp = [sum(g[i][j] for i in range(r))%2 for j in range(c)]
    return g, rp, cp

# CRC
def crc(data, gen):
    w = list(data + '0'*(len(gen)-1))
    for i in range(len(w)-len(gen)+1):
        if w[i] == '1':
            for j in range(len(gen)):
                w[i+j] = str(int(w[i+j]) ^ int(gen[j]))
    return ''.join(w[-(len(gen)-1):])

# HAMMING (7,4)
def ham(d1, d2, d3, d4):
    p1 = int(d1) ^ int(d2) ^ int(d4)
    p2 = int(d1) ^ int(d3) ^ int(d4)
    p4 = int(d2) ^ int(d3) ^ int(d4)
    return str(p1) + str(p2) + d1 + str(p4) + d2 + d3 + d4

def hamming(bits):
    pad = bits + '0'*((4-len(bits)%4)%4)
    enc = ''.join(ham(pad[i], pad[i+1], pad[i+2], pad[i+3]) for i in range(0, len(pad), 4))
    return enc, len(bits)

# CHECKSUM
def chksum(bits):
    b = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
    s = 0
    for i in range(0, len(b), 2):
        s += (b[i]<<8 if i+1 >= len(b) else (b[i]<<8)|b[i+1])
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF

def main():
    s = socket.socket()
    s.connect(("localhost", 9091))
    print("[Sender] Connected")
    
    while True:
        print("\n1-Parity 2-Block 3-CRC 4-Hamming 5-Checksum 0-Exit")
        c = input("Choice: ")
        if c == "0":
            s.sendall(b"QUIT")
            break
        
        try:
            if c == "1":
                d = input("Bits: ")
                b, p = parity(d)
                s.sendall(f"PR|{len(b)}|{b}|{p}".encode())
                print(f"Sent: P={p}")
            
            elif c == "2":
                r, c = int(input("Rows: ")), int(input("Cols: "))
                d = input(f"({r*c} bits): ")
                g, rp, cp = block_par(d, r, c)
                s.sendall(f"BP|{r}|{c}|{d}|{''.join(map(str,rp))}|{''.join(map(str,cp))}".encode())
                print(f"Sent: RP={rp} CP={cp}")
            
            elif c == "3":
                d = input("Data: ")
                gen = input("Gen: ")
                rem = crc(d, gen)
                s.sendall(f"CR|{d}|{gen}|{rem}|{d+rem}".encode())
                print(f"Sent: Rem={rem}")
            
            elif c == "4":
                d = input("Bits: ")
                enc, ol = hamming(d)
                s.sendall(f"HM|{ol}|{enc}".encode())
                print(f"Sent: {d}->{enc}")
            
            elif c == "5":
                d = input("Bits: ")
                cs = chksum(d)
                s.sendall(f"CS|{len(d)}|{d}|{cs:04x}".encode())
                print(f"Sent: CS={cs:04x}")
        except Exception as e:
            print(f"Error: {e}")
    
    s.close()

if __name__ == "__main__":
    main()
