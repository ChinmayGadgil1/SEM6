#include <iostream>
#include <cstdlib>
#include <ctime>
#include <windows.h>
using namespace std;

void delay(int ms) {
    Sleep(ms);
}

void drawFrame(int frame, bool lost) {
    cout << "S |\\     | R\n"; delay(80);
    cout << "  | \\    |\n"; delay(80);

    if(lost) {
        cout << "  |  \\   Frame " << frame << " (LOST)\n"; delay(80);
        cout << "  |   X\n"; delay(80);
        cout << "  |       |\n"; delay(80);
    } else {
        cout << "  |  \\   |   Frame " << frame << "\n"; delay(80);
        cout << "  |   \\  |\n"; delay(80);
        cout << "  |    \\ |\n"; delay(80);
    }
}

void drawACK(int frame) {
    cout << "S |    / | R\n"; delay(80);
    cout << "  |   /  |\n"; delay(80);
    cout << "  |  /   |   ACK " << frame << "\n"; delay(80);
    cout << "  | /    |\n"; delay(80);
    cout << "  |/     |\n"; delay(80);
}

int main() {
    int totalFrames, windowSize;
    cout << "Enter number of frames: ";
    cin >> totalFrames;
    cout << "Enter window size: ";
    cin >> windowSize;

    srand(time(0));

    cout << "\n=== Go-Back-N Simulation ===\n";
    cout << "Time ↓\n\n";

    int base = 1;

    while(base <= totalFrames) {
        cout << "\n[Window starting at Frame " << base << "]\n";

        int i;
        bool errorOccurred = false;

        // Send window
        for(i = base; i < base + windowSize && i <= totalFrames; i++) {
            bool lost = (rand() % 100) < 25;
            drawFrame(i, lost);

            if(lost) {
                cout << "⚠ Frame " << i << " lost!\n";
                errorOccurred = true;
                break;
            }
        }

        if(errorOccurred) {
            cout << "❌ Go-Back-N → Resending from Frame " << base << "\n";
            delay(800);
            continue;
        }

        // Send cumulative ACK
        drawACK(i - 1);
        cout << "✔ ACK " << i-1 << " received (cumulative)\n";

        base = i;
        delay(700);
    }

    cout << "\n🎉 Transmission Complete (Go-Back-N)\n";
    return 0;
}