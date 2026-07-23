import math


def ip_to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) + (b << 16) + (c << 8) + d


def int_to_ip(num):
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"


network = input("Enter Base Network (Example: 192.168.10.0/24): ")
ip, prefix = network.split("/")
prefix = int(prefix)

n = int(input("Enter Number of Subnets: "))

subnets = []

for i in range(n):
    name = input("Enter Subnet Name: ")
    hosts = int(input(f"Enter Hosts Required for {name}: "))
    subnets.append((name, hosts))

# Allocate largest subnet first
subnets.sort(key=lambda x: x[1], reverse=True)

current_ip = ip_to_int(ip)

print("\nSubnet Details\n")

for name, hosts in subnets:

    total = hosts + 2
    host_bits = math.ceil(math.log2(total))
    prefix_len = 32 - host_bits

    block_size = 2 ** host_bits
    broadcast = current_ip + block_size - 1

    print(f"Subnet Name       : {name}")
    print(f"Network Address   : {int_to_ip(current_ip)}/{prefix_len}")
    print(f"Broadcast Address : {int_to_ip(broadcast)}")
    print(f"Host Range        : {int_to_ip(current_ip + 1)} - {int_to_ip(broadcast - 1)}")
    print(f"Usable Hosts      : {block_size - 2}")
    print()

    current_ip += block_size