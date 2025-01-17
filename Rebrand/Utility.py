class Graph:
    def __init__(self, oriented):
       self.graph = {}
       self.nodes = []
       self.edges = {}
       self.oriented = oriented

    def add_edge(self, u, v, weight, capacity, line_id):
        self.graph.setdefault(u, []).append((v, weight, capacity))

        self.edges.setdefault((u, v), []).append((weight, capacity, line_id))

        if not self.oriented:
            self.graph.setdefault(v, []).append((u, weight, capacity))

            self.edges.setdefault((v, u), []).append((weight, capacity, line_id))
        #print(self.graph)

    def remove_connected(self, from_node, to_node):
        for edge in self.graph.get(from_node, []):
            if edge[0] == to_node:
                self.graph[from_node].remove(edge)

    def set_orientation(self, oriented):
        self.oriented = oriented

class DrawNode:
    def __init__(self, node_id, x, y, circle_id, text_id):
        self.id = node_id
        self.x = x
        self.y = y
        self.circle_id = circle_id
        self.text_id = text_id

class DrawEdge:
    def __init__(self, from_node_id, to_node_id, line_id, flux, capacity, flux_id):
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.line_text_id = line_id
        self.capacity = capacity
        self.flux = flux
        self.flux_text_id = flux_id