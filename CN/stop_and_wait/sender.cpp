#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#pragma comment(lib, "ws2_32.lib")

using namespace std;

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);

    SOCKET sockfd;
    char buffer[1024];
    sockaddr_in senderAddr{}, receiverAddr{};
    int addr_len = sizeof(receiverAddr);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    senderAddr.sin_family = AF_INET;
    senderAddr.sin_port = htons(5000);
    senderAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(sockfd, (sockaddr*)&senderAddr, sizeof(senderAddr));

    receiverAddr.sin_family = AF_INET;
    receiverAddr.sin_port = htons(5001);
    receiverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    int timeout = 2000;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO,
               (const char*)&timeout, sizeof(timeout));

    string frames[] = {"Hello", "World", "Stop", "Wait", "ARQ"};

    int seq = 0;

    cout << "SENDER STARTED\n\n";

    for (string msg : frames) {
        while (true) {
            string frame = "FRAME:" + to_string(seq) + ":" + msg;

            cout << "SENDER: Sending -> " << frame << endl;

            sendto(sockfd, frame.c_str(), frame.size(), 0,
                   (sockaddr*)&receiverAddr, addr_len);

            memset(buffer, 0, sizeof(buffer));

            int n = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                             NULL, NULL);

            if (n == SOCKET_ERROR) {
                cout << "SENDER: Timeout, retransmitting\n\n";
                Sleep(1000);
                continue;
            }

            cout << "SENDER: Received -> " << buffer << endl;

            // Handle NAK
            if (buffer[0] == 'N') {
                cout << "SENDER: NAK received, retransmitting\n\n";
                continue;
            }

            int ack = buffer[4] - '0';

            if (ack == seq) {
                cout << "SENDER: Correct ACK\n";
                cout << "SENDER: Moving to next frame\n\n";
                seq = 1 - seq;
                break;
            } else {
                cout << "SENDER: Wrong ACK, retransmitting\n\n";
            }

            Sleep(1000);
        }
    }

    cout << "ALL FRAMES SENT SUCCESSFULLY\n";

    closesocket(sockfd);
    WSACleanup();
    return 0;
}