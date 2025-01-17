import heapq

######################################################### Prim's Eager algorithm

def prim_mst(graph):
    mst = {}
    total_weight = 0

    min_heap = []
    best_weight = {}

    start_node = next(iter(graph))
    visited = set()

    heapq.heappush(min_heap, (0, start_node, None))

    while min_heap:
        weight, curr_node, parent = heapq.heappop(min_heap)

        if curr_node in visited:
            continue

        visited.add(curr_node)

        if parent is not None:
            mst.setdefault(parent, []).append((curr_node, weight))
            mst.setdefault(curr_node, []).append((parent, weight))
            total_weight += weight

        for n, w in graph.get(curr_node, []):
            if n not in visited:
                if n not in best_weight or w < best_weight[n][1]:
                    best_weight[n] = (curr_node, w)
                    heapq.heappush(min_heap, (w, n, curr_node))

    return mst

######################################################## Kruskal's algorithm

def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)

    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

def kruskal_mst(graph, nodes):
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            if (u, v, weight) not in edges and (v, u, weight) not in edges:
                edges.append((u, v, weight))

    edges.sort(key=lambda edge: edge[2])

    parent = {}
    rank = {}
    for vertex in nodes:
        parent[vertex] = vertex
        rank[vertex] = 0

    mst = {}
    total_weight = 0

    for u, v, weight in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)

        if root_u != root_v:
            mst.setdefault(u, [])
            mst[u].append((v, weight))
            total_weight += weight
            union(parent, rank, root_u, root_v)

    return mst

####################################################### Boruvka's algorithm

def boruvka_mst(graph, nodes):
    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}

    mst = {}
    total_weight = 0
    num_components = len(nodes)

    while num_components > 1:
        cheapest = {node: None for node in nodes}
        for u in graph:
            for v, weight in graph[u]:
                root_u = find(parent, u)
                root_v = find(parent, v)
                if root_u != root_v:
                    if cheapest[root_u] is None or weight < cheapest[root_u][2]:
                        cheapest[root_u] = (u, v, weight)
                    if cheapest[root_v] is None or weight < cheapest[root_v][2]:
                        cheapest[root_v] = (u, v, weight)

        for node in nodes:
            if cheapest[node] is not None:
                u, v, weight = cheapest[node]
                root_u = find(parent, u)
                root_v = find(parent, v)
                if root_u != root_v:
                    union(parent, rank, root_u, root_v)
                    mst.setdefault(u, [])
                    mst[u].append((v, weight))
                    total_weight += weight
                    num_components -= 1

    return mst