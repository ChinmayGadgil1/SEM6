import socket

# PARITY CHECK
def par_chk(bits, p):
    ones = bits.count('1')
    cp = str(ones % 2)
    return cp == p

# BLOCK PARITY CHECK
def block_chk(bits, r, c, rp, cp):
    g = [[int(bits[i*c+j]) for j in range(c)] for i in range(r)]
    crp = [sum(g[i])%2 for i in range(r)]
    ccp = [sum(g[i][j] for i in range(r))%2 for j in range(c)]
    rp = [int(x) for x in rp]
    cp = [int(x) for x in cp]
    return crp == rp and ccp == cp

# CRC VERIFY
def crc_chk(tx, gen):
    w = list(tx)
    for i in range(len(w)-len(gen)+1):
        if w[i] == '1':
            for j in range(len(gen)):
                w[i+j] = str(int(w[i+j]) ^ int(gen[j]))
    return all(x == '0' for x in w[-(len(gen)-1):])

# HAMMING DECODE
def ham_dec(enc):
    b = [int(x) for x in enc]
    s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    s4 = b[3] ^ b[4] ^ b[5] ^ b[6]
    ep = s1 + (s2<<1) + (s4<<2)
    if 0 < ep < 7:
        b[ep] ^= 1
    return str(b[2])+str(b[4])+str(b[5])+str(b[6]), ep > 0

def ham_decode(enc, ol):
    dec = ''
    for i in range(0, len(enc), 7):
        d, _ = ham_dec(enc[i:i+7])
        dec += d
    return dec[:ol]

# CHECKSUM VERIFY
def cs_chk(bits, recv_cs):
    b = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
    s = 0
    for i in range(0, len(b), 2):
        s += (b[i]<<8 if i+1 >= len(b) else (b[i]<<8)|b[i+1])
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    cs = (~s) & 0xFFFF
    return cs == int(recv_cs, 16)

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 9091))
    s.listen(1)
    c, a = s.accept()
    print(f"[Receiver] Connected from {a}")
    
    while True:
        m = c.recv(1024).decode()
        if m == "QUIT":
            break
        if not m:
            continue
        
        try:
            p = m.split('|')
            tag = p[0]
            
            if tag == "PR":
                _, b, pr = p[1], p[2], p[3]
                ok = par_chk(b, pr)
                print(f"PARITY: {b} P={pr} {'✓' if ok else '✗'}")
            
            elif tag == "BP":
                r, c, b, rp, cp = int(p[1]), int(p[2]), p[3], p[4], p[5]
                ok = block_chk(b, r, c, rp, cp)
                print(f"BLOCK({r}x{c}): {b} {'✓' if ok else '✗'}")
            
            elif tag == "CR":
                d, gen, rem, tx = p[1], p[2], p[3], p[4]
                ok = crc_chk(tx, gen)
                print(f"CRC: {d}|{gen} REM={rem} {'✓' if ok else '✗'}")
            
            elif tag == "HM":
                ol, enc = int(p[1]), p[2]
                dec = ham_decode(enc, ol)
                print(f"HAMMING: {enc} -> {dec}")
            
            elif tag == "CS":
                _, b, cs = p[1], p[2], p[3]
                ok = cs_chk(b, cs)
                print(f"CHECKSUM: {b} CS={cs} {'✓' if ok else '✗'}")
        
        except Exception as e:
            print(f"Error: {e}")
    
    c.close()
    s.close()

if __name__ == "__main__":
    main()
