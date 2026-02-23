#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

#define MAX_NODES 200
#define INF INT_MAX

typedef struct Graph {
    int numNodes;
    int adjMatrix[MAX_NODES][MAX_NODES];
} Graph;

Graph* createGraph(int nodes) {
    Graph* graph = malloc(sizeof(Graph));
    graph->numNodes = nodes;
    for (int i = 0; i < nodes; i++) {
        for (int j = 0; j < nodes; j++) {
            graph->adjMatrix[i][j] = (i == j) ? 0 : INF;
        }
    }
    return graph;
}

void addEdge(Graph* graph, int src, int dest, int weight) {
    graph->adjMatrix[src][dest] = weight;
}

int minDistance(int dist[], bool sptSet[], int numNodes) {
    int min = INF, min_index;
    for (int v = 0; v < numNodes; v++) {
        if (sptSet[v] == false && dist[v] <= min) {
            min = dist[v], min_index = v;
        }
    }
    return min_index;
}

void dijkstra(Graph* graph, int src) {
    int dist[MAX_NODES];
    bool sptSet[MAX_NODES];

    for (int i = 0; i < graph->numNodes; i++) {
        dist[i] = INF, sptSet[i] = false;
    }

    dist[src] = 0;

    for (int count = 0; count < graph->numNodes - 1; count++) {
        int u = minDistance(dist, sptSet, graph->numNodes);
        sptSet[u] = true;

        for (int v = 0; v < graph->numNodes; v++) {
            if (!sptSet[v] && graph->adjMatrix[u][v] != INF && 
                dist[u] != INF && dist[u] + graph->adjMatrix[u][v] < dist[v]) {
                dist[v] = dist[u] + graph->adjMatrix[u][v];
            }
        }
    }
}

int main() {
    int numNodes = 150;
    Graph* graph = createGraph(numNodes);

    for (int i = 0; i < numNodes; i++) {
        for (int j = 1; j <= 4; j++) {
            int dest = (i + j * 17) % numNodes;
            addEdge(graph, i, dest, (i + j) % 10 + 1);
        }
    }

    for (int i = 0; i < 20; i++) {
        dijkstra(graph, i % numNodes);
    }

    return 0;
}
