#include <SFML/Graphics.hpp>
#include <vector>
#include <string>

using namespace std;

const int WIDTH = 1000;
const int HEIGHT = 600;

float senderX = 200;
float receiverX = 800;
float speed = 0.4;

struct Packet {
    int id;
    float x, y;
    bool isAck;
    bool delivered;
};

vector<Packet> packets;

// Draw sender & receiver
void drawEndpoints(sf::RenderWindow &window) {
    sf::RectangleShape sender(sf::Vector2f(5, 400));
    sender.setPosition(senderX, 100);

    sf::RectangleShape receiver(sf::Vector2f(5, 400));
    receiver.setPosition(receiverX, 100);

    window.draw(sender);
    window.draw(receiver);
}

// Draw packets
void drawPackets(sf::RenderWindow &window, sf::Font &font) {
    for (auto &p : packets) {
        sf::RectangleShape rect(sf::Vector2f(40, 30));
        rect.setPosition(p.x, p.y);

        if (p.isAck)
            rect.setFillColor(sf::Color::Yellow);
        else
            rect.setFillColor(sf::Color::Red);

        window.draw(rect);

        // Label
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(14);
        text.setFillColor(sf::Color::Black);

        if (p.isAck)
            text.setString("A" + to_string(p.id));
        else
            text.setString(to_string(p.id));

        text.setPosition(p.x + 10, p.y + 5);
        window.draw(text);
    }
}

////////////////////////////////////////////////////////////
// STOP AND WAIT
////////////////////////////////////////////////////////////
void stopAndWait() {
    static int current = 1;
    static bool waitingAck = false;

    if (!waitingAck && current <= 5) {
        packets.push_back({current, senderX, 200, false, false});
        waitingAck = true;
    }

    for (auto &p : packets) {
        if (!p.isAck) {
            p.x += speed;

            if (p.x >= receiverX && !p.delivered) {
                p.delivered = true;
                packets.push_back({p.id, receiverX, 250, true, false});
            }
        } else {
            p.x -= speed;

            if (p.x <= senderX) {
                packets.clear();
                waitingAck = false;
                current++;
            }
        }
    }
}

////////////////////////////////////////////////////////////
// GO BACK N
////////////////////////////////////////////////////////////
void goBackN() {
    static int base = 1;
    static int nextSeq = 1;
    int windowSize = 3;

    if (nextSeq < base + windowSize && nextSeq <= 5) {
        packets.push_back({nextSeq, senderX, 150 + nextSeq * 40, false, false});
        nextSeq++;
    }

    for (auto &p : packets) {
        if (!p.isAck) {
            p.x += speed;

            if (p.x >= receiverX && !p.delivered) {
                p.delivered = true;

                if (p.id == base) {
                    packets.push_back({p.id, receiverX, 300, true, false});
                }
            }
        } else {
            p.x -= speed;

            if (p.x <= senderX) {
                base++;
                packets.clear();
            }
        }
    }
}

////////////////////////////////////////////////////////////
// SELECTIVE REPEAT
////////////////////////////////////////////////////////////
void selectiveRepeat() {
    static int base = 1;
    static int nextSeq = 1;
    int windowSize = 3;

    if (nextSeq < base + windowSize && nextSeq <= 5) {
        packets.push_back({nextSeq, senderX, 150 + nextSeq * 40, false, false});
        nextSeq++;
    }

    for (auto &p : packets) {
        if (!p.isAck) {
            p.x += speed;

            if (p.x >= receiverX && !p.delivered) {
                p.delivered = true;
                packets.push_back({p.id, receiverX, 300, true, false});
            }
        } else {
            p.x -= speed;

            if (p.x <= senderX) {
                base++;
            }
        }
    }
}

////////////////////////////////////////////////////////////
// MAIN
////////////////////////////////////////////////////////////
int main() {
    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "CN Flow Control Simulator");

    sf::Font font;
    font.loadFromFile("C:/Windows/Fonts/arial.ttf");

    int mode = 1;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Num1)) {
                packets.clear();
                mode = 1;
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Num2)) {
                packets.clear();
                mode = 2;
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Num3)) {
                packets.clear();
                mode = 3;
            }
        }

        window.clear(sf::Color::White);

        drawEndpoints(window);

        if (mode == 1) stopAndWait();
        else if (mode == 2) goBackN();
        else selectiveRepeat();

        drawPackets(window, font);

        window.display();
    }

    return 0;
}