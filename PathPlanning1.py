import networkx as nx
import time

# print("Hello, World!")
# import numpy as np
# print(np.__version__)




import matplotlib.pyplot as plt 

# Start measuring the code run time
start_time = time.time()

# Create a directed graph from the grid
def create_graph_from_grid(grid):
    G = nx.DiGraph()
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if r + 1 < rows:
                G.add_edge((r, c), (r + 1, c), weight=grid[r + 1][c])
                G.add_edge((r + 1, c), (r, c), weight=grid[r][c])
            if c + 1 < cols:
                G.add_edge((r, c), (r, c + 1), weight=grid[r][c + 1])
                G.add_edge((r, c + 1), (r, c), weight=grid[r][c])
            if r + 1 < rows and c + 1 < cols:
                G.add_edge((r, c), (r + 1, c + 1), weight=grid[r + 1][c + 1])
                G.add_edge((r + 1, c + 1), (r, c), weight=grid[r][c])
            if r + 1 < rows and c - 1 >= 0:
                G.add_edge((r, c), (r + 1, c - 1), weight=grid[r + 1][c - 1])
                G.add_edge((r + 1, c - 1), (r, c), weight=grid[r][c])
            if r - 1 >= 0 and c + 1 < cols:
                G.add_edge((r, c), (r - 1, c + 1), weight=grid[r - 1][c + 1])
                G.add_edge((r - 1, c + 1), (r, c), weight=grid[r][c])
            if r - 1 >= 0 and c - 1 >= 0:
                G.add_edge((r, c), (r - 1, c - 1), weight=grid[r - 1][c - 1])
                G.add_edge((r - 1, c - 1), (r, c), weight=grid[r][c])
    return G

# Visualize the grid with the shortest path
def visualize_grid_with_path(grid, start, end, path):
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
    ax.add_patch(plt.Circle((start[1], start[0]), 0.15, color='green', label='Start'))
    ax.add_patch(plt.Circle((end[1], end[0]), 0.15, color='red', label='End'))

    # Draw the path
    if path:
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            ax.plot([c1, c2], [r1, r2], color='blue', linewidth=2)

    plt.gca().invert_yaxis()
    plt.legend(loc='upper right')
    plt.show()

# Find the shortest path using Dijkstra's algorithm in networkx
def dijkstra_shortest_path_networkx(grid, start, end):
    G = create_graph_from_grid(grid)
    try:
        length, path = nx.single_source_dijkstra(G, start, end)
        return length, path
    except nx.NetworkXNoPath:
        return -1, []

# Example usage:
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

start = (11, 4)
end = (7, 6)


# Visualize the grid
plt.imshow(grid, cmap='Blues', origin='lower')
plt.scatter(start[1], start[0], color='green', label='Start')
plt.scatter(end[1], end[0], color='red', label='End')
plt.legend(loc='upper right')
plt.show()



# Find the shortest path and its length
length, path = dijkstra_shortest_path_networkx(grid, start, end)
print(f"Shortest path length: {length}")
print(f"Path: {path}")


# Calculate the code run time
end_time = time.time()
runtime = (end_time - start_time)
print(f"Runtime: {runtime} seconds")


# Visualize the grid with the shortest path
visualize_grid_with_path(grid, start, end, path)


