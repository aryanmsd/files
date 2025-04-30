import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def is_valid(state, capacities):
    return 0 <= state[0] <= capacities[0] and 0 <= state[1] <= capacities[1]

def bfs_water_jug(capacities, target):
    visited = set()
    queue = deque([((0, 0), [])])  # (current state, path to state)
    graph = nx.DiGraph()
    
    while queue:
        (current, path) = queue.popleft()
        
        if current in visited:
            continue
        
        visited.add(current)
        graph.add_node(current)
        
        new_path = path + [current]
        
        if current[0] == target or current[1] == target:
            return new_path, graph
        
        jug1, jug2 = current
        successors = [
            (capacities[0], jug2),  # Fill jug1
            (jug1, capacities[1]),  # Fill jug2
            (0, jug2),  # Empty jug1
            (jug1, 0),  # Empty jug2
            (max(0, jug1 - (capacities[1] - jug2)), min(capacities[1], jug2 + jug1)),  # Pour jug1 -> jug2
            (min(capacities[0], jug1 + jug2), max(0, jug2 - (capacities[0] - jug1)))   # Pour jug2 -> jug1
        ]
        
        for state in successors:
            if state not in visited and is_valid(state, capacities):
                queue.append((state, new_path))
                graph.add_edge(current, state)
    
    return None, graph

def draw_graph(graph, path):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.show()

if __name__ == "__main__":
    jug1_capacity = int(input("Enter the capacity of Jug 1: "))
    jug2_capacity = int(input("Enter the capacity of Jug 2: "))
    target_amount = int(input("Enter the target amount: "))
    
    path, graph = bfs_water_jug((jug1_capacity, jug2_capacity), target_amount)
    
    if path:
        print("Solution path:", path)
        draw_graph(graph, path)
    else:
        print("No solution found.")
