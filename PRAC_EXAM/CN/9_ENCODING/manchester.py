import matplotlib.pyplot as plt
import numpy as np

def manchester_encode(binary_string):
  
    encoded = ""
    for bit in binary_string:
        if bit == '0':
            encoded += "10"
        elif bit == '1':
            encoded += "01"
    return encoded


def manchester_decode(encoded_string):
   
    if len(encoded_string) % 2 != 0:
        return "Invalid encoded string length"
    
    decoded = ""
    for i in range(0, len(encoded_string), 2):
        pair = encoded_string[i:i+2]
        if pair == "10":
            decoded += "0"
        elif pair == "01":
            decoded += "1"
        else:
            return "Invalid Manchester encoding"
    return decoded


def plot_signals(original, encoded):
    plt.figure(figsize=(10, 4))
    
    encoded_signal = [int(bit) for bit in encoded]
    x_enc = np.arange(len(encoded_signal))
    plt.step(x_enc, encoded_signal, where='mid', linewidth=2, color='green')
    
    plt.ylim(-0.5, 1.5)
    plt.xticks([])
    plt.yticks([])
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    original = "10101101"
    encoded = manchester_encode(original)
    decoded = manchester_decode(encoded)
    
    print(f"Original: {original}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    
    # Plot the encoded signal with original bit labels
    plot_signals(original, encoded)