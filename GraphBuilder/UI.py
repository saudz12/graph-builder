import tkinter as tk
import math

import Controls
import Models
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import random
import time

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Algorithms Visualization")

        # Mode and other settings
        self.mode = tk.StringVar(value="move_node")

        # Algorithm selection
        self.algorithm = tk.StringVar(value="Prim")

        # Starting node selection
        self.start_node = tk.IntVar()

        # Node Counter
        self.node_counter = 0

        self.is_oriented = False

        self.nodes = {}
        self.edges = []
        self.graph = Models.Graph(self.is_oriented)
        self.reusable_ids = []

        self.r = 20

        self.main_frame = None
        self.canvas = None
        self.density_text = None
        self.nr_of_nodes_text = None

        self.start_node_menu = None

        # For moving nodes

        self.selected_node_id = None
        self.dragging = False

        # For edge drawing

        self.edge_start_node = None

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas

        self.canvas = tk.Canvas(self.main_frame, bg="white", width=300, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Modes

        modes_frame = tk.LabelFrame(control_frame, text="Mode")
        modes_frame.pack(pady=10)

        tk.Radiobutton(modes_frame, text="Move Nodes", variable=self.mode, value="move_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Delete Nodes", variable=self.mode, value="delete_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Delete Edges", variable=self.mode, value="delete_edge").pack(anchor=tk.W)

        # textbox

        nr_of_nodes_frame = tk.LabelFrame(control_frame, text="Nr of Nodes")
        nr_of_nodes_frame.pack(pady=10)
        self.nr_of_nodes_text = tk.Entry(nr_of_nodes_frame)
        self.nr_of_nodes_text.insert(0, "0")
        self.nr_of_nodes_text.pack(pady=5)

        density_frame = tk.LabelFrame(control_frame, text="Density")
        density_frame.pack(pady=10)
        self.density_text = tk.Entry(density_frame)
        self.density_text.insert(0, "0")
        self.density_text.pack(pady=5)

        # Algorithm selection

        alg_frame = tk.LabelFrame(control_frame, text="Algorithm")
        alg_frame.pack(pady=10)
        algorithms = ["Prim", "Kruskal", "Boruvka"]
        alg_menu = tk.OptionMenu(alg_frame, self.algorithm, self.algorithm.get(), *algorithms)
        alg_menu.pack()

        # Starting node selection

        start_node_frame = tk.LabelFrame(control_frame, text="Start Node")
        start_node_frame.pack(pady=10)
        self.start_node_menu = tk.OptionMenu(start_node_frame, self.start_node, None)
        self.start_node_menu.pack()

        # Generate button

        test_button = tk.Button(control_frame, text="Run Tests", command=self.run_tests)
        test_button.pack(pady=10)

        # Generate button

        generate_button = tk.Button(control_frame, text="Generate", command=self.generate_graph)
        generate_button.pack(pady=10)

        # Run button

        run_button = tk.Button(control_frame, text="Run", command=self.run_algorithm)
        run_button.pack(pady=10)

        # Clear Canvas button

        reset_button = tk.Button(control_frame, text="Reset Everything", command=self.clear_everything)
        reset_button.pack(pady=10)

        # Bind events

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)

    def toggle_orientation(self):
        print(self.is_oriented.get())
        print(self.graph.graph)
        if self.nodes or self.edges:
            self.clear_everything()

        self.graph.set_orientation(self.is_oriented.get())

    def canvas_click(self, event):
        if self.mode.get() == "draw_node":
            self.add_node(event.x, event.y)
        elif self.mode.get() == "draw_edge":
            self.select_edge_node(event.x, event.y)
        elif self.mode.get() == "move_node":
            self.start_move_node(event.x, event.y)
        elif self.mode.get() == "delete_node":
            node_id = self.get_node_at_position(event.x, event.y)
            if node_id is not None:
                self.delete_node(node_id)
        elif self.mode.get() == "delete_edge":
            self.delete_edge(event.x, event.y)

    def add_node(self, x, y):
        if self.reusable_ids:
            node_id = self.reusable_ids.pop(0)
        else:
            node_id = self.node_counter
            self.node_counter += 1
        self.r = 20 # radius
        circle_id = self.canvas.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill="lightblue")
        text_id = self.canvas.create_text(x, y, text=str(node_id), font=12)

        node = Models.DrawNode(node_id, x, y, circle_id, text_id)
        self.nodes[node_id] = node
        self.graph.nodes.append(node_id)
        print(self.graph.nodes)

        # Update start node menu

        self.update_start_node_menu()
        #print(self.nodes)
        print(self.graph.graph.keys())

    def select_edge_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id is not None:
            if self.edge_start_node is None:
                self.edge_start_node = node_id
                # Highlight the node
                self.canvas.itemconfig(self.nodes[node_id].circle_id, outline="red", width=2)
            elif node_id == self.edge_start_node:
                self.canvas.itemconfig(self.nodes[node_id].circle_id, outline="black", width=1)
                self.edge_start_node = None
            else:
                from_node_id = self.edge_start_node
                to_node_id = node_id
                if from_node_id == to_node_id:
                    return
                self.add_edge(from_node_id, to_node_id)
                # Remove highlight
                self.canvas.itemconfig(self.nodes[from_node_id].circle_id, outline="black", width=1)
                self.edge_start_node = None
        else:
            if self.edge_start_node is not None:
                self.canvas.itemconfig(self.nodes[self.edge_start_node].circle_id, outline="black", width=1)
                self.edge_start_node = None

    def get_node_at_position(self, x, y):
        overlapping = self.canvas.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        for item in overlapping:
            for node_id, node in self.nodes.items():
                if item == node.circle_id or item == node.text_id:
                    return node_id
        return None

    def delete_node(self, node_id):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            self.canvas.delete(node.circle_id)
            self.canvas.delete(node.text_id)

            self.reusable_ids.append(node_id)
            self.reusable_ids.sort()

            edges_to_delete = [edge for edge in self.edges if edge.from_node_id == node_id or edge.to_node_id == node_id]

            for edge in edges_to_delete:
                if edge.flux_text_id:
                    self.canvas.delete(edge.flux_text_id)
                self.canvas.delete(edge.line_text_id)
                self.edges.remove(edge)

            self.graph.graph.pop(node_id, None)
            self.graph.nodes.remove(node_id)

            #print(self.graph.graph.values())
            for neighbors in self.graph.graph.values():
                neighbors[:] = [(v, f, c) for v, f, c in neighbors if v != node_id]
            print(self.graph.nodes)

            del self.nodes[node_id]

            self.update_start_node_menu()
            #print(self.nodes)
            print(self.graph.graph.keys())

    def add_edge(self, from_node_id, to_node_id, weight):
        for edge in self.edges:
            if edge.from_node_id == from_node_id and edge.to_node_id == to_node_id:
                return  # Edge already exists

            if not self.is_oriented and edge.from_node_id == to_node_id and edge.to_node_id == from_node_id:
                return  # Edge already exists in undirected graph

        line_id, weight_text_id = self.paint_edge(from_node_id, to_node_id, weight)

        edge = Models.DrawEdge(from_node_id, to_node_id, line_id, weight, weight_text_id)
        edge.weight = weight
        #edge.weight_text_id = weight_text_id
        self.edges.append(edge)

        self.graph.add_edge(from_node_id, to_node_id, weight, line_id)

        print(self.graph.graph)
        print(self.edges)

    def paint_edge(self, from_node_id, to_node_id, weight):
        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]

        line_id = self.canvas.create_line(from_node.x, from_node.y, to_node.x, to_node.y)
        weight_text_id = self.canvas.create_text((from_node.x + to_node.x) / 2, (from_node.y + to_node.y) / 2,
                                                 text=str(weight))

        return line_id, weight_text_id

    def delete_edge(self, x, y):
        closest_edge = None
        min_distance = float('inf')

        for edge in self.edges:
            from_node = self.nodes[edge.from_node_id]
            to_node = self.nodes[edge.to_node_id]

            distance = self.distance_to_line(x, y, from_node.x, from_node.y, to_node.x, to_node.y)
            if distance < min_distance and distance < 10:
                min_distance = distance
                closest_edge = edge

        if closest_edge:
            self.canvas.delete(closest_edge.line_text_id)
            self.canvas.delete(closest_edge.flux_text_id)
            self.edges.remove(closest_edge)
            print(self.graph.graph)
            print(self.graph.graph[closest_edge.from_node_id])

            self.graph.remove_connected(closest_edge.from_node_id, closest_edge.to_node_id)

            if not self.is_oriented:
                self.graph.remove_connected(closest_edge.to_node_id, closest_edge.from_node_id)

    def distance_to_line(self, px, py, x1, y1, x2, y2):
        line_mag = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if line_mag < 0.000001:
            return float('inf')

        u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
        if u < 0 or u > 1:
            dist1 = math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
            dist2 = math.sqrt((px - x2) ** 2 + (py - y2) ** 2)
            return min(dist1, dist2)
        else:
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            return math.sqrt((px - ix) ** 2 + (py - iy) ** 2)

    def start_move_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id is not None:
            self.selected_node_id = node_id
            self.dragging = True

    def canvas_drag(self, event):
        if self.mode.get() == "move_node" and self.dragging and self.selected_node_id is not None:
            node = self.nodes[self.selected_node_id]
            dx = event.x - node.x
            dy = event.y - node.y
            self.canvas.move(node.circle_id, dx, dy)
            self.canvas.move(node.text_id, dx, dy)
            node.x = event.x
            node.y = event.y

            # Update all edges connected to this node
            for edge in self.edges:
                if edge.from_node_id == self.selected_node_id or edge.to_node_id == self.selected_node_id:
                    # Update edge coordinates
                    from_node = self.nodes[edge.from_node_id]
                    to_node = self.nodes[edge.to_node_id]
                    self.canvas.coords(edge.line_text_id, from_node.x, from_node.y, to_node.x, to_node.y)
                    #edge.line_id
                    # Update weight label position
                    weight = edge.weight

                    weight_x = (from_node.x + to_node.x) / 2
                    weight_y = (from_node.y + to_node.y) / 2
                    self.canvas.coords(edge.flux_text_id, weight_x, weight_y)

            # Redraw canvas to reflect the updates
            self.canvas.update()

    def canvas_release(self, event):
        if self.mode.get() == "move_node" and self.dragging:
            self.dragging = False
            self.selected_node_id = None

    def update_edges(self, node_id):
        for edge in self.edges:
            if edge.from_node_id == node_id or edge.to_node_id == node_id:
                from_node = self.nodes[edge.from_node_id]
                to_node = self.nodes[edge.to_node_id]
                self.canvas.coords(edge.line_text_id, from_node.x, from_node.y, to_node.x, to_node.y)

    def run_tests(self):
        results = {
            "Prim": [],
            "Kruskal": [],
            "Boruvka": []
        }
        #thing
        sample_size = 10
        sample_density = .20
        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.prim_mst(graph)
        elapsed_time = time.time() - start_time

        results["Prim"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.kruskal_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Kruskal"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.boruvka_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Boruvka"].append((sample_size, elapsed_time))

        # thing
        sample_size = 20
        sample_density = .20
        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.prim_mst(graph)
        elapsed_time = time.time() - start_time

        results["Prim"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.kruskal_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Kruskal"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.boruvka_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Boruvka"].append((sample_size, elapsed_time))

        # thing
        sample_size = 40
        sample_density = .20
        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.prim_mst(graph)
        elapsed_time = time.time() - start_time

        results["Prim"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.kruskal_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Kruskal"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.boruvka_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Boruvka"].append((sample_size, elapsed_time))

        # thing
        sample_size = 80
        sample_density = .20
        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.prim_mst(graph)
        elapsed_time = time.time() - start_time

        results["Prim"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.kruskal_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Kruskal"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.boruvka_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Boruvka"].append((sample_size, elapsed_time))

        # thing
        sample_size = 160
        sample_density = .20
        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.prim_mst(graph)
        elapsed_time = time.time() - start_time

        results["Prim"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.kruskal_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Kruskal"].append((sample_size, elapsed_time))

        graph = self.generate_random_graph(sample_size, sample_density)
        start_time = time.time()
        Controls.boruvka_mst(graph, sorted(graph.keys()))
        elapsed_time = time.time() - start_time

        results["Boruvka"].append((sample_size, elapsed_time))

        self.plot_performance_comparison(results)

    def generate_graph(self):
        self.clear_everything()
        print("generating...")
        num_nodes = int(self.nr_of_nodes_text.get()) or -1
        density = float(self.density_text.get()) or -1
        graph = self.generate_random_graph(num_nodes, density)
        self.print_graph(graph)

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        a = (width - 2 * 30) / 2  # semi-major axis
        b = (height - 2 * 30) / 2  # semi-minor axis

        # Calculate center point
        center_x = width / 2
        center_y = height / 2

        positions = []

        # Generate positions
        for i in range(num_nodes):
            # Calculate angle for even distribution
            angle = (2 * math.pi * i) / num_nodes

            # Calculate position using parametric equations of ellipse
            x = center_x + a * math.cos(angle)
            y = center_y + b * math.sin(angle)

            self.add_node(x, y)

            positions.append((round(x), round(y)))

        for node_id in graph.keys():
            for to, w in graph.get(node_id, []):
                self.add_edge(node_id, to, w)
                print(node_id, "-w>", to)

        return

    def run_algorithm(self):

        algorithm = self.algorithm.get()

        if algorithm == "Prim":
            mst_graph = Controls.prim_mst(self.graph.graph)
            print(mst_graph)
            if mst_graph:
                self.paint_graph(mst_graph)
            else:
                print("No MST generated.")

        elif algorithm == "Kruskal":
            mst_graph = Controls.kruskal_mst(self.graph.graph, self.graph.nodes)
            if mst_graph:
                self.paint_graph(mst_graph)
            else:
                print("No MST generated.")

        elif algorithm == "Boruvka":
            mst_graph = Controls.boruvka_mst(self.graph.graph, self.graph.nodes)
            if mst_graph:
                self.paint_graph(mst_graph)
            else:
                print("No MST generated.")
        return

    def paint_graph(self, graph):
        print(graph)
        for node in graph:
            for edge in graph[node]:
                self.highlight_edge(node, edge[0])
                print(node, ": ", edge)
        # self.draw_mst(mst_graph)

    def highlight_nodes(self, finds):
        for node_id in finds:
            self.canvas.itemconfig(self.nodes[node_id].circle_id, fill="yellow")
            self.canvas.update()
            self.canvas.after(500)

    def highlight_edge(self, from_node_id, to_node_id):
        for edge in self.edges:
            if (edge.from_node_id == from_node_id and edge.to_node_id == to_node_id) or \
                    (edge.from_node_id == to_node_id and edge.to_node_id == from_node_id):
                self.canvas.itemconfig(edge.line_text_id, fill="red", width=2)
                self.canvas.update()
                # self.canvas.after(250)
                return

    def clear_canvas(self):
        self.canvas.delete("all")
        self.edges.clear()
        self.update_start_node_menu()

    def clear_everything(self):
        to_delete = []

        for node_id in self.nodes:
            to_delete.append(node_id)
        for node_id in to_delete:
            self.delete_node(node_id)

        self.graph = Models.Graph(self.is_oriented)
        self.canvas.delete("all")

    def update_start_node_menu(self):
        menu = self.start_node_menu["menu"]
        menu.delete(0, "end")
        for node_id in self.nodes.keys():
            menu.add_command(label=str(node_id), command=lambda value=node_id: self.start_node.set(value))
        if self.nodes:
            self.start_node.set(next(iter(self.nodes)))
        else:
            self.start_node.set(None)

    def generate_random_graph(self, num_nodes, density, min_weight=1, max_weight=100):
        if not 0 <= density <= 1:
            raise ValueError("Density must be between 0 and 1")

        graph = defaultdict(list)

        for source in range(num_nodes):
            for dest in range(num_nodes):
                if source == dest:
                    continue

                if random.random() < density:
                    existing_neighbors = [neighbor for neighbor, _ in graph[source]]
                    if dest not in existing_neighbors:
                        weight = random.randint(min_weight, max_weight)

                        graph[source].append((dest, weight))
                        graph[dest].append((source, weight))

        return dict(graph)

    def print_graph(self, graph):
        for node in sorted(graph.keys()):
            neighbors = sorted(graph[node])
            print(f"Node {node}: {neighbors}\n")

    def plot_performance_comparison(self, algorithm_results):

        plt.figure(figsize=(10, 6))

        styles = ['-o', '--s', ':^', '-.v', '-d', '--p']
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']

        for i, (algorithm_name, results) in enumerate(algorithm_results.items()):
            nodes, times = zip(*results)

            style = styles[i % len(styles)]
            color = colors[i % len(colors)]

            plt.plot(nodes, times, style, label=algorithm_name, color=color)

        plt.xlabel('Number of Nodes')
        plt.ylabel('Time Elapsed (seconds)')
        plt.title('Algorithm Performance Comparison')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

        plt.ylim(bottom=0)

        plt.show(block=False)
