// error_receiver.cpp  (Windows)
// Compile (MSVC):  cl /EHsc /std:c++17 error_receiver.cpp ws2_32.lib /Fe:error_receiver.exe
// Compile (MinGW): g++ -o error_receiver.exe error_receiver.cpp -std=c++17 -lws2_32
// Usage  :  run this BEFORE error_sender.exe

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")

#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include <stdexcept>

#include "error_common.h"

static const int PORT = 9091;

// ── Winsock RAII ──────────────────────────────────────────────────────────────
struct WinsockGuard {
    WinsockGuard() {
        WSADATA wsa;
        if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
            throw std::runtime_error("WSAStartup failed: " +
                                     std::to_string(WSAGetLastError()));
    }
    ~WinsockGuard() { WSACleanup(); }
};

// ── Socket helpers ────────────────────────────────────────────────────────────
bool recv_exact(SOCKET sock, char* buf, int n) {
    int got = 0;
    while (got < n) {
        int r = recv(sock, buf + got, n - got, 0);
        if (r <= 0) return false;
        got += r;
    }
    return true;
}

bool recv_packet(SOCKET sock, std::string& out) {
    uint32_t net_len;
    if (!recv_exact(sock, reinterpret_cast<char*>(&net_len), 4)) return false;
    uint32_t len = ntohl(net_len);
    if (len == 0) { out.clear(); return true; }
    out.resize(len);
    return recv_exact(sock, &out[0], static_cast<int>(len));
}

// ── Status banner ─────────────────────────────────────────────────────────────
void print_status(bool ok) {
    if (ok)
        std::cout << "\n  STATUS: [OK]  No errors detected.\n";
    else
        std::cout << "\n  STATUS: [ERROR]  Corruption detected!\n";
}

// ═════════════════════════════════════════════════════════════════════════════
int main() {
    WinsockGuard wsa;

    SOCKET server_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_fd == INVALID_SOCKET) {
        std::cerr << "socket() failed: " << WSAGetLastError() << "\n";
        return 1;
    }

    BOOL opt = TRUE;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR,
               reinterpret_cast<const char*>(&opt), sizeof(opt));

    sockaddr_in addr{};
    addr.sin_family      = AF_INET;
    addr.sin_port        = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_fd, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "bind() failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd); return 1;
    }
    if (listen(server_fd, 1) == SOCKET_ERROR) {
        std::cerr << "listen() failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd); return 1;
    }

    std::cout << "[Receiver] Listening on port " << PORT << " ...\n";

    sockaddr_in client_addr{};
    int client_len = sizeof(client_addr);
    SOCKET client_fd = accept(server_fd,
                              reinterpret_cast<sockaddr*>(&client_addr),
                              &client_len);
    if (client_fd == INVALID_SOCKET) {
        std::cerr << "accept() failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd); return 1;
    }
    char ip_buf[INET_ADDRSTRLEN] = {};
    strcpy(ip_buf, inet_ntoa(client_addr.sin_addr));
    std::cout << "[Receiver] Sender connected from " << ip_buf << "\n";

    std::string msg;
    while (recv_packet(client_fd, msg)) {
        if (msg == "QUIT") {
            std::cout << "\n[Receiver] Sender disconnected. Bye!\n";
            break;
        }

        if (msg.size() < 3 || msg[2] != '|') {
            std::cerr << "[Receiver] Unknown message format.\n";
            continue;
        }

        std::string tag     = msg.substr(0, 2);
        std::string payload = msg.substr(3);

        std::cout << "\n" << std::string(60, '=') << "\n";

        try {
            // ── Parity ────────────────────────────────────────────────────
            if (tag == "PR") {
                std::cout << "Received: PARITY-PROTECTED DATA\n";
                std::cout << std::string(60, '=') << "\n";

                ParityResult r = parity_decode(payload);

                uint8_t recv_parity = static_cast<uint8_t>(payload.back());
                std::cout << "Data bits         : " << r.bits << "\n";
                std::cout << "Number of 1s      : " << r.ones_count << "\n";
                std::cout << "Parity recomputed : " << static_cast<int>(r.parity_bit) << "\n";
                std::cout << "Parity received   : " << static_cast<int>(recv_parity) << "\n";
                print_status(r.ok);

            // ── Block Parity ──────────────────────────────────────────────
            } else if (tag == "BP") {
                std::cout << "Received: BLOCK (2D) PARITY DATA\n";
                std::cout << std::string(60, '=') << "\n";

                BlockParityResult r = block_parity_decode(payload);

                std::cout << "Data bits        : " << r.bits << "\n";
                std::cout << "Grid (" << r.rows << " rows x " << r.cols << " cols):\n";
                std::cout << std::string(56, '-') << "\n";
                for (int row = 0; row < r.rows; row++) {
                    std::cout << "  Row " << row << "  :";
                    for (int col = 0; col < r.cols; col++)
                        std::cout << "  " << static_cast<int>(r.grid[row][col]);
                    std::cout << "   | RowParity: " << static_cast<int>(r.row_parity[row]) << "\n";
                }
                std::cout << std::string(56, '-') << "\n";
                std::cout << "ColParity:";
                for (int col = 0; col < r.cols; col++)
                    std::cout << "  " << static_cast<int>(r.col_parity[col]);
                std::cout << "\n";
                print_status(r.ok);

            // ── CRC-8 ─────────────────────────────────────────────────────
            } else if (tag == "CR") {
                std::cout << "Received: CRC-8 PROTECTED DATA\n";
                std::cout << std::string(60, '=') << "\n";

                CRC8Result r = crc8_decode(payload);

                std::cout << "Data bits        : " << r.bits << "\n";
                std::cout << "Packed bytes(hex): ";
                for (unsigned char c : r.packed_bytes) std::cout << to_hex8(c) << " ";
                std::cout << "\n";
                std::cout << "CRC-8 recomputed : " << to_hex8(r.crc)
                          << "  (" << std::bitset<8>(r.crc) << ")\n";
                uint8_t recv_crc = static_cast<uint8_t>(payload.back());
                std::cout << "CRC-8 received   : " << to_hex8(recv_crc)
                          << "  (" << std::bitset<8>(recv_crc) << ")\n";
                print_status(r.ok);

            // ── Checksum ──────────────────────────────────────────────────
            } else if (tag == "CS") {
                std::cout << "Received: CHECKSUM-PROTECTED DATA\n";
                std::cout << std::string(60, '=') << "\n";

                ChecksumResult r = checksum_decode(payload);

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
                std::cout << "Checksum recomp. : " << to_hex16(r.checksum) << "\n";
                uint16_t bit_len = (static_cast<uint8_t>(payload[0]) << 8)
                                 |  static_cast<uint8_t>(payload[1]);
                size_t packed_len = (bit_len + 7) / 8;
                uint16_t recv_cs = (static_cast<uint8_t>(payload[2 + packed_len]) << 8)
                                 |  static_cast<uint8_t>(payload[2 + packed_len + 1]);
                std::cout << "Checksum received: " << to_hex16(recv_cs) << "\n";
                print_status(r.ok);

            } else {
                std::cerr << "[Receiver] Unknown tag '" << tag << "'\n";
            }

        } catch (const std::exception& e) {
            std::cerr << "[Receiver] Decode error: " << e.what() << "\n";
        }

        std::cout << std::string(60, '=') << "\n";
    }

    closesocket(client_fd);
    closesocket(server_fd);
    return 0;
}
