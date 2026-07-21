
import math
def ip_to_int(ip: str) -> int:
    parts = list(map(int, ip.split('.')))
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]


def int_to_ip(x: int) -> str:
    return f"{(x >> 24) & 0xFF}.{(x >> 16) & 0xFF}.{(x >> 8) & 0xFF}.{x & 0xFF}"


def get_mask(prefix: int) -> int:
    if prefix == 0:
        return 0
    return (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF


def flsm():
    print("===== FLSM Subnetting =====")
    network_input = input("Enter Network Address (EX: 192.168.1.0/24): ").strip()
    network_addr, prefix_str = network_input.split('/', 1)
    prefix = int(prefix_str)

    num_subnets = int(input("Enter Number of Required Subnets: "))
    if num_subnets <= 0:
        print("Number of subnets must be > 0")
        return

    borrowed_bits = math.ceil(math.log2(num_subnets)) if num_subnets > 1 else 0
    new_prefix = prefix + borrowed_bits

    base_ip = ip_to_int(network_addr)
    subnet_size = 1 << (32 - new_prefix)

    print("\nFLSM Subnet Details")
    for i in range(num_subnets):
        subnet_ip = (base_ip + (i * subnet_size)) & 0xFFFFFFFF
        mask = get_mask(new_prefix)
        broadcast = subnet_ip | (~mask & 0xFFFFFFFF)
        first_host = subnet_ip + 1
        last_host = broadcast - 1
        total_hosts = subnet_size - 2
        # Simple, easy-to-read output
        print(f"Subnet {i+1}: {int_to_ip(subnet_ip)}/{new_prefix}")
        print(f"  Broadcast: {int_to_ip(broadcast)}")
        if total_hosts > 0:
            print(f"  Hosts: {total_hosts}  Range: {int_to_ip(first_host)} - {int_to_ip(last_host)}")
        else:
            print("  No usable hosts")
        print()


def vlsm():
    print("===== VLSM Subnetting =====")
    base_network_input = input("Enter Base Network (EX: 192.168.10.0/24): ").strip()
    if '/' not in base_network_input:
        print("Invalid input format. Use a/b (e.g. 192.168.10.0/24)")
        return

    network_addr, prefix_str = base_network_input.split('/', 1)
    prefix = int(prefix_str)

    num = int(input("Enter Number of Subnets: "))
    if num <= 0:
        print("Number of subnets must be > 0")
        return

    reqs = []
    for i in range(num):
        name = input(f"Enter Subnet Name {i+1}: ").strip()
        hosts = int(input(f"Enter Required Hosts for {name}: "))
        reqs.append((name, hosts))

    # sort descending by required hosts
    reqs.sort(key=lambda x: x[1], reverse=True)

    current_ip = ip_to_int(network_addr)

    print("\nVLSM Subnet Details")
    for name, hosts_needed in reqs:
        total_needed = hosts_needed + 2
        subnet_bits = math.ceil(math.log2(total_needed)) if total_needed > 1 else 0
        prefix_len = 32 - subnet_bits
        mask = get_mask(prefix_len)
        broadcast = current_ip | (~mask & 0xFFFFFFFF)
        first_host = current_ip + 1
        last_host = broadcast - 1
        available_hosts = (1 << subnet_bits) - 2 if subnet_bits > 0 else 0
        # Simple, easy-to-read output
        print(f"Subnet: {name}  -> {int_to_ip(current_ip)}/{prefix_len}")
        print(f"  Broadcast: {int_to_ip(broadcast)}")
        if available_hosts > 0:
            print(f"  Hosts: {available_hosts}  Range: {int_to_ip(first_host)} - {int_to_ip(last_host)}")
        else:
            print("  No usable hosts")
        print()

        # advance current_ip by block size
        block_size = 1 << subnet_bits if subnet_bits > 0 else 1
        current_ip = (current_ip + block_size) & 0xFFFFFFFF


def main():
    try:
        while True:
            print("============================")
            print(" FLSM and VLSM Calculator")
            print("============================")
            print("1. Fixed Length Subnet Masking (FLSM)")
            print("2. Variable Length Subnet Masking (VLSM)")
            print("3. Exit")
            choice = input("Enter Your Choice: ").strip()

            if choice == '1':
                flsm()
            elif choice == '2':
                vlsm()
            elif choice == '3':
                print("Exiting Program...")
                break
            else:
                print("Invalid Choice! Please Try Again.")
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")


if __name__ == '__main__':
    main()
