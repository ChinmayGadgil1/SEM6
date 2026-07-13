#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

typedef pair<int, int> pii;
typedef unordered_map<int, vector<pii>> Graph;

void dijkstra(Graph& graph, int start) {
    unordered_map<int, int> distances;
    
    // Step 1: Initialize distances
    for (auto& node : graph) {
        distances[node.first] = INT_MAX;
    }
    distances[start] = 0;
    
    priority_queue<pii, vector<pii>, greater<pii>> pq;
    unordered_set<int> visited;
    
    pq.push({0, start});
    
    cout << "\nInitial Routing Table" << endl;
    cout << "------------------------------------------------" << endl;
    for (auto& node : distances) {
        cout << "Router " << node.first << " --> " << node.second << endl;
    }
    
    // Step 2: Process routers
    while (!pq.empty()) {
        int current_distance = pq.top().first;
        int current_router = pq.top().second;
        pq.pop();
        
        if (visited.count(current_router)) {
            continue;
        }
        visited.insert(current_router);
        
        cout << "\nProcessing Router " << current_router << endl;
        cout << "------------------------------------------------" << endl;
        
        for (auto& edge : graph[current_router]) {
            int neighbor = edge.first;
            int weight = edge.second;
            
            cout << "Checking Path:" << endl;
            cout << current_router << " --> " << neighbor << endl;
            cout << "Link Cost = " << weight << endl;
            
            int new_distance = current_distance + weight;
            
            if (new_distance < distances[neighbor]) {
                int old_distance = distances[neighbor];
                distances[neighbor] = new_distance;
                
                cout << "Updating Router " << neighbor << endl;
                cout << "Old Distance = " << old_distance << endl;
                cout << "New Distance = " << new_distance << endl;
                
                pq.push({new_distance, neighbor});
            } else {
                cout << "No Update Required" << endl;
            }
            cout << endl;
        }
        
        cout << "Routing Table After Processing" << endl;
        cout << "------------------------------------------------" << endl;
        for (auto& node : distances) {
            cout << "Router " << node.first << " --> " << node.second << endl;
        }
    }
    
    // Step 3: Final Shortest Path Table
    cout << "\nFinal Shortest Path Table" << endl;
    cout << "------------------------------------------------" << endl;
    cout << "Destination Router\tShortest Distance" << endl;
    for (auto& node : distances) {
        cout << node.first << "\t\t\t" << node.second << endl;
    }
}

int main() {
    Graph graph;
    
    graph[0] = {{1, 4}, {2, 2}};
    graph[1] = {{0, 4}, {2, 1}, {3, 5}};
    graph[2] = {{0, 2}, {1, 1}, {3, 8}, {4, 10}};
    graph[3] = {{1, 5}, {2, 8}, {4, 2}, {5, 6}};
    graph[4] = {{2, 10}, {3, 2}, {5, 3}};
    graph[5] = {{3, 6}, {4, 3}};
    
    int start = 0;
    dijkstra(graph, start);
    
    return 0;
}