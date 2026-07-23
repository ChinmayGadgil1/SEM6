import math


def ip_to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) + (b << 16) + (c << 8) + d


def int_to_ip(num):
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"


network = input("Enter Network Address (Example: 192.168.1.0/24): ")
ip, prefix = network.split("/")
prefix = int(prefix)

subnets = int(input("Enter Number of Subnets: "))

borrow_bits = math.ceil(math.log2(subnets))
new_prefix = prefix + borrow_bits

subnet_size = 2 ** (32 - new_prefix)
base_ip = ip_to_int(ip)

print("\nSubnet Details\n")

for i in range(subnets):
    subnet_ip = base_ip + i * subnet_size
    broadcast = subnet_ip + subnet_size - 1

    print(f"Subnet {i + 1}: {int_to_ip(subnet_ip)}/{new_prefix}")
    print(f"Broadcast Address : {int_to_ip(broadcast)}")
    print(f"Host Range        : {int_to_ip(subnet_ip + 1)} - {int_to_ip(broadcast - 1)}")
    print(f"Usable Hosts      : {subnet_size - 2}")
    print()