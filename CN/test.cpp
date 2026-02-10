#include <iostream>
#include <fstream>
#include <cstdio>
using namespace std;

void plotSignal(const string &filename, int V, int len, const string &title, const string &bits)
{
    FILE *gp = popen("gnuplot -persistent", "w");
    fprintf(gp, "set title '%s'\n", title.c_str());
    fprintf(gp, "set xrange [0:%d]\n", len);
    fprintf(gp, "set yrange [%d:%d]\n", -V - 2, V + 2);
    fprintf(gp, "set grid\n");
    
    for (size_t i = 0; i < bits.length(); i++)
    {
        fprintf(gp, "set label '%c' at %zu.5,%d center\n", bits[i], i, V + 1);
    }
    
    fprintf(gp, "plot '%s' with lines linewidth 2\n", filename.c_str());
    pclose(gp);
}

void rzUnipolar(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    file << t << " " << 0 << endl;
    for (char bit : bits)
    {
        if (bit == '1')
        {
            file << t << " " << V << endl;
            file << t + 0.5 << " " << V << endl;
            file << t + 0.5 << " " << 0 << endl;
        }
        file << t + 1 << " " << 0 << endl;
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "RZ Unipolar", bits);
}

void nrzL(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int currentLevel = (bits[0] == '1') ? V : -V;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        int level = (bit == '1') ? V : -V;
        if (currentLevel != level)
            file << t << " " << level << endl;
        file << t + 1 << " " << level << endl;
        currentLevel = level;
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "NRZ-L", bits);
}

void nrzI(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int currentLevel = V;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        if (bit == '1')
            currentLevel = -currentLevel;
        file << t << " " << currentLevel << endl;
        file << t + 1 << " " << currentLevel << endl;
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "NRZ-I", bits);
}

void manchester(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int currentLevel = (bits[0] == '1') ? V : -V;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        int firstHalf = (bit == '1') ? V : -V;
        int secondHalf = (bit == '1') ? -V : V;
        if (currentLevel != firstHalf)
            file << t << " " << firstHalf << endl;
        file << t + 0.5 << " " << firstHalf << endl;
        file << t + 0.5 << " " << secondHalf << endl;
        file << t + 1 << " " << secondHalf << endl;
        currentLevel = secondHalf;
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "Manchester", bits);
}

void differentialManchester(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int currentLevel = V;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        if (bit == '0')
            currentLevel = -currentLevel;
        file << t << " " << currentLevel << endl;
        file << t + 0.5 << " " << currentLevel << endl;
        currentLevel = -currentLevel;
        file << t + 0.5 << " " << currentLevel << endl;
        file << t + 1 << " " << currentLevel << endl;
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "Differential Manchester", bits);
}

void ami(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int lastPulse = V;
    int currentLevel = 0;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        if (bit == '1')
        {
            lastPulse = -lastPulse;
            if (currentLevel != lastPulse)
                file << t << " " << lastPulse << endl;
            file << t + 1 << " " << lastPulse << endl;
            currentLevel = lastPulse;
        }
        else
        {
            if (currentLevel != 0)
                file << t << " " << 0 << endl;
            file << t + 1 << " " << 0 << endl;
            currentLevel = 0;
        }
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "AMI", bits);
}

void pseudoternary(const string &bits, int V)
{
    ofstream file("signal.dat");
    double t = 0.0;
    int lastPulse = V;
    int currentLevel = 0;
    file << t << " " << currentLevel << endl;
    for (char bit : bits)
    {
        if (bit == '0')
        {
            lastPulse = -lastPulse;
            if (currentLevel != lastPulse)
                file << t << " " << lastPulse << endl;
            file << t + 1 << " " << lastPulse << endl;
            currentLevel = lastPulse;
        }
        else
        {
            if (currentLevel != 0)
                file << t << " " << 0 << endl;
            file << t + 1 << " " << 0 << endl;
            currentLevel = 0;
        }
        t += 1;
    }
    file.close();
    plotSignal("signal.dat", V, bits.length(), "Pseudoternary", bits);
}

int main()
{
    int choice, V;
    string bits;

    cout << "Enter bit stream: ";
    cin >> bits;
    cout << "Enter voltage level: ";
    cin >> V;
    while (true)
    {
        cout << "\n===== Line Coding Schemes =====\n";
        cout << "1) RZ Unipolar\n";
        cout << "2) NRZ-L\n";
        cout << "3) NRZ-I\n";
        cout << "4) Manchester\n";
        cout << "5) Differential Manchester\n";
        cout << "6) AMI\n";
        cout << "7) Pseudoternary\n";
        cout << "8) Exit\n";
        cout << "Enter choice: ";
        cin >> choice;

        if (choice == 8)
        {
            cout << "Exiting...\n";
            break;
        }

        if (choice < 1 || choice > 7)
        {
            cout << "Invalid choice!\n";
            continue;
        }

        switch (choice)
        {
        case 1:
            rzUnipolar(bits, V);
            break;
        case 2:
            nrzL(bits, V);
            break;
        case 3:
            nrzI(bits, V);
            break;
        case 4:
            manchester(bits, V);
            break;
        case 5:
            differentialManchester(bits, V);
            break;
        case 6:
            ami(bits, V);
            break;
        case 7:
            pseudoternary(bits, V);
            break;
        }
    }

    return 0;
}
