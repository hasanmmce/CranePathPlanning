import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GridPathFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Path Finder")
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Rows:").grid(row=0, column=0)
        tk.Label(self.root, text="Columns:").grid(row=0, column=2)
        
        self.rows_entry = tk.Entry(self.root)
        self.rows_entry.grid(row=0, column=1)
        
        self.cols_entry = tk.Entry(self.root)
        self.cols_entry.grid(row=0, column=3)
        
        tk.Button(self.root, text="Create Grid", command=self.create_grid).grid(row=0, column=4)
        
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=1, column=0, columnspan=5)
        
        self.start_coords = []
        self.end_coords = []
        
        self.hv_multiplier = 1
        self.diag_multiplier = 1
    
    def create_grid(self):
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())
        
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        for r in range(rows):
            for c in range(cols):
                entry = tk.Entry(self.grid_frame, width=5)
                entry.grid(row=r, column=c)
                self.grid[r][c] = entry
        
        tk.Button(self.root, text="Set Weights", command=self.set_weights).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Add Start Point", command=self.add_start_point).grid(row=2, column=2)
        tk.Button(self.root, text="Add End Point", command=self.add_end_point).grid(row=2, column=3)
        tk.Button(self.root, text="Set Multipliers", command=self.set_multipliers).grid(row=2, column=4)
        tk.Button(self.root, text="Find Paths", command=self.find_paths).grid(row=3, column=0, columnspan=5)
    
    def set_weights(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                try:
                    self.grid[r][c] = int(self.grid[r][c].get())
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Invalid weight at ({r}, {c})")
                    return
    
    def add_start_point(self):
        row = simpledialog.askinteger("Input", "Start Row:")
        col = simpledialog.askinteger("Input", "Start Column:")
        self.start_coords.append((row, col))
    
    def add_end_point(self):
        row = simpledialog.askinteger("Input", "End Row:")
        col = simpledialog.askinteger("Input", "End Column:")
        self.end_coords.append((row, col))
    
    def set_multipliers(self):
        self.hv_multiplier = float(simpledialog.askfloat("Input", "HV Multiplier:"))
        self.diag_multiplier = float(simpledialog.askfloat("Input", "Diagonal Multiplier:"))
    
    def create_graph_from_grid(self, grid, hv_multiplier=1, diag_multiplier=1):
        G = nx.DiGraph()
        rows, cols = len(grid), len(grid[0])
        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    G.add_edge((r, c), (r + 1, c), weight=grid[r + 1][c] * hv_multiplier)
                    G.add_edge((r + 1, c), (r, c), weight=grid[r][c] * hv_multiplier)
                if c + 1 < cols:
                    G.add_edge((r, c), (r, c + 1), weight=grid[r][c + 1] * hv_multiplier)
                    G.add_edge((r, c + 1), (r, c), weight=grid[r][c] * hv_multiplier)
                if r + 1 < rows and c + 1 < cols:
                    G.add_edge((r, c), (r + 1, c + 1), weight=grid[r + 1][c + 1] * diag_multiplier)
                    G.add_edge((r + 1, c + 1), (r, c), weight=grid[r][c] * diag_multiplier)
                if r + 1 < rows and c - 1 >= 0:
                    G.add_edge((r, c), (r + 1, c - 1), weight=grid[r + 1][c - 1] * diag_multiplier)
                    G.add_edge((r + 1, c - 1), (r, c), weight=grid[r][c] * diag_multiplier)
                if r - 1 >= 0 and c + 1 < cols:
                    G.add_edge((r, c), (r - 1, c + 1), weight=grid[r - 1][c + 1] * diag_multiplier)
                    G.add_edge((r - 1, c + 1), (r, c), weight=grid[r][c] * diag_multiplier)
                if r - 1 >= 0 and c - 1 >= 0:
                    G.add_edge((r, c), (r - 1, c - 1), weight=grid[r - 1][c - 1] * diag_multiplier)
                    G.add_edge((r - 1, c - 1), (r, c), weight=grid[r][c] * diag_multiplier)
        return G

    def compute_shortest_paths(self, grid, start, end, hv_multiplier=1, diag_multiplier=1):
        G = self.create_graph_from_grid(grid, hv_multiplier, diag_multiplier)
        try:
            length, path = nx.single_source_dijkstra(G, start, end)
            return length, path
        except nx.NetworkXNoPath:
            return float('inf'), []

    def find_paths(self):
        self.set_weights()
        paths = []
        total_length = 0
        
        for start, end in zip(self.start_coords, self.end_coords):
            length, path = self.compute_shortest_paths(self.grid, start, end, self.hv_multiplier, self.diag_multiplier)
            paths.append(path)
            total_length += length
        
        self.visualize_grid_with_paths(self.grid, self.start_coords, self.end_coords, paths)
        print(f"Total path length: {total_length}")
        for i, path in enumerate(paths):
            print(f"Path {i+1}: {path}")

    def visualize_grid_with_paths(self, grid, starts, ends, paths):
        rows, cols = len(grid), len(grid[0])
        fig, ax = plt.subplots()
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True)
        
        for r in range(rows):
            for c in range(cols):
                ax.text(c, r, grid[r][c], va='center', ha='center')

        # Highlight the start and end points
        for start in starts:
            ax.add_patch(plt.Circle((start[1], start[0]), 0.2, color='green', label='Start'))
        for end in ends:
            ax.add_patch(plt.Circle((end[1], end[0]), 0.2, color='red', label='End'))

        # Draw the paths
        for path in paths:
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]
                ax.plot([c1, c2], [r1, r2], color='blue', linewidth=2)

        plt.gca().invert_yaxis()
        plt.legend(loc='upper right')

        # Embedding the plot in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=5)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GridPathFinder(root)
    root.mainloop()
