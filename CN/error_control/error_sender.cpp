// error_sender.cpp  (Windows)
// Compile (MSVC):  cl /EHsc /std:c++17 error_sender.cpp ws2_32.lib /Fe:error_sender.exe
// Compile (MinGW): g++ -o error_sender.exe error_sender.cpp -std=c++17 -lws2_32
// Usage  :  start error_receiver.exe first, then run error_sender.exe

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

static const int   PORT      = 9091;      // different port from framing demo
static const char* SERVER_IP = "127.0.0.1";

// ── Winsock RAII ──────────────────────────────────────────────────────────────
struct WinsockGuard {
    WinsockGuard() {
        WSADATA wsa;
        int err = WSAStartup(MAKEWORD(2, 2), &wsa);
        if (err != 0)
            throw std::runtime_error("WSAStartup failed, code: " + std::to_string(err));
    }
    ~WinsockGuard() { WSACleanup(); }
};

// ── Socket helpers ────────────────────────────────────────────────────────────
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

// Length-prefixed send: 4-byte big-endian length + payload
void send_packet(SOCKET sock, const std::string& payload) {
    uint32_t net_len = htonl(static_cast<uint32_t>(payload.size()));
    send(sock, reinterpret_cast<const char*>(&net_len), 4, 0);
    send(sock, payload.data(), static_cast<int>(payload.size()), 0);
}

// ── Display helpers ───────────────────────────────────────────────────────────
void print_bits(const std::string& label, const std::string& data) {
    std::cout << label;
    for (unsigned char c : data)
        std::cout << std::bitset<8>(c) << " ";
    std::cout << "\n";
}

// ── Menu ──────────────────────────────────────────────────────────────────────
void print_menu() {
    std::cout << "\n"
              << "=== Error Control Methods (Sender) ===\n"
              << "1. Parity (Even, entire bit string)\n"
              << "2. Block (2D) Parity (bit matrix)\n"
              << "3. CRC-8\n"
              << "4. Checksum (16-bit one's complement)\n"
              << "5. Exit\n"
              << "Choice: ";
}

// ═════════════════════════════════════════════════════════════════════════════
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

        if (choice == "5") {
            send_packet(sock, "QUIT");
            std::cout << "Exiting...\n";
            break;
        }

        // ── 1. Parity ─────────────────────────────────────────────────────
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

        // ── 2. Block Parity ───────────────────────────────────────────────
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

        // ── 3. CRC-8 ──────────────────────────────────────────────────────
        } else if (choice == "3") {
            std::string data;
            std::cout << "Enter bit data (e.g. 11010101): ";
            std::getline(std::cin, data);

            try {
                CRC8Result r = crc8_encode(data);

                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "CRC-8  (polynomial " << to_hex8(CRC8_POLY) << ")\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Data bits        : " << r.bits << "\n";
                std::cout << "Packed bytes(hex): ";
                for (unsigned char c : r.packed_bytes) std::cout << to_hex8(c) << " ";
                std::cout << "\n";
                std::cout << "CRC-8            : " << to_hex8(r.crc)
                          << "  (" << std::bitset<8>(r.crc) << ")\n";
                std::cout << "Wire format      : [bit_len(2B)] + [packed data] + [" << to_hex8(r.crc) << "]\n";

                send_packet(sock, "CR|" + crc8_pack(r));
                std::cout << "[INFO] Sent CRC-8-protected data.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }

        // ── 4. Checksum ───────────────────────────────────────────────────
        } else if (choice == "4") {
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
            std::cout << "Invalid choice. Enter 1-5.\n";
        }
    }

    closesocket(sock);
    return 0;
}
