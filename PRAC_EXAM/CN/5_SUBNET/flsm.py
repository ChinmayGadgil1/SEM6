import math
import ipaddress

network = ipaddress.ip_network(
    input("Enter Network Address (e.g. 192.168.1.0/24): "),
    strict=False
)

num_subnets = int(input("Enter Number of Subnets: "))

borrow_bits = math.ceil(math.log2(num_subnets))
new_prefix = network.prefixlen + borrow_bits

subnets = list(network.subnets(new_prefix=new_prefix))

print("\nFLSM Subnet Details\n")

for i in range(num_subnets):
    subnet = subnets[i]

    print(f"Subnet {i+1}: {subnet}")
    print(f"Broadcast Address : {subnet.broadcast_address}")
    print(f"Host Range        : {list(subnet.hosts())[0]} - {list(subnet.hosts())[-1]}")
    print(f"Usable Hosts      : {subnet.num_addresses - 2}")
    print()