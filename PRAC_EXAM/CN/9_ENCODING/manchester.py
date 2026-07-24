import matplotlib.pyplot as plt

def manchester_encode(binary_string):
    encoded = ""

    for bit in binary_string:
        if bit == "0":
            encoded += "10"
        else:
            encoded += "01"

    return encoded


def plot_signal(encoded):
    signal = [int(bit) for bit in encoded]
    x = range(len(signal))
    plt.step(x, signal)
    plt.show()


# Main Program
original = input("Enter binary string: ")

encoded = manchester_encode(original)

print("Original :", original)
print("Encoded  :", encoded)

plot_signal(encoded)