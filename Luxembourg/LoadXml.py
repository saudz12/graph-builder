import xml.etree.ElementTree as ET


def compute_scale_and_offset(x_min, y_min, x_max, y_max, width, height):
    grid_height = x_max - x_min
    grid_width = y_max - y_min

    if grid_width == 0 or grid_height == 0:
        raise ValueError("Grid dimensions cannot be zero.")

    scale_x = height / grid_height
    scale_y = width / grid_width
    scale = min(scale_x, scale_y)

    return scale

def scale_coordinates(x, y, x_min, y_min, scale):
    scaled_x = (x - x_min) * scale
    scaled_y = (y - y_min) * scale
    return scaled_x, scaled_y

class GraphInfo:
    def __init__(self):
        self.adjacency = {}
        self.positions = {}

        #for resizing
        self.up = 0 #min x
        self.left = 0 #min y
        self.down = 0 #max x
        self.right = 0 #max y
        self.scale = 0 #scaling fom original x/y to canvas x/y

    def full_setup(self, filename, width, height):
        self.load_tree(filename)
        self.scale_tree(width, height)

    def load_tree(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        #nodes
        for node in root.iter('node'):
            #print(node.attrib['id'])
            node_id = int(node.attrib['id'])
            pos_x = float(node.attrib['longitude'])
            pos_y = float(node.attrib['latitude'])

            self.adjacency.setdefault(node_id, [])
            self.positions.setdefault(node_id, (pos_x, pos_y))

        for arc in root.iter('arc'):
            from_id = int(arc.attrib['from'])
            to_id = int(arc.attrib['to'])
            weight = int(arc.attrib['length'])

            self.adjacency[from_id].append((to_id, weight))

    def get_limits(self):
        first_id = next(iter(self.positions))
        #print(positions[first_id])

        self.up = self.positions[first_id][0]
        self.left = self.positions[first_id][1]
        self.down = self.positions[first_id][0]
        self.right = self.positions[first_id][1]

        for key in self.positions:
            value = self.positions[key]
            # print(value)
            if value[0] < self.up:
                self.up = value[0]

            if value[1] < self.left:
                self.left = value[1]

            if value[0] > self.down:
                self.down = value[0]

            if value[1] > self.right:
                self.right = value[1]

    def scale_tree(self, width, height):
        scaled_positions = {}

        self.get_limits()

        scale = compute_scale_and_offset(self.up, self.left, self.down, self.right, width, height)

        for node in self.positions:
            x, y = self.positions[node]
            scaled_x, scaled_y = scale_coordinates(x, y, self.up, self.left, scale)
            scaled_positions[node] = (scaled_x, scaled_y)
            #print(node, scaled_positions[node])

        self.positions = scaled_positions

        #print(self.positions)
        #print(next(iter(self.positions)))

# def debug():
#     adjacency = {}
#     positions = {}
#     load_tree('Harta_Luxemburg.xml', adjacency, positions)
#
#     first_id = (next(iter(positions)))
#     print(positions[first_id])
#
#     xmin = positions[first_id][0]
#     ymin = positions[first_id][1]
#     xmax = positions[first_id][0]
#     ymax = positions[first_id][1]
#
#     for key in positions:
#         value = positions[key]
#         #print(value)
#         if value[0] < xmin:
#             xmin = value[0]
#         if value[1] < ymin:
#             ymin = value[1]
#         if value[0] > xmax:
#             xmax = value[0]
#         if value[1] > ymax:
#             ymax = value[1]
#
#     print("leftmost, uppermost, rightmost, lowermsot: ", xmin, ymin, xmax, ymax)
#
#     scale = compute_scale_and_offset(xmin, ymin, xmax, ymax, 2000, 1500)
#
#     xsmin = None
#     ysmin = None
#     xsmax = None
#     ysmax = None
#
#     leftmost = None
#     rightmost = None
#     uppermost = None
#     lowermost = None
#
#     print("Scale: ", scale)
#
#     for node in positions:
#         x, y = positions[node]
#         #print(node, x, y)
#         scaled_x, scaled_y = scale_coordinates(x, y, xmin, ymin, scale)
#         #print(node, scaled_x, scaled_y)
#
#         if xsmin is None:
#             xsmin = scaled_x
#             leftmost = node
#         if scaled_x < xsmin:
#             xsmin = scaled_x
#             leftmost = node
#         if ysmin is None:
#             ysmin = scaled_y
#             uppermost = node
#         if scaled_y < ysmin:
#             ysmin = scaled_y
#             uppermost = node
#         if xsmax is None or scaled_x > xsmax:
#             xsmax = scaled_x
#             rightmost = node
#         if ysmax is None or scaled_y > ysmax:
#             ysmax = scaled_y
#             lowermost = node
#         #print(xsmin, ysmin, xsmax, ysmax)
#
#         #input()
#
#     print("leftmost, uppermost, rightmost, lowermsot: ", leftmost, uppermost, rightmost, lowermost)
#
#     #print(positions)
#
# #debug()