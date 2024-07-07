import networkx as nx
import matplotlib.pyplot as plt
import math

# Step 2: Create the Graph from Grid with weight multipliers
def create_graph_from_grid(grid, hv_multiplier, diag_multiplier):
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

# Step 3: Compute Shortest Paths
def compute_shortest_paths(grid, start, end, hv_multiplier, diag_multiplier):
    G = create_graph_from_grid(grid, hv_multiplier, diag_multiplier)
    try:
        length, path = nx.single_source_dijkstra(G, start, end)
        return length, path
    except nx.NetworkXNoPath:
        return float('inf'), []

# Step 4: Combine and Visualize Paths
def find_and_visualize_paths(grid, starts, ends, hv_multiplier, diag_multiplier):
    paths = []
    total_length = 0
    
    for start, end in zip(starts, ends):
        length, path = compute_shortest_paths(grid, start, end, hv_multiplier, diag_multiplier)
        paths.append(path)
        total_length += length
    
    visualize_grid_with_paths(grid, starts, ends, paths)
    return total_length, paths

# Step 5: Visualize the Grid and Paths
def visualize_grid_with_paths(grid, starts, ends, paths):
    rows, cols = len(grid), len(grid[0])
    fig, ax = plt.subplots()
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    
    for r in range(rows):
        for c in range(cols):
            ax.text(c, r, grid[r][c], va='center', ha='center', fontsize=5)

    # Highlight the start and end points
    for start in starts:
        ax.add_patch(plt.Circle((start[1], start[0]), 0.1, color='green', label='Start'))
    for end in ends:
        ax.add_patch(plt.Circle((end[1], end[0]), 0.1, color='red', label='End'))

    # Draw the paths
    for path in paths:
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            ax.plot([c1, c2], [r1, r2], color='blue', linewidth=2)

    plt.gca().invert_yaxis()
    plt.legend(loc='upper right')
    plt.show()

# Example Usage
grid = [
    # [1,1,1,1,1,1,1000000,1000000,1000000,1000000,1000000,1000000,1,1],
    # [1,1,1,1,1,1,1000000,1000000,1000000,1000000,1000000,1000000,1,1],
    # [1,1,1,1,1000000,1,1,1,1,1,1,1,1,1],
    # [1000000,1000000,1000000,1,1,1,1,1,1,1,1,1,1,1],
    # [1000000,1000000,1000000,1,1,1,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,1,1,1,1,1,1000000,1,1,1],
    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,100000,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,1000000,1,1,1,1,1,1,1,1],
    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    
    [7684,7684,3085,3735,3735,3735,1000000,1000000,1000000,1000000,1000000,1000000,5230,5230],
    [7684,7684,3085,3735,3735,3735,1000000,1000000,1000000,1000000,1000000,1000000,5230,5230],
    [7684,7684,3085,5831,1000000,11275,11275,11275,9293,9293,5230,5230,5230,5230],
    [1000000,1000000,1000000,5831,5831,11275,11275,11275,3264,5230,5230,5230,3085,3085],
    [1000000,1000000,1000000,11275,5831,11275,11275,11275,3735,5230,5230,5230,3085,3085],
    [6075,11275,11275,11275,3735,3735,3085,3735,3735,3735,2273,3085,3085,3085],
    [6075,11275,11275,11275,6985,7684,7684,7684,3735,4239,4239,8708,8708,8708],
    [3264,3264,3264,6985,6985,7684,7684,7684,3085,4239,1000000,8708,8708,8708],
    [3264,3264,3264,8708,8708,8708,8708,8708,3085,4239,4239,8708,8708,8708],
    [3085,3085,3085,8708,8708,1000000,8708,8708,3085,3085,2663,3264,3264,3264],
    [3085,5003,5003,8708,8708,1000000,8708,8708,5230,5831,5831,11275,11275,11275],
    [3264,5003,5003,5003,2273,2273,2273,5230,5230,5831,5831,11275,11275,11275]

]

starts = [(0,12), (8,12), (11,4), (0,4)]
ends = [(4,8), (6,9), (7,6), (5,5)]
hv_multiplier = 100/1000
diag_multiplier = math.sqrt(2*100**2)/1000

total_length, paths = find_and_visualize_paths(grid, starts, ends, hv_multiplier, diag_multiplier)
print(f"Total path length: {total_length}")
for i, path in enumerate(paths):
    print(f"Path {i+1}: {path}")