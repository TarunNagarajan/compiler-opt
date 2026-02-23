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

void bfs(Graph* graph, int startNode) {
    int queue[MAX_NODES];
    int front = 0;
    int rear = 0;

    graph->visited[startNode] = true;
    queue[rear++] = startNode;

    while (front < rear) {
        int currentNode = queue[front++];
        
        Node* temp = graph->adjLists[currentNode];
        while (temp) {
            int adjNode = temp->id;
            if (!graph->visited[adjNode]) {
                graph->visited[adjNode] = true;
                queue[rear++] = adjNode;
            }
            temp = temp->next;
        }
    }
}

int main() {
    int numNodes = 500;
    Graph* graph = createGraph(numNodes);

    // Create a random-ish graph
    for (int i = 0; i < numNodes; i++) {
        for (int j = 1; j <= 5; j++) {
            int dest = (i + j * 7) % numNodes;
            addEdge(graph, i, dest);
        }
    }

    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < numNodes; j++) graph->visited[j] = false;
        bfs(graph, i % numNodes);
    }

    return 0;
}
