import time
import statistics
import matplotlib.pyplot as plt
import networkx as nx

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
