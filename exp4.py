import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt

def a_star_water_jug(jug1, jug2, target):
    def heuristic(state):
        return abs(state[0] - target) + abs(state[1] - target)
    
    start = (0, 0)
    queue = [(heuristic(start), 0, start, [])]
    visited = set()
    total_cost = 0
    
    print("\nRules of the Water Jug Problem:")
    print("1. You can fill a jug to its full capacity.")
    print("2. You can empty a jug completely.")
    print("3. You can transfer water from one jug to another until the receiving jug is full or the pouring jug is empty.")
    print("\nSolution Steps:")
    
    while queue:
        _, cost, (a, b), path = heapq.heappop(queue)
        if (a, b) in visited:
            continue
        visited.add((a, b))
        path = path + [(a, b)]
        total_cost = cost
        print(f"Current State: Jug1 = {a}, Jug2 = {b}, Cost = {cost}")
        
        if a == target or b == target:
            print(f"\nTotal Cost of Operations: {total_cost}")
            return path, total_cost
        
        possible_moves = [
            (jug1, b),  # Fill jug1
            (a, jug2),  # Fill jug2
            (0, b),     # Empty jug1
            (a, 0),     # Empty jug2
            (a - min(a, jug2 - b), b + min(a, jug2 - b)),  # Pour jug1 to jug2
            (a + min(b, jug1 - a), b - min(b, jug1 - a))   # Pour jug2 to jug1
        ]
        
        for move in possible_moves:
            if move not in visited:
                heapq.heappush(queue, (cost + heuristic(move), cost + 1, move, path))
    return None, None

def generate_sparse_graph(n=20, density=0.2):
    # Create an empty graph
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # Generate edges until we reach desired density
    target_edges = int(n * (n-1) * density / 2)
    edges_added = 0
    
    # Ensure graph is connected first
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(len(nodes)-1):
        weight = random.randint(1, 20)
        G.add_edge(nodes[i], nodes[i+1], weight=weight)
        edges_added += 1
    
    # Add random edges until desired density
    while edges_added < target_edges:
        u, v = random.sample(range(n), 2)
        if not G.has_edge(u, v):
            weight = random.randint(1, 20)
            G.add_edge(u, v, weight=weight)
            edges_added += 1
    
    # Convert to dictionary format
    graph_dict = {i: {} for i in range(n)}
    for (u, v, w) in G.edges.data('weight'):
        graph_dict[u][v] = w
        graph_dict[v][u] = w
    
    return graph_dict, G

def a_star_sparse_graph(graph, start, goal):
    def heuristic(node):
        return abs(goal - node)
    
    queue = [(heuristic(start), 0, start, [])]
    visited = set()
    
    while queue:
        _, cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        
        if node == goal:
            return path, cost
        
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight + heuristic(neighbor), cost + weight, neighbor, path))
    return None, None

def display_graph(G, shortest_path, start, goal):
    # Dramatically increased figure size for maximum spacing
    plt.figure(figsize=(20, 16))
    
    # Increased k parameter significantly for maximum node separation
    pos = nx.spring_layout(G, k=5.0, iterations=200, seed=42)
    
    # Draw the base graph with increased spacing and sizes
    nx.draw(G, pos, with_labels=True, 
            node_color='lightblue',
            edge_color='gray',
            node_size=1200,        # Larger nodes
            font_size=14,          # Larger node labels
            width=1.5,             # Slightly thicker edges
            alpha=0.9)             # Slightly more opaque
    
    # Draw edge weights with more space and larger font
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, 
                                edge_labels=edge_labels,
                                font_size=12,      # Larger weight labels
                                label_pos=0.5,     # Centered on edges
                                bbox=dict(facecolor='white', 
                                        edgecolor='none',
                                        alpha=0.7,  # Background for weight labels
                                        pad=2))
    
    # Draw the shortest path if it exists
    if shortest_path and len(shortest_path) > 1:
        path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, 
                             edgelist=path_edges,
                             edge_color='red',
                             width=3.5)
    
    # Highlight start and goal nodes with larger sizes
    nx.draw_networkx_nodes(G, pos, 
                          nodelist=[start],
                          node_color='green',
                          node_size=1500)
    nx.draw_networkx_nodes(G, pos,
                          nodelist=[goal],
                          node_color='orange',
                          node_size=1500)
    
    plt.title("Sparse Graph with Shortest Path", 
              pad=20,
              size=16,
              fontweight='bold')
    
    # Added more padding around the graph
    plt.margins(0.2)
    
    # Increased legend size and moved it outside the graph
    plt.legend(['Nodes', 'Start Node', 'Goal Node', 'Shortest Path'],
              fontsize=12,
              bbox_to_anchor=(1.1, 1.05))
    
    plt.axis('off')
    # Adjusted layout to account for legend
    plt.tight_layout()
    plt.show()

def main():
    # Water Jug Problem
    print("Water Jug Problem Solver")
    print("-----------------------")
    jug1_capacity = int(input("Enter capacity of first jug: "))
    jug2_capacity = int(input("Enter capacity of second jug: "))
    target_amount = int(input("Enter target amount: "))
    
    solution, water_cost = a_star_water_jug(jug1_capacity, jug2_capacity, target_amount)
    if solution:
        print("\nWater Jug Solution Path:", solution)
    else:
        print("\nNo solution exists for the given parameters.")

    # Sparse Graph Problem
    print("\nSparse Graph Problem Solver")
    print("-------------------------")
    graph_dict, G = generate_sparse_graph()
    start_node, goal_node = random.sample(range(20), 2)
    print(f"Randomly Selected Start Node: {start_node}, Goal Node: {goal_node}")
    
    shortest_path, path_cost = a_star_sparse_graph(graph_dict, start_node, goal_node)
    if shortest_path:
        print(f"\nShortest Path Found: {' -> '.join(map(str, shortest_path))}")
        print(f"Total Path Cost: {path_cost}")
        display_graph(G, shortest_path, start_node, goal_node)
    else:
        print(f"\nNo path exists between nodes {start_node} and {goal_node}")

if __name__ == "__main__":
    main()