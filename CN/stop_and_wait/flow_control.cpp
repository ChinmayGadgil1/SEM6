#include <iostream>
#include <cstdlib>
#include <ctime>
#include <windows.h>
using namespace std;

void delay(int ms) {
    Sleep(ms);
}

// Frame: Sender → Receiver
void drawFrame(int frame, bool lost) {
    cout << "S |\\     | R\n"; delay(120);
    cout << "  | \\    |\n"; delay(120);

    if(lost) {
        cout << "  |  \\   Frame " << frame << " (LOST)\n"; delay(120);
        cout << "  |   X\n"; delay(120);
        cout << "  |       |\n"; delay(120);
    } else {
        cout << "  |  \\   |   Frame " << frame << "\n"; delay(120);
        cout << "  |   \\  |\n"; delay(120);
        cout << "  |    \\ |\n"; delay(120);
    }
}

// ACK: Receiver → Sender
void drawACK(int frame, bool lost) {
    if(lost) {
        cout << "S |        | R\n"; delay(120);
        cout << "  |     /  |\n"; delay(120);
        cout << "  |   X    |   ACK " << frame << " (LOST)\n"; delay(120);
        cout << "  |        |\n"; delay(120);
    } else {
        cout << "S |    / | R\n"; delay(120);
        cout << "  |   /  |\n"; delay(120);
        cout << "  |  /   |   ACK " << frame << "\n"; delay(120);
        cout << "  | /    |\n"; delay(120);
        cout << "  |/     |\n"; delay(120);
    }
}

int main() {
    int totalFrames;
    cout << "Enter number of frames: ";
    cin >> totalFrames;

    srand(time(0));

    cout << "\n=== Stop-and-Wait Flow Control (Accurate Diagram) ===\n";
    cout << "Time ↓\n\n";
    cout << "Sender        Receiver\n";
    cout << "----------------------------------\n";

    int frame = 1;

    while(frame <= totalFrames) {
        cout << "\n[Frame " << frame << "]\n";

        delay(400);

        bool frameLost = (rand() % 100) < 25;
        drawFrame(frame, frameLost);

        if(frameLost) {
            cout << "⚠ Frame " << frame << " lost → Timeout → Retransmit\n";
            delay(800);
            continue;
        }

        cout << "✔ Frame received at Receiver\n";
        delay(400);

        bool ackLost = (rand() % 100) < 25;
        drawACK(frame, ackLost);

        if(ackLost) {
            cout << "⚠ ACK lost → Timeout → Retransmit Frame " << frame << "\n";
            delay(800);
            continue;
        }

        cout << "✔ ACK received at Sender\n";
        frame++;
        delay(700);
    }

    cout << "\n🎉 All frames successfully transmitted!\n";

    return 0;
}