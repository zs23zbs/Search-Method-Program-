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

def run_benchmark():
   """Runs the full benchmarking process and prints the results."""
  
   results = {}
  
   print("\n\n" + "="*80)
   print("--- Starting Batch Benchmarking on Random Graphs ---")
   print("="*80)


   for setting_name, config in benchmark_settings.items():
       print(f"\nRunning setting: {setting_name} (Nodes: {config['N_nodes']}, Branching: {config['B_factor']})")
      
       setting_results = {alg_name: {'runtime': [], 'expanded': [], 'memory': [], 'cost': []}
                          for alg_name in search_algorithms}
      
       for run_id in range(config['N_runs']):
           current_seed = start_seed + run_id
          
           graph, coordinates = generate_connected_random_graph( # create the graph
               num_nodes=config['N_nodes'],
               min_weight=2,
               max_weight=10,
               branching_factor=config['B_factor'],
               seed=current_seed
           )
          
           start_node = 0
           target_node = config['N_nodes'] - 1


           if not graph:
               print(f"Skipping run {run_id}: Graph generation failed.")
               continue

           for alg_name, alg_config in search_algorithms.items(): # run the algorithms 
               algorithm = alg_config['func']
               is_informed = alg_config['informed']


               start_time = time.time()
              
               if is_informed:
                   path, expanded, memory = algorithm(graph, start_node, target_node, coordinates)
               else:
                   if alg_name == "IDDFS":  # deal with IDDFS's extra depth_limit
                       path, expanded, memory = algorithm(graph, start_node, target_node, config['N_nodes'])
                   else:
                       path, expanded, memory = algorithm(graph, start_node, target_node)
              
               end_time = time.time()
               runtime = (end_time - start_time) * 1000 # Convert to milliseconds


               cost = calculate_path_cost(graph, path) if path else float('inf')


               setting_results[alg_name]['runtime'].append(runtime)
               setting_results[alg_name]['expanded'].append(expanded)
               setting_results[alg_name]['memory'].append(memory)
               setting_results[alg_name]['cost'].append(cost)


       results[setting_name] = setting_results # the average + result of running the setting


   # process and display the results 
   print("\n\n" + "="*80)
   print("FINAL BENCHMARK RESULTS (Mean ± Std Dev)")
   print("="*80)
  
   for setting_name, setting_results in results.items(): # calculating + printing the stats for each setting 
       print(f"\n--- Complexity Setting: {setting_name} ---")
       header = f"{'Algorithm':<12} | {'Runtime (ms)':<20} | {'Nodes Expanded':<20} | {'Peak Memory (Units)':<20} | {'Path Cost':<10}"
       print('-' * len(header))
       print(header)
       print('-' * len(header))


       for alg_name, metrics in setting_results.items():
          
           def safe_stats(data):
               if not data: return "N/A"
               mean = statistics.mean(data)
               stdev = statistics.stdev(data) if len(data) > 1 else 0.0
               return f"{mean:.2f} ± {stdev:.2f}"


           runtime_stats = safe_stats(metrics['runtime'])
           expanded_stats = safe_stats(metrics['expanded'])
           memory_stats = safe_stats(metrics['memory'])
          
           # taking the mean of the runs for the cost
           successful_costs = [c for c in metrics['cost'] if c != float('inf')]
           mean_cost = statistics.mean(successful_costs) if successful_costs else "Inf"


           print(f"{alg_name:<12} | {runtime_stats:<20} | {expanded_stats:<20} | {memory_stats:<20} | {mean_cost:<10}")

if __name__ == "__main__":
   seed = 42
   Nnodes = 50
   Bfactor = 3
   start_node_id = 0
   target_node_id = Nnodes - 1

   random_graph, random_coordinates = generate_connected_random_graph(
       num_nodes=Nnodes,
       min_weight=2,
       max_weight=10,
       branching_factor=Bfactor,
       seed=seed
   )

   if random_graph:
       # A* search for path visualization 
       a_star_results = A_star(
           random_graph,
           start_node_id,
           target_node_id,
           random_coordinates
       )
       a_star_path, _, _ = a_star_results
       a_star_cost = calculate_path_cost(random_graph, a_star_path)
       print(f"A* Path: {a_star_path}")
       print(f"A* Path Cost: {a_star_cost:.2f}")

       # best_first for comparisons
       best_first_results = best_first(
           random_graph,
           start_node_id,
           target_node_id,
           random_coordinates
       )
       best_first_path, _, _ = best_first_results
       best_first_cost = calculate_path_cost(random_graph, best_first_path)
       print(f"Best-First Path: {best_first_path}")
       print(f"Best-First Path Cost: {best_first_cost:.2f}")  

       # make the visualization 
       visual_graph(random_graph, random_coordinates, a_star_path,"A_star_visual_path.png")

       # running the batch benchmarking 
       run_benchmark()