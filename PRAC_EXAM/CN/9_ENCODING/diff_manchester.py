import matplotlib.pyplot as plt
import numpy as np


def diff_manchester_encode(bits, start_level=1):
    level = start_level
    encoded = []

    for bit in bits:

        # For 0, change the level at the beginning
        if bit == '0':
            level = 1 - level

        # Store the first half of the bit
        encoded.append(level)

        # Mid-bit transition (always happens)
        level = 1 - level
        encoded.append(level)

    return ''.join(str(bit) for bit in encoded)


def plot_signal(encoded):
    values = [int(bit) for bit in encoded]
    x = np.arange(len(values))

    plt.figure(figsize=(10, 3))
    plt.step(x, values, where='post', linewidth=2)

    plt.xticks([])
    plt.yticks([])
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# Main Program
bits = input("Enter binary string: ")

encoded = diff_manchester_encode(bits)

print("Original :", bits)
print("Encoded  :", encoded)

plot_signal(encoded)