import networkx as nx
import matplotlib.pyplot as plt

def is_safe(graph, vertex, color, colors):
    """Check if assigning 'color' to 'vertex' is valid"""
    for neighbor in graph.neighbors(vertex):
        if colors[neighbor] == color:
            return False
    return True

def graph_coloring_util(graph, m, colors, vertex):
    """Recursive backtracking function to assign colors"""
    if vertex == len(graph):  # All vertices are colored
        return True

    for color in range(1, m + 1):  # Try all colors (1 to m)
        if is_safe(graph, vertex, color, colors):
            colors[vertex] = color  # Assign color

            if graph_coloring_util(graph, m, colors, vertex + 1):
                return True

            colors[vertex] = 0  # Backtrack

    return False

def graph_coloring(graph, m):
    """Main function to solve graph coloring and visualize it"""
    colors = {node: 0 for node in graph.nodes()}  # Initialize colors

    if not graph_coloring_util(graph, m, colors, 0):
        print("No solution found!")
        return

    # Assign colors
    color_map = {1: "red", 2: "blue", 3: "green", 4: "yellow", 5: "purple"}
    node_colors = [color_map[colors[node]] for node in graph.nodes()]

    # Draw the graph
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=16, edge_color="gray")
    plt.show()

# Example graph (Adjacency list representation)
G = nx.Graph()
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]
G.add_edges_from(edges)

m = 3  # Number of colors
graph_coloring(G, m)
