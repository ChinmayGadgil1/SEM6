#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <sstream>

using namespace std;

struct Subnet {
	string network;
	string broadcast;
	string mask;
	string firstHost;
	string lastHost;
	int totalHosts;
};

class IPv4Utils {
public:
	static unsigned int ipToInt(const string& ip) {
		unsigned int result = 0;
		int parts[4];
		sscanf(ip.c_str(), "%d.%d.%d.%d", &parts[0], &parts[1], &parts[2], &parts[3]);
		result = (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3];
		return result;
	}

	static string intToIp(unsigned int ip) {
		return to_string((ip >> 24) & 0xFF) + "." + to_string((ip >> 16) & 0xFF) + 
			   "." + to_string((ip >> 8) & 0xFF) + "." + to_string(ip & 0xFF);
	}

	static unsigned int getMask(int prefixLen) {
		return prefixLen == 0 ? 0 : (~0U << (32 - prefixLen));
	}
};

void flsm() {
	cout << "===== FLSM Subnetting =====" << endl;
	
	string networkInput;
	cout << "Enter Network Address (EX: 192.168.1.0/24): ";
	cin >> networkInput;
	
	size_t slashPos = networkInput.find('/');
	string networkAddr = networkInput.substr(0, slashPos);
	int prefixLen = stoi(networkInput.substr(slashPos + 1));
	
	int numSubnets;
	cout << "Enter Number of Required Subnets: ";
	cin >> numSubnets;
	
	int borrowedBits = ceil(log2(numSubnets));
	int newPrefix = prefixLen + borrowedBits;
	
	cout << "\nFLSM Subnet Details" << endl;
	cout << "===================" << endl;
	
	unsigned int baseIp = IPv4Utils::ipToInt(networkAddr);
	unsigned int subnetSize = 1 << (32 - newPrefix);
	
	for (int i = 0; i < numSubnets; i++) {
		unsigned int subnetIp = baseIp + (i * subnetSize);
		unsigned int mask = IPv4Utils::getMask(newPrefix);
		unsigned int broadcast = subnetIp | (~mask);
		unsigned int firstHost = subnetIp + 1;
		unsigned int lastHost = broadcast - 1;
		int totalHosts = subnetSize - 2;
		
		cout << "Subnet " << (i + 1) << endl;
		cout << "Network Address : " << IPv4Utils::intToIp(subnetIp) << endl;
		cout << "Broadcast Address : " << IPv4Utils::intToIp(broadcast) << endl;
		cout << "Subnet Mask : " << IPv4Utils::intToIp(mask) << endl;
		
		if (totalHosts > 0) {
			cout << "First Host : " << IPv4Utils::intToIp(firstHost) << endl;
			cout << "Last Host : " << IPv4Utils::intToIp(lastHost) << endl;
			cout << "Total Hosts : " << totalHosts << endl;
		} else {
			cout << "No usable hosts" << endl;
		}
		cout << endl;
	}
}

void vlsm() {
	cout << "===== VLSM Subnetting =====" << endl;
	
	string baseNetworkInput;
	cout << "Enter Base Network (EX: 192.168.10.0/24): ";
	cin >> baseNetworkInput;
	
	size_t slashPos = baseNetworkInput.find('/');
	string networkAddr = baseNetworkInput.substr(0, slashPos);
	int prefixLen = stoi(baseNetworkInput.substr(slashPos + 1));
	
	int numDepartments;
	cout << "Enter Number of Subnets: ";
	cin >> numDepartments;
	
	vector<pair<string, int>> requirements;
	
	for (int i = 0; i < numDepartments; i++) {
		string dept;
		int hosts;
		cout << "Enter Subnet Name " << (i + 1) << ": ";
		cin >> dept;
		cout << "Enter Required Hosts for " << dept << ": ";
		cin >> hosts;
		requirements.push_back({dept, hosts});
	}
	
	sort(requirements.begin(), requirements.end(), 
		 [](const pair<string, int>& a, const pair<string, int>& b) {
			 return a.second > b.second;
		 });
	
	unsigned int currentIp = IPv4Utils::ipToInt(networkAddr);
	
	cout << "\nVLSM Subnet Details" << endl;
	cout << "===================" << endl;
	
	for (auto& req : requirements) {
		string dept = req.first;
		int hostsNeeded = req.second;
		int totalNeeded = hostsNeeded + 2;
		int subnetBits = ceil(log2(totalNeeded));
		int prefix = 32 - subnetBits;
		unsigned int mask = IPv4Utils::getMask(prefix);
		unsigned int broadcast = currentIp | (~mask);
		unsigned int firstHost = currentIp + 1;
		unsigned int lastHost = broadcast - 1;
		int availableHosts = (1 << subnetBits) - 2;
		
		cout << "Subnet : " << dept << endl;
		cout << "Required Hosts : " << hostsNeeded << endl;
		cout << "Subnet : " << IPv4Utils::intToIp(currentIp) << "/" << prefix << endl;
		cout << "Subnet Mask : " << IPv4Utils::intToIp(mask) << endl;
		cout << "Network Address : " << IPv4Utils::intToIp(currentIp) << endl;
		cout << "Broadcast Address : " << IPv4Utils::intToIp(broadcast) << endl;
		
		if (availableHosts > 0) {
			cout << "First Host : " << IPv4Utils::intToIp(firstHost) << endl;
			cout << "Last Host : " << IPv4Utils::intToIp(lastHost) << endl;
			cout << "Available Hosts : " << availableHosts << endl;
		} else {
			cout << "No usable hosts" << endl;
		}
		cout << endl;
		
		currentIp += (1 << subnetBits);
	}
}

int main() {
	int choice;
	
	while (true) {
		cout << "============================" << endl;
		cout << " FLSM and VLSM Calculator" << endl;
		cout << "============================" << endl;
		cout << "1. Fixed Length Subnet Masking (FLSM)" << endl;
		cout << "2. Variable Length Subnet Masking (VLSM)" << endl;
		cout << "3. Exit" << endl;
		cout << "Enter Your Choice: ";
		cin >> choice;
		
		if (choice == 1) {
			flsm();
		} else if (choice == 2) {
			vlsm();
		} else if (choice == 3) {
			cout << "Exiting Program..." << endl;
			break;
		} else {
			cout << "Invalid Choice! Please Try Again." << endl;
		}
	}
	
	return 0;
}
