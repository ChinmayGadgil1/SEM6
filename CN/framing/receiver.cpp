#include <iostream>
#include <string>
#include <stdexcept>
#include <cstring>
#include <vector>
#include <winsock2.h>
#include <iphlpapi.h>
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")
#include "framing_common.h"
static const int PORT = 9090;
bool recv_exact(SOCKET sock, char* buf, size_t n) {
    size_t received = 0;
    while (received < n) {
        int r = recv(sock, buf + received, n - received, 0);
        if (r <= 0) return false;
        received += r;
    }
    return true;
}
bool recv_frame(SOCKET sock, std::string& out) {
    uint32_t net_len;
    if (!recv_exact(sock, (char*)&net_len, 4)) return false;
    uint32_t len = ntohl(net_len);
    if (len == 0) { out.clear(); return true; }
    out.resize(len);
    return recv_exact(sock, &out[0], len);
}
void display_cc_frame(const std::string& raw_frame, int idx) {
    int count = (unsigned char)raw_frame[0];
    std::cout << "  Frame " << idx << ": [" << count << "]";
    for (int j = 1; j < (int)raw_frame.size(); j++)
        std::cout << "[" << raw_frame[j] << "]";
    std::cout << "\n";
}
int main() {
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        std::cerr << "WSAStartup failed\n";
        return 1;
    }

    SOCKET server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == INVALID_SOCKET) {
        std::cerr << "socket failed\n";
        WSACleanup();
        return 1;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));

    sockaddr_in addr{};
    addr.sin_family      = AF_INET;
    addr.sin_port        = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_fd, (sockaddr*)&addr, sizeof(addr)) < 0) {
        std::cerr << "bind failed\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
    if (listen(server_fd, 1) < 0) {
        std::cerr << "listen failed\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    std::cout << "[Receiver] Listening on port " << PORT << " ...\n";

    sockaddr_in client_addr{};
    int client_len = sizeof(client_addr);
    SOCKET client_fd = accept(server_fd, (sockaddr*)&client_addr, &client_len);
    if (client_fd == INVALID_SOCKET) {
        std::cerr << "accept failed\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
    std::cout << "[Receiver] Sender connected from "
              << inet_ntoa(client_addr.sin_addr) << "\n";
    std::string msg;
    while (recv_frame(client_fd, msg)) {
        if (msg == "QUIT") {
            std::cout << "\n[Receiver] Sender disconnected. Bye!\n";
            break;
        }
        if (msg.size() < 3 || msg[2] != '|') {
            std::cerr << "[Receiver] Unknown message format.\n";
            continue;
        }
        std::string type    = msg.substr(0, 2);
        std::string payload = msg.substr(3);
        std::cout << "\n" << std::string(60, '=') << "\n";
        try {
            if (type == "CC") {
                std::cout << "Received: CHARACTER COUNT FRAME(S)\n";
                std::cout << std::string(60, '=') << "\n";
                int i = 0, idx = 1;
                std::string full_data;
                while (i < (int)payload.size()) {
                    int count = (unsigned char)payload[i];
                    if (count < 1 || i + count > (int)payload.size()) {
                        std::cerr << "[Receiver] Corrupt frame at offset " << i << "\n";
                        break;
                    }
                    std::string frame = payload.substr(i, count);
                    display_cc_frame(frame, idx++);
                    full_data += frame.substr(1);
                    i += count;
                }
                std::string decoded = character_count_decode(payload);
                std::cout << "\nDecoded data : " << decoded << "\n";
                std::cout << "Rule: read count C → next C-1 chars are payload.\n";
            } else if (type == "BS") {
                std::cout << "Received: BYTE STUFFED FRAME\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Raw frame    : " << payload << "\n";
                std::string decoded = byte_unstuff(payload);
                std::cout << "Decoded data : " << decoded  << "\n";
                std::cout << "Unstuffing   : ESC ESC → ESC  |  ESC FLAG → FLAG\n";
            } else if (type == "BT") {
                std::cout << "Received: BIT STUFFED FRAME\n";
                std::cout << std::string(60, '=') << "\n";
                std::cout << "Raw frame    : " << payload << "\n";
                std::string decoded = bit_unstuff(payload);
                std::cout << "Decoded bits : " << decoded  << "\n";
                std::cout << "Unstuffing   : after 5 consecutive 1s, remove the stuffed 0.\n";
            } else {
                std::cerr << "[Receiver] Unknown type '" << type << "'\n";
            }
        } catch (const std::exception& e) {
            std::cerr << "[Receiver] Decode error: " << e.what() << "\n";
        }
        std::cout << std::string(60, '=') << "\n";
    }
    closesocket(client_fd);
    closesocket(server_fd);
    WSACleanup();
    return 0;
}