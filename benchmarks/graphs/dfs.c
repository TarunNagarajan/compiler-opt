#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_NODES 1000

typedef struct Node {
    int id;
    struct Node* next;
} Node;

typedef struct Graph {
    int numNodes;
    Node* adjLists[MAX_NODES];
    bool visited[MAX_NODES];
} Graph;

Node* createNode(int id) {
    Node* newNode = malloc(sizeof(Node));
    newNode->id = id;
    newNode->next = NULL;
    return newNode;
}

Graph* createGraph(int nodes) {
    Graph* graph = malloc(sizeof(Graph));
    graph->numNodes = nodes;
    for (int i = 0; i < nodes; i++) {
        graph->adjLists[i] = NULL;
        graph->visited[i] = false;
    }
    return graph;
}

void addEdge(Graph* graph, int src, int dest) {
    Node* newNode = createNode(dest);
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;
}

void dfs(Graph* graph, int vertex) {
    graph->visited[vertex] = true;
    Node* adjList = graph->adjLists[vertex];
    Node* temp = adjList;

    while (temp != NULL) {
        int connectedVertex = temp->id;
        if (!graph->visited[connectedVertex]) {
            dfs(graph, connectedVertex);
        }
        temp = temp->next;
    }
}

int main() {
    int numNodes = 500;
    Graph* graph = createGraph(numNodes);

    for (int i = 0; i < numNodes; i++) {
        for (int j = 1; j <= 3; j++) {
            int dest = (i + j * 13) % numNodes;
            addEdge(graph, i, dest);
        }
    }

    for (int i = 0; i < 50; i++) {
        for (int j = 0; j < numNodes; j++) graph->visited[j] = false;
        dfs(graph, i % numNodes);
    }

    return 0;
}
