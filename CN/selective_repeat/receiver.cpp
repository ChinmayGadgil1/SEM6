#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <map>
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

    int base = 0;
    int windowSize = 4;

    map<int, string> recvBuffer;
    map<int, bool> received; // track all received frames

    cout << "RECEIVER STARTED (SELECTIVE REPEAT)\n\n";

    while (true) {
        memset(buffer, 0, sizeof(buffer));

        recvfrom(sockfd, buffer, sizeof(buffer), 0,
                 (sockaddr*)&senderAddr, &addr_len);

        string frameStr(buffer);
        cout << "RECEIVER: Frame arrived -> " << frameStr << endl;

        int seq = stoi(frameStr.substr(6, frameStr.find(":", 6) - 6));

        // simulate frame loss
        if (rand() % 100 < 20) {
            cout << "RECEIVER: Frame lost\n\n";
            continue;
        }

        // Case 1: Frame inside window
        if (seq >= base && seq < base + windowSize) {

            if (!received[seq]) {
                cout << "RECEIVER: Frame " << seq << " accepted and buffered\n";
                recvBuffer[seq] = frameStr;
                received[seq] = true;
            } else {
                cout << "RECEIVER: Duplicate frame " << seq << endl;
            }

            char ack[20];
            sprintf(ack, "ACK:%d", seq);

            // simulate ACK loss
            if (rand() % 100 < 20) {
                cout << "RECEIVER: ACK lost\n\n";
                continue;
            }

            sendto(sockfd, ack, strlen(ack), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: ACK sent -> " << ack << endl;

            // deliver in-order frames
            while (received[base]) {
                cout << "RECEIVER: Delivering frame " << base << endl;
                recvBuffer.erase(base);
                base++;
            }
        }

        // Case 2: Old frame (already delivered)
        else if (seq < base) {
            cout << "RECEIVER: Old frame received again\n";

            char ack[20];
            sprintf(ack, "ACK:%d", seq);

            sendto(sockfd, ack, strlen(ack), 0,
                   (sockaddr*)&senderAddr, addr_len);

            cout << "RECEIVER: Re-sent ACK -> " << ack << endl;
        }

        // Case 3: Future frame (outside window)
        else {
            cout << "RECEIVER: Frame outside window ignored\n";
        }

        cout << endl;
    }

    closesocket(sockfd);
    WSACleanup();
    return 0;
}