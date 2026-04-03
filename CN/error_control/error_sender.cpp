#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#include <iostream>
#include <string>
#include <iomanip>
#include <stdexcept>
#include "error_common.h"
static const int   PORT      = 9091;
static const char* SERVER_IP = "127.0.0.1";
struct WinsockGuard {
    WinsockGuard() {
        WSADATA wsa;
        int err = WSAStartup(MAKEWORD(2, 2), &wsa);
        if (err != 0)
            throw std::runtime_error("WSAStartup failed, code: " + std::to_string(err));
    }
    ~WinsockGuard() { WSACleanup(); }
};
SOCKET create_connection() {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET)
        throw std::runtime_error("socket() failed, code: " +
                                 std::to_string(WSAGetLastError()));
    sockaddr_in addr{};
    addr.sin_family      = AF_INET;
    addr.sin_port        = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(SERVER_IP);
    if (connect(sock, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) == SOCKET_ERROR) {
        closesocket(sock);
        throw std::runtime_error("connect() failed - is error_receiver.exe running? code: " +
                                 std::to_string(WSAGetLastError()));
    }
    return sock;
}
void send_packet(SOCKET sock, const std::string& payload) {
    uint32_t net_len = htonl(static_cast<uint32_t>(payload.size()));
    send(sock, reinterpret_cast<const char*>(&net_len), 4, 0);
    send(sock, payload.data(), static_cast<int>(payload.size()), 0);
}
void print_bits(const std::string& label, const std::string& data) {
    std::cout << label;
    for (unsigned char c : data)
        std::cout << std::bitset<8>(c) << " ";
    std::cout << "\n";
}
void print_menu() {
    std::cout << "\n"
              << "=== Error Control Methods (Sender) ===\n"
              << "1. Parity (Even, entire bit string)\n"
              << "2. Block (2D) Parity (bit matrix)\n"
              << "3. CRC (data bits + generator polynomial)\n"
              << "4. Hamming (7,4)\n"
              << "5. Reed-Solomon (GF(2^8))\n"
              << "6. Checksum (16-bit one's complement)\n"
              << "7. Exit\n"
              << "Choice: ";
}
int main() {
    WinsockGuard wsa;

    SOCKET sock = INVALID_SOCKET;
    try { sock = create_connection(); }
    catch (const std::exception& e) {
        std::cerr << "[ERROR] " << e.what() << "\n";
        return 1;
    }
    std::cout << "[INFO] Connected to error_receiver at "
              << SERVER_IP << ":" << PORT << "\n";
    std::string choice;
    while (true) {
        print_menu();
        std::getline(std::cin, choice);

        if (choice == "7") {
            send_packet(sock, "QUIT");
            std::cout << "Exiting...\n";
            break;
        }
        if (choice == "1") {
            std::string data;
            std::cout << "Enter bit data (e.g. 1010): ";
            std::getline(std::cin, data);

            try {
                ParityResult r = parity_encode(data);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "PARITY (Even, entire bit string)\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Data bits        : " << r.bits << "\n";
                std::cout << "Number of 1s     : " << r.ones_count << "\n";
                std::cout << "Parity bit (even): " << static_cast<int>(r.parity_bit) << "\n";
                std::cout << "Codeword         : " << r.bits << static_cast<int>(r.parity_bit) << "\n";

                send_packet(sock, "PR|" + parity_pack(r));
                std::cout << "[INFO] Sent parity-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else if (choice == "2") {
            std::string data, tmp_rows, tmp_cols;
            std::cout << "Enter number of rows: ";
            std::getline(std::cin, tmp_rows);
            std::cout << "Enter number of columns: ";
            std::getline(std::cin, tmp_cols);

            int rows = 0, cols = 0;
            try { rows = std::stoi(tmp_rows); } catch (...) { rows = 0; }
            try { cols = std::stoi(tmp_cols); } catch (...) { cols = 0; }
            if (rows <= 0 || cols <= 0) {
                std::cerr << "[ERROR] Rows and columns must be positive integers.\n";
                continue;
            }

            std::cout << "Enter bit data in row-major order (exactly "
                      << (rows * cols) << " bits): ";
            std::getline(std::cin, data);

            try {
                BlockParityResult r = block_parity_encode(data, rows, cols);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "BLOCK (2D) PARITY  —  "
                          << r.rows << " rows x " << r.cols << " cols\n";
                std::cout << std::string(60, '=') << "\n";

                std::cout << "Data bits: " << r.bits << "\n";
                std::cout << "\nGrid (bits)";
                for (int c = 0; c < cols; c++)
                    std::cout << "  C" << c;
                std::cout << " | P(row)\n";
                std::cout << std::string(56, '-') << "\n";
                for (int row = 0; row < r.rows; row++) {
                    std::cout << "  Row " << row << "  :";
                    for (int col = 0; col < cols; col++)
                        std::cout << "  " << static_cast<int>(r.grid[row][col]);
                    std::cout << " |   " << static_cast<int>(r.row_parity[row]) << "\n";
                }
                std::cout << std::string(56, '-') << "\n";
                std::cout << "P(col)  :";
                for (int col = 0; col < cols; col++)
                    std::cout << "  " << static_cast<int>(r.col_parity[col]);
                std::cout << "\n";

                send_packet(sock, "BP|" + block_parity_pack(r));
                std::cout << "[INFO] Sent block-parity-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else if (choice == "3") {
            std::string data_bits, generator_bits;
            std::cout << "Enter data bits (e.g. 11010101): ";
            std::getline(std::cin, data_bits);
            std::cout << "Enter generator polynomial bits (e.g. 10011): ";
            std::getline(std::cin, generator_bits);

            try {
                CRCPolyResult r = crc_poly_encode(data_bits, generator_bits);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "CRC (Polynomial Division)\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Data bits            : " << r.data_bits << "\n";
                std::cout << "Generator polynomial : " << r.generator_bits << "\n";
                std::cout << "CRC remainder        : " << r.remainder_bits << "\n";
                std::cout << "Transmitted bits     : " << r.transmitted_bits << "\n";

                send_packet(sock, "CR|" + crc_poly_pack(r));
                std::cout << "[INFO] Sent CRC-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else if (choice == "4") {
            std::string data;
            std::cout << "Enter bit data (e.g. 110101011001): ";
            std::getline(std::cin, data);

            try {
                HammingResult r = hamming_encode(data);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "HAMMING (7,4)\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Original data bits : " << r.data_bits << "\n";
                std::cout << "Encoded bits       : " << r.encoded_bits << "\n";
                std::cout << "Codeword length    : " << r.encoded_bits.size() << "\n";

                send_packet(sock, "HM|" + hamming_pack(r));
                std::cout << "[INFO] Sent Hamming-encoded data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else if (choice == "5") {
            std::string data, tmp_nsym;
            std::cout << "Enter bit data (e.g. 110101011001): ";
            std::getline(std::cin, data);
            std::cout << "Enter parity symbols nsym (1..32, e.g. 8): ";
            std::getline(std::cin, tmp_nsym);

            int nsym = 0;
            try { nsym = std::stoi(tmp_nsym); } catch (...) { nsym = 0; }

            try {
                ReedSolomonResult r = reed_solomon_encode(data, nsym);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "REED-SOLOMON\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Data bits         : " << r.bits << "\n";
                std::cout << "Parity symbols    : " << r.nsym << "\n";
                std::cout << "Packed bytes(hex) : ";
                for (unsigned char c : r.packed_bytes) std::cout << to_hex8(c) << " ";
                std::cout << "\n";
                std::cout << "Parity bytes(hex) : ";
                for (unsigned char c : r.parity_bytes) std::cout << to_hex8(c) << " ";
                std::cout << "\n";

                send_packet(sock, "RS|" + reed_solomon_pack(r));
                std::cout << "[INFO] Sent Reed-Solomon-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else if (choice == "6") {
            std::string data;
            std::cout << "Enter bit data (e.g. 110101011001): ";
            std::getline(std::cin, data);

            try {
                ChecksumResult r = checksum_encode(data);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "CHECKSUM  (16-bit one's complement)\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Data bits        : " << r.bits << "\n";
                std::cout << "Packed bytes(hex): ";
                for (unsigned char c : r.packed_bytes) std::cout << to_hex8(c) << " ";
                std::cout << "\n";
                std::cout << "Data (hex words) : ";
                int len = static_cast<int>(r.packed_bytes.size());
                for (int i = 0; i < len; i += 2) {
                    uint16_t w = (static_cast<uint8_t>(r.packed_bytes[i]) << 8)
                               | ((i + 1 < len) ? static_cast<uint8_t>(r.packed_bytes[i + 1]) : 0);
                    std::cout << to_hex16(w) << " ";
                }
                std::cout << "\n";
                std::cout << "Checksum         : " << to_hex16(r.checksum) << "\n";
                std::cout << "Wire format      : [bit_len(2B)] + [packed data] + ["
                          << to_hex8((r.checksum >> 8) & 0xFF) << " "
                          << to_hex8(r.checksum & 0xFF) << "]\n";

                send_packet(sock, "CS|" + checksum_pack(r));
                std::cout << "[INFO] Sent checksum-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }
        } else {
            std::cout << "Invalid choice. Enter 1-7.\n";
        }
    }

    closesocket(sock);
    return 0;
}
