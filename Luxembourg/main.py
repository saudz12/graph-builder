from Interface import *
from LoadXml import GraphInfo

if __name__ == '__main__':
    g = GraphInfo()

    g.full_setup("Harta_Luxemburg.xml", 2000, 1500)

    root = tk.Tk()
    app = GUI(root, g.adjacency, g.positions)

    root.mainloop()