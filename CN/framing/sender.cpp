// sender.cpp  (Windows)
// Compile (MSVC Developer Command Prompt):
//   cl /EHsc /std:c++17 sender.cpp ws2_32.lib /Fe:sender.exe
// Compile (MinGW / MSYS2):
//   g++ -o sender.exe sender.cpp -std=c++17 -lws2_32

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

#include "framing_common.h"

static const int   PORT      = 9090;
static const char* SERVER_IP = "127.0.0.1";

// ── Winsock init/cleanup ──────────────────────────────────────────────────────
struct WinsockGuard {
    WinsockGuard() {
        WSADATA wsa;
        int err = WSAStartup(MAKEWORD(2, 2), &wsa);
        if (err != 0)
            throw std::runtime_error("WSAStartup failed, code: " + std::to_string(err));
    }
    ~WinsockGuard() { WSACleanup(); }
};

// ── Connection ────────────────────────────────────────────────────────────────
SOCKET create_connection() {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET)
        throw std::runtime_error("socket() failed, code: " +
                                 std::to_string(WSAGetLastError()));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port   = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    if (connect(sock, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) == SOCKET_ERROR) {
        closesocket(sock);
        throw std::runtime_error("connect() failed - is receiver.exe running?  code: " +
                                 std::to_string(WSAGetLastError()));
    }
    return sock;
}

// ── Send helper ───────────────────────────────────────────────────────────────
void send_frame(SOCKET sock, const std::string& data) {
    uint32_t net_len = htonl(static_cast<uint32_t>(data.size()));
    send(sock, reinterpret_cast<const char*>(&net_len), 4, 0);
    send(sock, data.data(), static_cast<int>(data.size()), 0);
}

// ── Menu ──────────────────────────────────────────────────────────────────────
void print_menu() {
    std::cout << "\n=== Framing Methods (Sender) ===\n"
              << "1. Character Count\n"
              << "2. Byte Stuffing\n"
              << "3. Bit Stuffing\n"
              << "4. Exit\n"
              << "Choice: ";
}

int main() {
    WinsockGuard wsa;   // WSAStartup here; WSACleanup automatically on exit

    SOCKET sock = INVALID_SOCKET;
    try { sock = create_connection(); }
    catch (const std::exception& e) {
        std::cerr << "[ERROR] " << e.what() << "\n";
        return 1;
    }
    std::cout << "[INFO] Connected to receiver at " << SERVER_IP << ":" << PORT << "\n";

    std::string choice;
    while (true) {
        print_menu();
        std::getline(std::cin, choice);

        if (choice == "4") {
            send_frame(sock, "QUIT");
            std::cout << "Exiting...\n";
            break;
        }

        if (choice == "1") {
            std::string data, tmp;
            std::cout << "Enter text data: ";
            std::getline(std::cin, data);
            std::cout << "Enter total frame size (e.g. 5): ";
            std::getline(std::cin, tmp);
            int frame_size = std::stoi(tmp);

            try {
                auto frames = character_count_encode(data, frame_size);
                std::string packed;
                for (auto& f : frames) packed += f;

                std::cout << "\n" << std::string(50, '=') << "\n";
                std::cout << "Character Count Frames (sending):\n";
                std::cout << std::string(50, '=') << "\n";
                int idx = 1;
                for (auto& f : frames) {
                    int count = static_cast<unsigned char>(f[0]);
                    std::cout << "Frame " << idx++ << ": [" << count << "]";
                    for (int j = 1; j < static_cast<int>(f.size()); j++)
                        std::cout << "[" << f[j] << "]";
                    std::cout << "\n";
                }
                send_frame(sock, "CC|" + packed);
                std::cout << "[INFO] Sent " << frames.size() << " frame(s).\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }

        } else if (choice == "2") {
            std::string data;
            std::cout << "Enter text data (FLAG and ESC in data are handled): ";
            std::getline(std::cin, data);

            try {
                std::string framed = byte_stuff(data);
                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "Byte Stuffing:\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Original : " << data   << "\n";
                std::cout << "Framed   : " << framed << "\n";
                std::cout << "Structure: [FLAG][stuffed data][FLAG]\n";
                std::cout << "  - ESC in data  --> ESC ESC\n";
                std::cout << "  - FLAG in data --> ESC FLAG\n";
                send_frame(sock, "BS|" + framed);
                std::cout << "[INFO] Sent byte-stuffed frame.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }

        } else if (choice == "3") {
            std::string bits;
            std::cout << "Enter bit data (only 0s and 1s): ";
            std::getline(std::cin, bits);
            bits.erase(
                std::remove_if(bits.begin(), bits.end(), [](char c){ return c == ' '; }),
                bits.end());

            try {
                std::string framed = bit_stuff(bits);
                std::cout << "\n" << std::string(60, '=') << "\n";
                std::cout << "Bit Stuffing:\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Original  : " << bits   << "\n";
                std::cout << "Framed    : " << framed << "\n";
                std::cout << "Structure : [01111110][stuffed bits][01111110]\n";
                std::cout << "  - After 5 consecutive 1s, a 0 is inserted\n";
                send_frame(sock, "BT|" + framed);
                std::cout << "[INFO] Sent bit-stuffed frame.\n";
            } catch (const std::exception& e) {
                std::cerr << "[ERROR] " << e.what() << "\n";
            }

        } else {
            std::cout << "Invalid choice. Enter 1-4.\n";
        }
    }

    closesocket(sock);
    return 0;
}