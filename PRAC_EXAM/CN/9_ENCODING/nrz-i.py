import matplotlib.pyplot as plt

def nrzi_encode(bits):
    level = 0
    encoded = ""

    for bit in bits:
        # Transition for bit 1
        if bit == '1':
            level = 1 - level

        encoded += str(level)

    return encoded

def plot_signal(encoded):
    signal = [int(bit) for bit in encoded]
    x = range(len(signal))
    plt.step(x, signal,where='post')
    plt.show()


# Main Program
bits = input("Enter binary string: ")

encoded = nrzi_encode(bits)

print("Original :", bits)
print("Encoded  :", encoded)

plot_signal(encoded)