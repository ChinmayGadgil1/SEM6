#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <cstdlib>
#pragma comment(lib, "ws2_32.lib")

using namespace std;

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);

    SOCKET sockfd;
    char buffer[1024];
    sockaddr_in receiverAddr{}, senderAddr{};
    int addr_len = sizeof(senderAddr);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    receiverAddr.sin_family = AF_INET;
    receiverAddr.sin_port = htons(5001);
    receiverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(sockfd, (sockaddr*)&receiverAddr, sizeof(receiverAddr));

    int expected = 0;

    cout << "RECEIVER STARTED\n\n";

    while (true) {
        memset(buffer, 0, sizeof(buffer));

        recvfrom(sockfd, buffer, sizeof(buffer), 0,
                 (sockaddr*)&senderAddr, &addr_len);

        cout << "RECEIVER: Frame arrived -> " << buffer << endl;

        int seq = buffer[6] - '0';

        // 1. Simulate frame loss
        if (rand() % 100 < 20) {
            cout << "RECEIVER: Frame lost\n\n";
            continue;
        }

        // 2. Simulate corruption
        bool corrupted = (rand() % 100 < 20);
        if (corrupted) {
            cout << "RECEIVER: Frame corrupted\n";

            char nak[10];
            sprintf(nak, "NAK:%d", seq);

            sendto(sockfd, nak, strlen(nak), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: NAK sent -> " << nak << "\n\n";
            continue;
        }

        if (seq == expected) {
            cout << "RECEIVER: Correct frame received\n";

            // 3. Simulate delayed ACK
            if (rand() % 100 < 20) {
                cout << "RECEIVER: Delaying ACK...\n";
                Sleep(3000);
            }

            char ack[10];
            sprintf(ack, "ACK:%d", seq);

            // 4. Simulate ACK loss
            if (rand() % 100 < 20) {
                cout << "RECEIVER: ACK lost\n\n";
                continue;
            }

            sendto(sockfd, ack, strlen(ack), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: ACK sent -> " << ack << endl;

            expected = 1 - expected;
        } else {
            cout << "RECEIVER: Duplicate frame\n";

            char ack[10];
            sprintf(ack, "ACK:%d", 1 - expected);

            sendto(sockfd, ack, strlen(ack), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: Re-sent ACK -> " << ack << endl;
        }

        cout << endl;
    }

    closesocket(sockfd);
    WSACleanup();
    return 0;
}