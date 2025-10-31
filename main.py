from search_algorithms import bfs, dfs, iddfs, best_first, A_star
from graphing_sources import generate_connected_random_graph, generate_random_weighted_graph, is_graph_connected

# set needed variables 
SEED = 42
N_nodes = 50
B_factor = 3
start_node_id = 0
target_node_id = N_nodes -1 

random_graph, random_coordinates = generate_connected_random_graph(
    num_nodes=N_nodes,
    min_weight=2,
    max_weight=10,
    branching_factor = B_factor,
    seed=SEED
)

a_star_path = A_star(
    random_graph, 
    start_node_id,
    target_node_id,
    random_coordinates
)
print(f"A* Path: {a_star_path}")


# 3. Run Best-First Search, passing the coordinates
best_first_path = best_first(
   random_graph,
   start_node_id,
   target_node_id,
   random_coordinates # <--- This is the required addition
)
print("Best-First path:", best_first(random_graph, start_node_id, target_node_id, random_coordinates))