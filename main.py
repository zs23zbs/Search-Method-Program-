import time
import statistics
import matplotlib.pyplot as plt
import networkx as nx

from search_algorithms import bfs, dfs, iddfs, best_first, A_star
from graphing_sources import generate_connected_random_graph

def calculate_path_cost(graph, path):
    if not path or len(path) < 2:
        return 0.0 
    
    total_cost = 0.0 

    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]

        found_weight = False 

        #find the weight of the edge from the current node to the next one
        for neighbor, weight in graph.get(current_node, []):
            if neighbor == next_node: 
                total_cost += weight
                found_weight = True
                break
        if not found_weight: # shouldn't happen in a connected, bidirectional graph but just in case
            print(f"Error!!: An edge was not found between {current_node} and {next_node}")
            return float('inf')
    
    return total_cost

"""The Visualization Function"""
def visual_graph(graph, coordinates, path, filename="A_star_visual_path.png"):
    G = nx.Graph()
    edge_weights = {}

    for node, edges in graph.items():
        for neighbor, weight in edges:
            if node < neighbor: # add an edge one time for the undirected graph
                G.add_edge(node, neighbor, weight=weight)
                edge_weights[(node, neighbor)] = f"{weight:.1f}"
    
    # Find the node positions (using the coordinates)
    pos = coordinates

    # Take care of the colors and labels 
    node_colors = ['lightblue' for _ in range(len(coordinates))]
    if path: 
        for node in path:
            if node in coordinates:
                node_colors[node] = 'orange'

        # identifying the start and target nodes being different 
        if path[0] in coordinates: node_colors[path[0]] = 'green'
        if path[-1] in coordinates: node_colors[path[-1]] = 'red'

    # the path edges 
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        is_path_edge = (u, v) in path_edges or (v, u) in path_edges # check if the edges (u, v) or (v, u) is in path 
        edge_colors.append('purple' if is_path_edge else 'gray')
        edge_widths.append(3 if is_path_edge else 1)
    
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500) # drawing the nodes
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths) # drawing the edges 
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold') # drawing the labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_color='blue') # drawing the edge weights + label the edges with the weights 
    plt.title(f"A* Path Visualization (Cost: {calculate_path_cost(graph, path) :.2f})")
    plt.axis('off')
    plt.savefig(filename)
    print(f"\n+++ Visualization was successfully saved to {filename} +++")

search_algorithms = {
   "BFS": {'func': bfs, 'informed': False},
   "DFS": {'func': dfs, 'informed': False},
   "IDDFS": {'func': iddfs, 'informed': False},
   "Best-First": {'func': best_first, 'informed': True},
   "A*": {'func': A_star, 'informed': True},
}

# Setting up the benchmarking 
benchmark_settings = {
   "Easy": {"N_nodes": 20, "B_factor": 2, "N_runs": 5},
   "Medium": {"N_nodes": 50, "B_factor": 3, "N_runs": 5},
   "Hard": {"N_nodes": 100, "B_factor": 4, "N_runs": 5},
}

start_seed = 100