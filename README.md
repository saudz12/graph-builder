University Project: Graph Tools

This is a small project developed during the first semester of university. The goal was to learn Python, as it will be essential for future projects.

The repository includes three projects: Luxembourg, Graph Builder, and Rebrand.
Overview
Luxembourg

    Supports any type of graph, as long as the input follows the current XML format.
    Provides a base framework for testing different graph algorithms on a large scale. Dijkstra's and Bellman Ford's are currently implemented on it.

Graph Builder

    Generates weighted graphs based on a given number of nodes and edge density.
    Includes implementations of three algorithms for Minimum Spanning Tree (MST):
        Prim's Algorithm
        Kruskal's Algorithm
        Boruvka's Algorithm
    Uses matplotlib to create simple charts for visualizing results got from testing the algorithm's execution time on different sample size/density.

Rebrand

    Lets you draw your own flow network or weighted graph.
    Main supported functions: Add nodes and edges with different values for capacity and weight. Delete/remove created nodes and edges. Move nodes. Change graph type(directed/undirected). 
    Supports running algorithms directly on custom graphs. Available algorithms: Dfs, Bfs, find Conex Component, Kosaraju, topological sort, Kruskal's, Prim's, Boruvka's, Ford Fulkerson's max flow, min flow with Cycle Cancelling.

Notes

The project is a bit messy(it does not follow a specific pattern/architecture due to trying out new features in python), but it’s a solid starting point and a good learning experience.
