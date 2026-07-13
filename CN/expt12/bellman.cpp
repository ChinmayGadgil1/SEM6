#include <iostream>
#include <vector>
#include<tuple>
#include <climits>
using namespace std;

void bellman_ford(vector<tuple<int, int, int>>& graph, int vertices, int source) {
    
    // Step 1: Initialize distances
    vector<int> distance(vertices, INT_MAX);
    distance[source] = 0;
    
    cout << "\nInitial Routing Table" << endl;
    cout << "------------------------------------------------" << endl;
    
    for (int i = 0; i < vertices; i++) {
        if (distance[i] == INT_MAX)
            cout << "Router " << i << " --> INF" << endl;
        else
            cout << "Router " << i << " --> " << distance[i] << endl;
    }
    
    // Step 2: Relax edges repeatedly
    for (int iteration = 0; iteration < vertices - 1; iteration++) {
        
        cout << "\nIteration " << iteration + 1 << endl;
        cout << "------------------------------------------------" << endl;
        
        bool updated = false;
        
        for (auto& edge : graph) {
            int u = get<0>(edge);
            int v = get<1>(edge);
            int w = get<2>(edge);
            
            // Check for shorter path
            if (distance[u] != INT_MAX && distance[u] + w < distance[v]) {
                
                int old_distance = distance[v];
                distance[v] = distance[u] + w;
                updated = true;
                
                cout << "Updating Router " << v << endl;
                cout << "Path: Router " << u << " --> Router " << v << endl;
                cout << "Edge Cost = " << w << endl;
                cout << "Old Distance = " << (old_distance == INT_MAX ? -1 : old_distance) << endl;
                cout << "New Distance = " << distance[v] << endl << endl;
            }
        }
        
        // Show current routing table
        cout << "Routing Table After Iteration" << endl;
        cout << "--------------------------------" << endl;
        for (int i = 0; i < vertices; i++) {
            if (distance[i] == INT_MAX)
                cout << "Router " << i << " --> INF" << endl;
            else
                cout << "Router " << i << " --> " << distance[i] << endl;
        }
        
        if (!updated) {
            cout << "\nNo further updates possible." << endl;
            cout << "Shortest paths already found." << endl;
            break;
        }
    }
    
    // Step 3: Final Result
    cout << "\nFinal Routing Table" << endl;
    cout << "------------------------------------------------" << endl;
    cout << "Destination Router\tMinimum Distance" << endl;
    
    for (int i = 0; i < vertices; i++) {
        cout << i << "\t\t\t";
        if (distance[i] == INT_MAX)
            cout << "INF" << endl;
        else
            cout << distance[i] << endl;
    }
}

int main() {
    vector<tuple<int, int, int>> graph = {
        {0, 1, 6},
        {0, 2, 5},
        {0, 3, 5},
        {1, 4, -1},
        {2, 1, -2},
        {2, 4, 1},
        {3, 2, -2},
        {3, 5, -1},
        {4, 6, 3},
        {5, 6, 3}
    };
    
    int vertices = 7;
    int source = 0;
    
    bellman_ford(graph, vertices, source);
    
    return 0;
}