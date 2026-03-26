#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <vector>
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

    vector<string> frames = {"A","B","C","D","E","F","G","H"};

    int base = 0;
    int nextSeq = 0;
    int windowSize = 4;
    int n = frames.size();

    cout << "SENDER STARTED (GO-BACK-N)\n\n";

    while (base < n) {

        // send window
        while (nextSeq < base + windowSize && nextSeq < n) {
            string frame = "FRAME:" + to_string(nextSeq) + ":" + frames[nextSeq];

            cout << "SENDER: Sending -> " << frame << endl;

            sendto(sockfd, frame.c_str(), frame.size(), 0,
                   (sockaddr*)&receiverAddr, addr_len);

            nextSeq++;
        }

        memset(buffer, 0, sizeof(buffer));

        int bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0, NULL, NULL);

        if (bytes == SOCKET_ERROR) {
            cout << "SENDER: Timeout, retransmitting window\n";

            for (int i = base; i < nextSeq; i++) {
                string frame = "FRAME:" + to_string(i) + ":" + frames[i];

                cout << "SENDER: Retransmitting -> " << frame << endl;

                sendto(sockfd, frame.c_str(), frame.size(), 0,
                       (sockaddr*)&receiverAddr, addr_len);
            }

            cout << endl;
            continue;
        }

        cout << "SENDER: Received -> " << buffer << endl;

        int ack = stoi(string(buffer).substr(4));

        if (ack >= base) {
            base = ack + 1;
            cout << "SENDER: Sliding window, new base = " << base << endl;
        }

        cout << endl;
    }

    cout << "ALL FRAMES SENT SUCCESSFULLY\n";

    closesocket(sockfd);
    WSACleanup();
    return 0;
}