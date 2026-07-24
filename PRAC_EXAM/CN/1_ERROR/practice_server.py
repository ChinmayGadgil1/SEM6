import socket

def parity(bits):
    ones=bits.count('1')
    return str(ones%2)

def block_parity(r,c,data):
    g=[[int(data[i*c+j]) for j in range(c) ] for i in range(r)]
    
    row_par=[sum(row)%2 for row in g]
    col_par=[sum(g[i][j] for i in range(r))%2 for j in range(c)]
    return row_par,col_par

def ham(d1,d2,d3,d4):
    p1=int(d1)^int(d2)^int(d4)
    p2=int(d1)^int(d3)^int(d4)
    p3=int(d2)^int(d3)^int(d4)
    
    return str(p1)+str(p2)+d1+str(p3)+d2+d3+d4

def hamming(data):
    bits=data+'0'*(4-len(data)%4)%4
    result=""
    for i in range(0,len(bits),4):
        result+=ham(bits[i],bits[i+1],bits[i+2],bits[i+3])
    
    return result

def checksum(data):
    if len(data)%16:
        data+='0'*(16-len(data)%16)
    
    total=0
    
    for i in range(0,len(data),16):
        total+=int(data[i:i+16],2)
    
    while total>0xFFFF:
        total=(total & 0xFFFF) + (total>>16)
    
    return format(~total & 0xFFFF,"04x")

def crc(data,gen):
    data+='0'*(len(gen)-1)
    data=list(data)
    
    for i in range(len(data)-len(gen)+1):
        if data[i]=='1':
            for j in range(len(gen)):
                if data[i+j]==gen[j]:
                    data[i+j]='0'
                else:
                    data[i+j]='1'
    
    return ''.join(data[-(len(gen)-1):])
    
server=socket.socket()
server.bind(("localhost",8888))
server.listen(1)

conn,addr=server.accept()

while True:
    
    data=conn.recv(1024).decode()
    part=data.split('|')
    
    if data == "QUIT":
        break
    if part[0]=='1':
        result=parity(part[1])
        
    elif part[0]=='2':
        result=block_parity(part[1],part[2],part[3])
    
    elif part[0]=='3':
        result=hamming(part[1])
    elif part[0]=='4':
        result=checksum(part[1])
    
    elif part[0]=='5':
        result=crc(part[1],part[2])
    conn.sendall(result.encode())
    

conn.close()
server.close()
            
    