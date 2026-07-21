import matplotlib.pyplot as plt
import numpy as np


def diff_manchester_encode(bits, start_level=1):
    level = start_level
    encoded = []

    for bit in bits:
        if bit == '0':
            level ^= 1

        encoded.extend([level, level ^ 1])
        level ^= 1

    return ''.join(str(bit) for bit in encoded)


def diff_manchester_decode(encoded, start_level=1):
    if len(encoded) % 2 != 0:
        return "Invalid encoded string length"

    bits = []
    prev_level = start_level

    for i in range(0, len(encoded), 2):
        first = encoded[i]
        second = encoded[i + 1]

        if first == second:
            return "Invalid Differential Manchester encoding"

        bit = '0' if int(first) != prev_level else '1'
        bits.append(bit)
        prev_level = int(second)

    return ''.join(bits)


def plot_signal(encoded):
    values = [int(bit) for bit in encoded]
    x_values = np.arange(len(values))

    plt.figure(figsize=(10, 4))
    plt.step(x_values, values, where='post', linewidth=2, color='green')
    plt.xticks([])
    plt.yticks([])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    original = '10101101'
    encoded = diff_manchester_encode(original)
    decoded = diff_manchester_decode(encoded)

    print(f'Original: {original}')
    print(f'Encoded: {encoded}')
    print(f'Decoded: {decoded}')

    plot_signal(encoded)