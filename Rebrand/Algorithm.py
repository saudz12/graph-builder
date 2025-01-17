from collections import deque
import heapq
from xmlrpc.client import MAXINT
from collections import defaultdict
from typing import Dict, List, Tuple

from numpy.f2py.crackfortran import param_eval


######################################################### DEPTH FIRST SEARCH

def iterative_dfs(graph, start_id):
    visited = {}
    s = [start_id]
    result = []

    while s:
        node_id = s.pop()
        if node_id in visited:
            continue

        visited[node_id] = True
        result.append(node_id)

        for neighbor in reversed(graph.get(node_id, [])):
            # print(neighbor, '\n')
            s.append(neighbor[0])

    print(result)
    return result

######################################################### RECURSIVE DFS

def recursive_dfs(graph, node_id, visited, finds):
    visited[node_id] = True
    finds.append(node_id)
    #print(node_id)
    for neighbour in graph.get(node_id, []):
        print(neighbour)
        if neighbour[0] not in visited:
            recursive_dfs(graph, neighbour[0], visited, finds)

######################################################### BREADTH FIRST SEARCH

def bfs(graph, start_id):
    visited = {}
    visited[start_id] = True
    q = deque([start_id])
    result = [start_id]

    while q:
        node_id = q.popleft()

        for neighbour in graph.get(node_id, []):
            nid = neighbour[0]

            if nid in visited:
                continue

            q.append(neighbour[0])
            result.append(neighbour[0])
            visited[neighbour[0]] = True

    return result

######################################################### CONNECTED COMPONENTS - ONLY UNORDERED GRAPHS

def cc(graph, nodes):
    visited = {}

    conex = []

    for node_id in nodes:
        if node_id in visited:
            continue
        curr_comp = [node_id]

        stack = [node_id]

        while stack:
            node_id = stack.pop()
            curr_comp.append(node_id)
            if node_id not in visited:
                visited[node_id] = True

                for neighbor in graph.get(node_id, []):
                        if neighbor[0] not in visited:
                            stack.append(neighbor[0])
        conex.append(curr_comp)

    return conex

######################################################### KOSARAJU's STRONGLY CONNECTED COMPONENTS

def dfs_on_graph(t_g, curr_node, visited, component):
    visited[curr_node] = True
    component.append(curr_node)

    #print(curr_node)
    for neighbour in t_g.get(curr_node, []):
        #print(neighbour)
        if neighbour[0] not in visited:
            print(neighbour[0])
            dfs_on_graph(t_g, neighbour[0], visited, component)

def dfs_simple(graph, curr_node, visited, stack):
    visited[curr_node] = True

    for neighbour in graph.get(curr_node, []):
        if neighbour[0] not in visited:
            dfs_simple(graph, neighbour[0], visited, stack)

    #print(curr_node)
    stack.append(curr_node)

def scc_kosaraju(graph, nodes):
    stack = []
    visited = {}

    print(graph)
    for node_id in nodes:
        if node_id not in visited:
            dfs_simple(graph, node_id, visited, stack)

    #print(self.graph.graph)

    g_t = {}

    for key in graph:
        for val in graph[key]:
            if val[0] not in g_t:
                g_t[val[0]] = [[key, val[1]]]
            elif key not in g_t[val[0]]:
                g_t[val[0]].append([key, val[1]])

    #print(g_t)

    visited = {}
    scc_list = []

    #print(stack)

    while stack:
        curr = stack.pop()
        #print(curr)
        if curr not in visited:
            component = []
            dfs_on_graph(g_t, curr, visited, component)
            scc_list.append(component)

    #print(scc_list)

    return  scc_list

######################################################### TOPOLOGICAL SORT

def ts_builder(node_id, graph, visited, visiting, result):
    global has_cycle
    if node_id in visiting:
        has_cycle = True
        return
    if node_id in visited:
        return

    visiting.add(node_id)
    for neighbor, _, _ in graph.get(node_id, []):
        ts_builder(neighbor, graph, visited, visiting, result)
    visiting.remove(node_id)
    visited.add(node_id)
    result.append(node_id)

def ts(graph):
    visited = set()
    visiting = set()
    result = []
    global has_cycle
    has_cycle = False

    for node in graph:
        if node not in visited:
            ts_builder(node, graph, visited, visiting, result)
            if has_cycle:
                print("The graph has cycles")
                return []
    return result[::-1]

######################################################### Center Node

