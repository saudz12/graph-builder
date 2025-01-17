import tkinter as tk
import math
import Utility
import Algorithm
from Utility import DrawNode
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Algorithms Visualization")

        # Mode and other settings
        self.mode = tk.StringVar(value="draw_node")

        # Algorithm selection
        self.algorithm = tk.StringVar(value="DFS")

        # Starting node selection
        self.start_node = tk.IntVar()

        # Node Counter
        self.node_counter = 0

        self.is_oriented = True

        self.nodes = {}
        self.edges = []
        self.graph = Utility.Graph(self.is_oriented)
        self.reusable_ids = []

        self.r = 20

        self.main_frame = None
        self.canvas = None
        self.weight_text = None
        self.capacity_text = None

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

        tk.Radiobutton(modes_frame, text="Draw Nodes", variable=self.mode, value="draw_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Draw Edges", variable=self.mode, value="draw_edge").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Move Nodes", variable=self.mode, value="move_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Delete Nodes", variable=self.mode, value="delete_node").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Delete Edges", variable=self.mode, value="delete_edge").pack(anchor=tk.W)

        # checkbox

        self.is_oriented = tk.BooleanVar(value=self.is_oriented)
        oriented_checkbox = tk.Checkbutton(
            control_frame, text="Oriented Graph", variable=self.is_oriented,
            command=self.toggle_orientation
        )
        oriented_checkbox.pack(pady=10)

        # textbox

        capacity_frame = tk.LabelFrame(control_frame, text="Capacity")
        capacity_frame.pack(pady=10)
        self.capacity_text = tk.Entry(capacity_frame)
        self.capacity_text.insert(0, "0")
        self.capacity_text.pack(pady=5)

        weight_frame = tk.LabelFrame(control_frame, text="Weight")
        weight_frame.pack(pady=10)
        self.weight_text = tk.Entry(weight_frame)
        self.weight_text.insert(0, "0")
        self.weight_text.pack(pady=5)

        # Algorithm selection

        alg_frame = tk.LabelFrame(control_frame, text="Algorithm")
        alg_frame.pack(pady=10)
        algorithms = ["Recursive DFS", "DFS", "BFS", "CC", "Kosaraju", "Topological Sort", "Find Center", "Transform to Tree", "Prim", "Kruskal", "Boruvka", "Ford Fulkerson", "Cycle Cancelling"]
        alg_menu = tk.OptionMenu(alg_frame, self.algorithm, self.algorithm.get(), *algorithms)
        alg_menu.pack()

        # Starting node selection

        start_node_frame = tk.LabelFrame(control_frame, text="Start Node")
        start_node_frame.pack(pady=10)
        self.start_node_menu = tk.OptionMenu(start_node_frame, self.start_node, None)
        self.start_node_menu.pack()

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

        node = DrawNode(node_id, x, y, circle_id, text_id)
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

    def add_edge(self, from_node_id, to_node_id):
        for edge in self.edges:
            if edge.from_node_id == from_node_id and edge.to_node_id == to_node_id:
                return  # Edge already exists

            if not self.is_oriented and edge.from_node_id == to_node_id and edge.to_node_id == from_node_id:
                return  # Edge already exists in undirected graph

        weight = self.weight_text.get() or "0"
        capacity = self.capacity_text.get() or "0"
        try:
            weight = int(weight)
        except ValueError:
            weight = 0

        try:
            capacity = int(capacity)
        except ValueError:
            capacity = 0

        line_id, weight_text_id = self.paint_edge(from_node_id, to_node_id, weight, capacity)

        edge = Utility.DrawEdge(from_node_id, to_node_id, line_id, weight, capacity, weight_text_id)
        edge.weight = weight
        #edge.weight_text_id = weight_text_id
        self.edges.append(edge)

        self.graph.add_edge(from_node_id, to_node_id, weight, capacity, line_id)
        #print(from_node_id, ": ", to_node_id)
        if not self.is_oriented:
            #print(to_node_id, ": ", from_node)
            self.graph.add_edge(to_node_id, from_node_id, weight, capacity, line_id)

        print(self.graph.graph)
        print(self.edges)

    def paint_edge(self, from_node_id, to_node_id, weight, capacity):
        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]

        if self.is_oriented.get():
            dx, dy = to_node.x - from_node.x, to_node.y - from_node.y
            mid_x, mid_y = (from_node.x + to_node.x) / 2, (from_node.y + to_node.y) / 2
            curve_offset = 10
            curve_x = mid_x - curve_offset * dy / math.sqrt(dx ** 2 + dy ** 2)
            curve_y = mid_y + curve_offset * dx / math.sqrt(dx ** 2 + dy ** 2)

            line_id = self.canvas.create_line(from_node.x, from_node.y, curve_x, curve_y, to_node.x, to_node.y,
                                              smooth=True, arrow=tk.LAST)

            weight_text_id = self.canvas.create_text(curve_x, curve_y,
                                                     text=str(capacity) + "/" + str(weight))
        else:
            line_id = self.canvas.create_line(from_node.x, from_node.y, to_node.x, to_node.y)
            weight_text_id = self.canvas.create_text(   (from_node.x + to_node.x) / 2, (from_node.y + to_node.y) / 2,
                                                        text=str(capacity) + "/" + str(weight))

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

    def get_old_graph(self):
        for edge in self.edges:
            self.canvas.itemconfig(edge.line_text_id, width="1")

    def run_algorithm(self):
        self.get_old_graph()
        start_node_id = self.start_node.get()
        if start_node_id is None:
            print("Please select a starting node.")
            return

        algorithm = self.algorithm.get()

        # Reset colors
        for node in self.nodes.values():
            self.canvas.itemconfig(node.circle_id, fill="lightblue")
        for edge in self.edges:
            self.canvas.itemconfig(edge.line_text_id, fill="black")

        if algorithm == "Recursive DFS":
            visited = {}
            finds = []
            Algorithm.recursive_dfs(self.graph.graph, start_node_id, visited, finds)
            print(finds)
            self.highlight_nodes(finds)

        elif algorithm == "DFS":
            finds = Algorithm.iterative_dfs(self.graph.graph, start_node_id)
            self.highlight_nodes(finds)

        elif algorithm == "BFS":
            finds = Algorithm.bfs(self.graph.graph, start_node_id)
            self.highlight_nodes(finds)

        elif algorithm == "CC":
            conex_list = Algorithm.cc(self.graph.graph, self.graph.nodes)
            for component in conex_list:
                self.paint_component(component)

        elif algorithm == "Kosaraju":
            conex_list = Algorithm.scc_kosaraju(self.graph.graph, self.graph.nodes)
            for component in conex_list:
                self.paint_component(component)

        elif algorithm == "Topological Sort":
            order = Algorithm.ts(self.graph.graph)
            self.highlight_nodes(order)

        elif algorithm == "Find Center":
            center = Algorithm.find_center(self.graph.graph)
            self.canvas.itemconfig(self.nodes[center].circle_id, fill="green")
            self.canvas.update()

        elif algorithm == "Transform to Tree":
            center = Algorithm.find_center(self.graph.graph)
            self.canvas.itemconfig(self.nodes[center].circle_id, fill="green")
            self.canvas.update()
            self.make_tree(center)

        elif algorithm == "Prim":
            mst_graph = Algorithm.prim_mst(self.graph.graph)
            if mst_graph:
               self.paint_graph(mst_graph)
            else:
                print("No MST generated.")

        elif algorithm == "Kruskal":
            mst_graph = Algorithm.kruskal_mst(self.graph.graph, self.graph.nodes)
            if mst_graph:
                self.paint_graph(mst_graph)
            else:
                print("No MST generated.")

        elif algorithm == "Boruvka":
            mst_graph = Algorithm.boruvka_mst(self.graph.graph, self.graph.nodes)
            if mst_graph:
                self.paint_graph(mst_graph)
            else:
                print("No MST generated.")

        elif algorithm == "Ford Fulkerson":
            print("Ford Fulkerson:")
            source = int(input())
            sink = int(input())
            if source not in self.graph.nodes or sink not in self.graph.nodes:
                print("invalid source/sink")
                return

            max_flow, parent, r_g = Algorithm.ford_fulkerson(self.graph.graph, self.graph.nodes, source, sink)
            print("Max Flux: ", max_flow)

            for edge in self.edges:
                #self.canvas.itemconfig(edge.flux_text_id, text = str(r_g[edge.from_node_id][edge.to_node_id][0]) + "/" + str(r_g[edge.from_node_id][edge.to_node_id][1]))
                self.canvas.itemconfig(edge.flux_text_id, text=str(r_g[edge.to_node_id][edge.from_node_id]))
            v = sink

            while v != source:
                print(parent[v], "-->", v)
                self.highlight_edge(parent[v], v)
                v = parent[v]
            self.canvas.update()

        elif algorithm == "Cycle Cancelling":
            #testing...
            graph = {
                0: [(1, 1, 4), (2, 2, 3)],
                1: [(2, -3, 2), (3, 2, 2)],
                2: [(3, 1, 4)],
            }

            result = Algorithm.min_flow_cycle_canceling(graph, source=0, sink=3)
            print(result)

            #on our graph

            source = int(self.get_number_input())
            sink = int(self.get_number_input())

            found = False

            for node in self.nodes:
                if self.nodes[node].id == source:
                    found = True
                    break

            if not found:
                print("need a valid source")
                return

            found = False

            for node in self.nodes:
                if self.nodes[node].id == sink:
                    found = True
                    break

            if not found:
                print("need a valid sink")
                return

            print(source, sink)

            result = Algorithm.min_flow_cycle_canceling(self.graph.graph, source, sink);

            print(result)

            for node in result:
                print(node)
                for edge in result.get(node, []):
                    print(edge)
                    for e in self.edges:
                        if e.from_node_id == node and e.to_node_id == edge[0]:
                            self.canvas.itemconfig(e.flux_text_id, text=str(edge[1]) + "/" + str(edge[2]) + "/" + str(edge[3]))
                            continue


    def make_tree(self, center):
        visited = set()
        visited.add(center)

        stack = [center]
        while stack:
            curr_node = stack.pop()
            for neighbour in self.graph.graph.get(curr_node, []):
                if neighbour[0] not in visited:
                    visited.add(neighbour[0])
                    self.orient_edge(curr_node, neighbour[0])

    def orient_edge(self, from_node_id, to_node_id):
        for edge in self.edges:
            if edge.from_node_id == from_node_id and edge.to_node_id == to_node_id:
                self.canvas.itemconfig(edge.line_text_id, arrow=tk.LAST)
                self.canvas.update()
                break
            elif edge.from_node_id == to_node_id and edge.to_node_id == from_node_id:
                self.canvas.itemconfig(edge.line_text_id, arrow=tk.FIRST)
                self.canvas.update()
                break

    def paint_component(self, component):
        import random

        component_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        for node_id in component:
            self.canvas.itemconfig(self.nodes[node_id].circle_id, fill=component_color)
            self.canvas.update()

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
                #self.canvas.after(250)
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

        self.graph = Utility.Graph(self.is_oriented)
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

    def get_number_input(self, title="Enter Number", prompt="Please enter a number:"):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.grab_set()

        dialog.geometry("300x150")
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        dialog.geometry(f"+{x}+{y}")

        result = None

        def submit():
            nonlocal result
            try:
                value = entry.get()
                result = float(value)
                if result.is_integer():
                    result = int(result)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        tk.Label(dialog, text=prompt, pady=10).pack()
        entry = tk.Entry(dialog)
        entry.pack(pady=10)
        tk.Button(dialog, text="Submit", command=submit).pack()

        entry.focus()
        dialog.bind('<Return>', lambda e: submit())

        dialog.wait_window()
        return result