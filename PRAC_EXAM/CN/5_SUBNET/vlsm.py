import math
import ipaddress

network = ipaddress.ip_network(
    input("Enter Base Network (e.g. 192.168.10.0/24): "),
    strict=False
)

n = int(input("Enter Number of Subnets: "))

requirements = []

for i in range(n):
    name = input("Enter Subnet Name: ")
    hosts = int(input(f"Enter Required Hosts for {name}: "))
    requirements.append((name, hosts))

requirements.sort(key=lambda x: x[1], reverse=True)

current_ip = network.network_address

print("\nVLSM Subnet Details\n")

for name, hosts in requirements:

    total_addresses = hosts + 2
    host_bits = math.ceil(math.log2(total_addresses))
    prefix = 32 - host_bits

    subnet = ipaddress.ip_network(
        f"{current_ip}/{prefix}",
        strict=False
    )

    print(f"Subnet Name       : {name}")
    print(f"Network Address   : {subnet}")
    print(f"Broadcast Address : {subnet.broadcast_address}")
    print(f"Host Range        : {list(subnet.hosts())[0]} - {list(subnet.hosts())[-1]}")
    print(f"Usable Hosts      : {subnet.num_addresses - 2}")
    print()

    current_ip = subnet.broadcast_address + 1