def find_center(graph):

    tree = {}

    for node_id in graph:
        tree[node_id] = []
        for edge in graph.get(node_id, []):
            tree[node_id].append(edge[0])

    print(tree)


    print(graph)
    print(tree)

    changes = True
    while changes:
        changes = False
        stack = []
        min_connections = MAXINT

        for key in tree:
            if len(tree[key]) < min_connections:
                while stack:
                    stack.pop()
                min_connections = len(tree[key])

            if len(tree[key]) == min_connections:
                stack.append(key)

        if len(stack) != len(tree):
            changes = True

            print(stack)

            for key in stack:
                for node in tree:
                    remove_edge = []
                    if node in stack:
                        continue

                    print(node, ": ")
                    print("Before remove: ", tree[node])
                    for edge in tree.get(node):
                        if edge== key:
                            print(edge, "- to delete")
                            remove_edge.append(edge)

                    print("Will remove: ", remove_edge)

                    for edge in remove_edge:
                        print(edge)
                        tree[node].remove(edge)

                    print("After remove: ", tree[node])
                tree.pop(key)

        print(tree)

    center = next(iter(tree))

    print(center)

    return center

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

        for n, w, _ in graph.get(curr_node, []):
            if n not in visited:
                if n not in best_weight or w < best_weight[n][1]:
                    best_weight[n] = (curr_node, w)
                    heapq.heappush(min_heap, (w, n, curr_node))

    #print(mst.graph)
    print(total_weight)
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
        for v, weight, _ in graph[u]:
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

    print(mst)

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
            for v, weight, _ in graph[u]:
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

    print(total_weight)
    return mst

####################################################### Dijkstra's algorithm

####################################################### Bellman Ford's algorithm

####################################################### Ford Fulkerson's's algorithm

# def residual_bfs(graph, s, t, parent):
#     visited = set()
#     que = deque()
#     que.append(s)
#     visited.add(s)
#     parent[s] = -1
#
#     while que:
#         u = que.popleft()
#         for node_id in graph.get(u, {}):
#             flow, capacity = graph[u][node_id]
#             if node_id not in visited and capacity - flow > 0:
#                 que.append(node_id)
#                 visited.add(node_id)
#                 parent[node_id] = u
#                 if node_id == t:
#                     return  True
#
#     return False
#
# def ford_fulkerson(graph, nodes, source, sink):
#     max_flow = 0
#
#     r_g = {}
#     for node in graph:
#         r_g.setdefault(node, {})
#         for v, f, c in graph.get(node, []):
#             r_g[node][v] = [0, c]
#             if v not in r_g:
#                 r_g.setdefault(v, {})
#             r_g[v][node] = [0, 0]
#
#     for node in r_g:
#         print(node, ':', r_g[node])
#
#     parent = {node : -1 for node in nodes}
#
#     print(parent)
#
#     while residual_bfs(r_g, source, sink, parent):
#         tail = sink
#         flow = float('inf')
#         while tail != source:
#             flow = min(flow, r_g[parent[tail]][tail][1] - r_g[parent[tail]][tail][0])
#             tail = parent[tail]
#
#         tail = sink
#         while tail != source:
#             r_g[parent[tail]][tail][0] += flow
#             r_g[tail][parent[tail]][0] -= flow
#             tail = parent[tail]
#
#     for node in r_g:
#         print(node, ':', r_g[node])
#
#     print(parent)
#
#     for node in r_g[source]:
#         max_flow += r_g[source][node][0]
#
#     #print(max_flow)
#
#     return max_flow, parent, r_g

def residual_bfs(graph, s, t, parent):
    visited = set()
    que = deque()
    que.append(s)
    visited.add(s)
    parent[s] = -1

    while que:
        u = que.popleft()
        for node_id in graph.get(u, {}):
            flow = graph[u][node_id]
            if node_id not in visited and flow > 0:
                que.append(node_id)
                visited.add(node_id)
                parent[node_id] = u
                if node_id == t:
                    return  True

    return False

def ford_fulkerson(graph, nodes, source, sink):
    max_flow = 0

    r_g = {}
    for node in graph:
        r_g.setdefault(node, {})
        for v, f, c in graph.get(node, []):
            r_g[node][v] = c
            if v not in r_g:
                r_g.setdefault(v, {})
            r_g[v][node] = 0

    for node in r_g:
        print(node, ':', r_g[node])

    parent = {node : -1 for node in nodes}

    print(parent)

    while residual_bfs(r_g, source, sink, parent):
        tail = sink
        flow = float('inf')
        while tail != source:
            flow = min(flow, r_g[parent[tail]][tail])
            tail = parent[tail]

        tail = sink
        max_flow += flow

        while tail != source:
            r_g[parent[tail]][tail] -= flow
            r_g[tail][parent[tail]] += flow
            tail = parent[tail]

    for node in r_g:
        print(node, ':', r_g[node])

    print(parent)

    # for node in r_g[source]:
    #     max_flow += r_g[source][node]
    #print(max_flow) #???? ikd anymore there are 3 DIFFERENT WAYS TO DO THIS AND ALL SEEM TO WORK DIFF AND I M NOT TALKING ABOUT FF and FW

    return max_flow, parent, r_g

####################################################### Min Flow Cycle Cancelling WITH strong typing as I'm tired

