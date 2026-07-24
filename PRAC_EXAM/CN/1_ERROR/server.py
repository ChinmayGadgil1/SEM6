import socket


# PARITY
def parity(bits):
    ones = bits.count('1')
    return str(ones % 2)


# BLOCK PARITY
def block_par(bits, r, c):
    g = [[int(bits[i*c+j]) for j in range(c)] for i in range(r)]

    row_parity = [sum(row) % 2 for row in g]
    col_parity = [sum(g[i][j] for i in range(r)) % 2 for j in range(c)]

    return row_parity, col_parity


# CRC
def crc(data, gen):
    data += '0' * (len(gen) - 1)
    data = list(data)

    for i in range(len(data) - len(gen) + 1):
        if data[i] == '1':
            for j in range(len(gen)):
                if data[i + j] == gen[j]:
                    data[i + j] = '0'
                else:
                    data[i + j] = '1'

    return ''.join(data[-(len(gen) - 1):])


# HAMMING
def ham(d1, d2, d3, d4):
    p1 = int(d1) ^ int(d2) ^ int(d4)
    p2 = int(d1) ^ int(d3) ^ int(d4)
    p4 = int(d2) ^ int(d3) ^ int(d4)

    return str(p1) + str(p2) + d1 + str(p4) + d2 + d3 + d4


def hamming(bits):
    pad = bits + '0' * ((4 - len(bits) % 4) % 4)

    encoded = ""

    for i in range(0, len(pad), 4):
        encoded += ham(pad[i], pad[i+1], pad[i+2], pad[i+3])

    return encoded


# CHECKSUM
def checksum(bits):
    if len(bits) % 16:
        bits += '0' * (16 - len(bits) % 16)

    total = 0

    for i in range(0, len(bits), 16):
        total += int(bits[i:i+16], 2)

    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)

    return format(~total & 0xFFFF, "04x")

# SERVER
server = socket.socket()
server.bind(("localhost", 9091))
server.listen(1)

print("Waiting for client...")

conn, addr = server.accept()
print("Connected :", addr)


while True:

    data = conn.recv(1024).decode()

    if data == "QUIT":
        break

    parts = data.split("|")
    choice = parts[0]

    if choice == "1":
        bits = parts[1]
        result = parity(bits)

    elif choice == "2":
        r = int(parts[1])
        c = int(parts[2])
        bits = parts[3]

        rp, cp = block_par(bits, r, c)
        result = f"Row Parity = {rp}, Column Parity = {cp}"

    elif choice == "3":
        bits = parts[1]
        gen = parts[2]

        rem = crc(bits, gen)
        result = f"CRC Remainder = {rem}"

    elif choice == "4":
        bits = parts[1]

        enc = hamming(bits)
        result = f"Hamming Code = {enc}"

    elif choice == "5":
        bits = parts[1]

        cs = checksum(bits)
        result = f"Checksum = {cs}"

    else:
        result = "Invalid Choice"

    conn.sendall(result.encode())
conn.close()
server.close()