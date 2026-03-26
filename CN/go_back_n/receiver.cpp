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

    cout << "RECEIVER STARTED (GO-BACK-N)\n\n";

    while (true) {
        memset(buffer, 0, sizeof(buffer));

        recvfrom(sockfd, buffer, sizeof(buffer), 0,
                 (sockaddr*)&senderAddr, &addr_len);

        cout << "RECEIVER: Frame arrived -> " << buffer << endl;

        int seq = stoi(string(buffer).substr(6, 1)); // FRAME:x

        // simulate frame loss
        if (rand() % 100 < 20) {
            cout << "RECEIVER: Frame lost\n\n";
            continue;
        }

        if (seq == expected) {
            cout << "RECEIVER: Accepted frame " << seq << endl;
            expected++;

            // cumulative ACK
            int ackNum = expected - 1;
            char ack[20];
            sprintf(ack, "ACK:%d", ackNum);

            // simulate ACK loss
            if (rand() % 100 < 20) {
                cout << "RECEIVER: ACK lost\n\n";
                continue;
            }

            sendto(sockfd, ack, strlen(ack), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: Sent cumulative ACK -> " << ack << endl;
        } else {
            cout << "RECEIVER: Out-of-order frame discarded\n";

            int ackNum = expected - 1;
            char ack[20];
            sprintf(ack, "ACK:%d", ackNum);

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