def bellman_ford(graph: Dict[int, List[Tuple]], source: int, n: int, residual_graph: Dict[int, List[Tuple]]) -> Tuple[
    bool, Dict[int, float]]:

    distances = {i: float('inf') for i in range(n)}
    distances[source] = 0
    predecessor = {i: None for i in range(n)}

    for _ in range(n - 1):
        for u in residual_graph:
            for v, flux, capacity, weight in residual_graph[u]:
                if distances[u] + weight < distances[v] and flux < capacity:
                    distances[v] = distances[u] + weight
                    predecessor[v] = u

    for u in residual_graph:
        for v, flux, capacity, weight in residual_graph[u]:
            if distances[u] + weight < distances[v] and flux < capacity:
                return True, predecessor

    return False, predecessor


def find_negative_cycle(graph: Dict[int, List[Tuple]], n: int, residual_graph: Dict[int, List[Tuple]]) -> List[int]:
    has_negative_cycle, predecessor = bellman_ford(graph, 0, n, residual_graph)

    if not has_negative_cycle:
        return []

    visited = set()
    curr = 0
    while curr not in visited:
        visited.add(curr)
        curr = predecessor[curr]

    cycle = []
    start = curr
    cycle.append(start)
    curr = predecessor[start]
    while curr != start:
        cycle.append(curr)
        curr = predecessor[curr]
    cycle.append(start)

    return cycle[::-1]


def find_residual_capacity(cycle: List[int], residual_graph: Dict[int, List[Tuple]]) -> float:
    min_capacity = float('inf')

    for i in range(len(cycle) - 1):
        u = cycle[i]
        v = cycle[i + 1]

        for to_node, flux, capacity, weight in residual_graph[u]:
            if to_node == v:
                residual_cap = capacity - flux
                min_capacity = min(min_capacity, residual_cap)
                break

    return min_capacity


def create_residual_graph(graph: Dict[int, List[Tuple]]) -> Dict[int, List[Tuple]]:
    residual_graph = defaultdict(list)

    for u in graph:
        for v, weight, capacity in graph[u]:
            residual_graph[u].append((v, 0, capacity, weight))
            residual_graph[v].append((u, 0, 0, -weight))

    return residual_graph


def cycle_canceling(graph: Dict[int, List[Tuple]], source: int, sink: int) -> Dict[int, List[Tuple]]:
    n = max(max(graph.keys()), max(v for edges in graph.values() for v, _, _ in edges)) + 1

    residual_graph = create_residual_graph(graph)

    def dijkstra(source: int, sink: int) -> Tuple[bool, List[int]]:
        distances = {i: float('inf') for i in range(n)}
        distances[source] = 0
        predecessor = {i: None for i in range(n)}
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > distances[u]:
                continue

            for v, flux, capacity, weight in residual_graph[u]:
                if flux < capacity and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessor[v] = u
                    heapq.heappush(pq, (distances[v], v))

        if distances[sink] == float('inf'):
            return False, []

        path = []
        curr = sink
        while curr is not None:
            path.append(curr)
            curr = predecessor[curr]
        return True, path[::-1]

    while True:
        has_path, path = dijkstra(source, sink)
        if not has_path:
            break

        min_capacity = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            for to_node, flux, capacity, weight in residual_graph[u]:
                if to_node == v:
                    residual_cap = capacity - flux
                    min_capacity = min(min_capacity, residual_cap)
                    break

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            for j, (to_node, flux, capacity, weight) in enumerate(residual_graph[u]):
                if to_node == v:
                    residual_graph[u][j] = (to_node, flux + min_capacity, capacity, weight)
                    break
            for j, (to_node, flux, capacity, weight) in enumerate(residual_graph[v]):
                if to_node == u:
                    residual_graph[v][j] = (to_node, flux + min_capacity, capacity, weight)
                    break

    while True:
        cycle = find_negative_cycle(graph, n, residual_graph)
        if not cycle:
            break

        min_capacity = find_residual_capacity(cycle, residual_graph)

        for i in range(len(cycle) - 1):
            u = cycle[i]
            v = cycle[i + 1]
            for j, (to_node, flux, capacity, weight) in enumerate(residual_graph[u]):
                if to_node == v:
                    residual_graph[u][j] = (to_node, flux + min_capacity, capacity, weight)
                    break
            for j, (to_node, flux, capacity, weight) in enumerate(residual_graph[v]):
                if to_node == u:
                    residual_graph[v][j] = (to_node, flux + min_capacity, capacity, weight)
                    break

    result = defaultdict(list)
    for u in residual_graph:
        for v, flux, capacity, weight in residual_graph[u]:
            if capacity > 0:
                result[u].append((v, flux, capacity, weight))

    return dict(result)


def min_flow_cycle_canceling(graph: Dict[int, List[Tuple]], source: int, sink: int) -> Dict[int, List[Tuple]]:
    negated_graph = defaultdict(list)
    for u in graph:
        for v, weight, capacity in graph[u]:
            negated_graph[u].append((v, -weight, capacity))

    result = cycle_canceling(dict(negated_graph), source, sink)

    final_result = defaultdict(list)
    for u in result:
        for v, flux, capacity, weight in result[u]:
            final_result[u].append((v, flux, capacity, -weight))

    return dict(final_result)