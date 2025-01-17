import numpy as np
import heapq
import time

class Algorithms:
    def __init__(self, adjacency):
        self.graph = adjacency

    def alg_dijkstra(self, id_from, id_to):
        dist = [float('inf')] * len(self.graph)
        dist[id_from] = 0
        #print(min_dist, len(self.graph))
        prev_nodes = {}
        q = []

        heapq.heappush(q, (0, id_from))

        while len(q) != 0:
            d, u = heapq.heappop(q)

            if u == id_to:
                break

            for v, w in self.graph.get(u):
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev_nodes[v] = u
                    heapq.heappush(q, (alt, v))

        #print(prev_nodes)
        return prev_nodes

    def alg_bellman_ford(self, id_from, id_to):
        dist = [float('inf')] *  len(self.graph)
        dist[id_from] = 0
        prev_nodes = {}

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, w in self.graph[u]:
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev_nodes[v] = u

        # Check for negative weight cycles
        for u in self.graph:
            for v, w in self.graph[u]:
                if dist[u] + w < dist[v]:
                    raise ValueError("Graph contains a negative weight cycle")

        if id_to not in dist or dist[id_to] == float('inf'):
            raise ValueError(f"No path from {id_from} to {id_to}")

        return prev_nodes

    def alg_bellman_ford_numpy(self, id_from, id_to): #gpt help
        start_time = time.time()

        num_nodes = len(self.graph)

        # Initialize distances and previous nodes
        dist = np.full(num_nodes, np.inf, dtype=np.float64)
        dist[id_from] = 0
        prev_nodes = np.full(num_nodes, -1, dtype=np.int64)

        # Convert adjacency list to edge list for efficient processing
        edges = []
        for u in self.graph:
            for v, w in self.graph[u]:
                edges.append((u, v, w))
        edges = np.array(edges, dtype=np.int64)

        # Relax edges |V| - 1 times
        for iteration in range(num_nodes - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev_nodes[v] = u
                    #print(v, prev_nodes[v])
                    updated = True
            # If no updates in this iteration, we can stop early
            if not updated:
                break

        # Check for negative weight cycles involving reachable nodes
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                raise ValueError("Graph contains a negative weight cycle")

        # Ensure the target is reachable
        if dist[id_to] == np.inf:
            raise ValueError(f"No path from {id_from} to {id_to}")

        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")

        return prev_nodes.tolist()

class Node:
    def __init__(self, id, x, y, tkid):
        self.id = id
        self.x = x
        self.y = y
        self.tkid = tkid

class Edge:
    def __init__(self, from_x, from_y, to_x, to_y, line_id):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.line_id = line_id
