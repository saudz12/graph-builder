import tkinter as tk
from Utilities import *

class GUI:
    def __init__(self, master, adjacency, positions):
        self.master = master
        self.master.title("Luxembourg")
        self.master.resizable(height=0, width=0)
        self.adjacency = adjacency
        self.algorithms = Algorithms(adjacency)
        self.positions = positions
        #self.master.state('zoomed')

        self.points = {}

        self.main_frame = None
        self.canvas = None

        self.dot = 1

        self.c_width = 2000
        self.c_height = 1500

        self.turn = False

        self.from_search_circle = None
        self.to_search_circle = None

        self.from_search_node = None
        self.to_search_node = None

        self.mode = tk.StringVar(value = "dijkstra")

        self.create_widgets()

        self.init_map()

        self.road = []

    def create_widgets(self):
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white", width = self.c_width, height = self.c_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)

        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        modes_frame = tk.LabelFrame(control_frame, text="Mode", font=30)
        modes_frame.pack(pady=10)

        tk.Radiobutton(modes_frame, text="Dijkstra's", font=30, variable=self.mode, value="dijkstra").pack(anchor=tk.W)
        tk.Radiobutton(modes_frame, text="Bellman-Ford", font=30, variable=self.mode, value="bellman-ford").pack(anchor=tk.W)

        run_button = tk.Button(control_frame, text="Run", font=30, command=self.run_algorithm)
        run_button.pack(pady=10)

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)

    def init_map(self):
        #line_id = self.canvas.create_line(100, 1500 - 400, 200, 1500 - 300, smooth = True, fill = "blue")

        # for node in self.positions:
        #     x, y = self.positions[node]
        #     #print(node, x, y)

        for node in self.positions:
            from_x, from_y = self.positions[node]
            self.positions[node] = (self.c_width - from_y, self.c_height - from_x)

        for node in self.adjacency:
            from_x, from_y = self.positions[node]

            tknid = self.canvas.create_oval(from_x - self.dot,
                                            from_y - self.dot,
                                            from_x + self.dot,
                                            from_y + self.dot,
                                            fill = 'blue')
            self.points[tknid] = Node(node, from_x, from_y, tknid)

            for edge in self.adjacency[node]:

                #from_x = self.c_width - from_x

                to_node, _ = edge
                to_x, to_y = self.positions[to_node]

                #to_x = self.c_width - to_x

                #self.canvas.create_line(self.c_width - from_y, self.c_height - from_x,self.c_width - to_y, self.c_height - to_x, smooth=True, fill="blue")
                self.canvas.create_line(from_x,from_y,to_x,to_y, smooth=True, fill="blue")
            #self.canvas.update()

    def canvas_click(self, event):
        x = event.x
        y = event.y

        if self.from_search_circle is not None:
            self.canvas.delete(self.from_search_circle.tkid)
        if self.to_search_circle is not None:
            self.canvas.delete(self.to_search_circle.tkid)

        print(x, y)

        selected = self.canvas.find_overlapping(x - self.dot,
                                                y - self.dot,
                                                x + self.dot,
                                                y + self.dot)

        if len(selected) != 0:
            # print(selected)
            # print(selected[0])
            # print(self.points[selected[0]])

            if selected[0] not in self.points:
                return

            found = self.points[selected[0]]


            hx = found.x
            hy = found.y
            node_id = found.id

            if self.turn is False:
                self.turn = True
                self.from_search_node = node_id

                tknid1 = self.canvas.create_oval(hx - self.dot * 5,
                                                 hy - self.dot * 5,
                                                 hx + self.dot * 5,
                                                 hy + self.dot * 5,
                                                 fill='red')

                self.from_search_circle = Node(0, hx, hy, tknid1)


                if self.to_search_circle is not None:
                    tknid2 = self.canvas.create_oval(hx - self.dot * 5,
                                                     hy - self.dot * 5,
                                                     hx + self.dot * 5,
                                                     hy + self.dot * 5,
                                                     fill='red')

                    self.to_search_circle.tkid = tknid2

                print("New source, same destination")
            else:
                self.turn = False
                self.to_search_node = node_id

                if self.from_search_circle is not None:
                    tknid1 = self.canvas.create_oval(self.from_search_circle.x - self.dot * 5,
                                                     self.from_search_circle.y - self.dot * 5,
                                                     self.from_search_circle.x + self.dot * 5,
                                                     self.from_search_circle.y + self.dot * 5,
                                                     fill='red')

                    self.from_search_circle.tkid = tknid1

                tknid2 = self.canvas.create_oval(hx - self.dot * 5,
                                                 hy - self.dot * 5,
                                                 hx + self.dot * 5,
                                                 hy + self.dot * 5,
                                                 fill='green')

                self.to_search_circle = Node(0, hx, hy, tknid2)

                print("Same source, New destination")
        else:
            if self.from_search_circle is not None:
                print("Same source")
                self.from_search_circle.tkid = self.canvas.create_oval(self.from_search_circle.x - self.dot * 5,
                                                                       self.from_search_circle.y - self.dot * 5,
                                                                       self.from_search_circle.x + self.dot * 5,
                                                                       self.from_search_circle.y + self.dot * 5,
                                                                       fill='red')

            if self.to_search_circle is not None:
                print("Same destination")
                self.to_search_circle.tkid = self.canvas.create_oval(self.to_search_circle.x - self.dot * 5,
                                                                     self.to_search_circle.y + self.dot * 5,
                                                                     self.to_search_circle.x - self.dot * 5,
                                                                     self.to_search_circle.y + self.dot * 5,
                                                                     fill='green')

    def canvas_release(self, event):
        return

    def clean_road(self):
        for line_id in self.road:
            self.canvas.delete(line_id)
        self.road = []

    def draw_road(self, id_from, id_to, prev):
        self.clean_road()
        c = id_to

        total_cost = 0

        while c != id_from:
            x, y = self.positions.get(c)
            #c = prev.get(c)
            parent = prev[c]
            for neighbour, weight in self.adjacency.get(parent):
                if neighbour == c:
                    total_cost += weight
                    break

            X, Y = self.positions.get(parent, (self.positions.get(id_to)))
            self.road.append(self.canvas.create_line(x, y, X, Y, smooth=True, fill="red", width=4))

            c = parent

        print("Total cost: ", total_cost)

    def run_algorithm(self):
        mode = self.mode.get()

        if self.from_search_circle is None or self.to_search_circle is None:
            return

        print("from: (", self.from_search_circle.x, ", ", self.from_search_circle.y, ") to (", self.to_search_circle.x, ", ", self.to_search_circle.y, ")")
        print(self.from_search_node, self.adjacency[self.from_search_node])
        print(self.to_search_node, self.adjacency[self.to_search_node])

        if mode == "dijkstra":
            print("Dijktra's")
            prev = self.algorithms.alg_dijkstra(self.from_search_node, self.to_search_node)
            #self.draw_road(self.from_search_node, self.to_search_node, prev)
        else:
            print("Bellman-ford")
            prev = self.algorithms.alg_bellman_ford_numpy(self.from_search_node, self.to_search_node)
        self.draw_road(self.from_search_node, self.to_search_node, prev)

