import csv
import random
from collections import deque

"""Load the Adjacencies.txt file"""
def load_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        for line in file: 
            a, b = line.strip().split() # collect the first and second city
            if a not in graph: 
                graph[a] = []
            if b not in graph: 
                graph[b] = []

            # Make the graph bidirection
            graph[a].append(b)
            graph[b].append(a)

    return graph

"""Load the csv coordinates (1).txt file"""
def load_coordinates_csv(filename):
    coordinates = {}
    with open(filename, newline='') as csvfile:
        read = csv.reader(csvfile)
        for row in read: # each row in csv, store the corresponding variables 
            city = row[0].strip()
            latitude = float(row[1])
            longitude = float(row[2])

            coordinates[city] = (latitude, longitude) # assign the tuple values (latitude and longitude) to the city (key of pair) into coordinates dictionary
    return coordinates

"""For random graph generator"""
def generate_random_weighted_graph(num_nodes=10, branching_factor=2, min_weight=1, max_weight=10, seed=None):
    if seed is not None:
        random.seed(seed)
    
    graph = {i: [] for i in range(num_nodes)} # created some isolated nodes

    coordinates = {
        node: (random.randint(0, 1000), random.randint(0, 1000))
        for node in range(num_nodes)
    }

    # makes sure that the graph is connected 
    for node in range(1, num_nodes):
        connect_to =random.randint(0, node - 1)
        weight = random.randint(min_weight, max_weight)

        # make an edge from node to connect_to 
        graph[node].append(connect_to, weight)

        # make an edge from connect_to to node 
        if not any(entry[0] == node for entry in graph[connect_to]):
            graph[connect_to].append(node, weight)

    target_edges = int(num_nodes * branching_factor /2)
    current_edges = sum(len(graph[i]) for i in range(num_nodes) // 2) # count the unique edges 
    edges_to_add = max(0, target_edges - current_edges)

    for _ in range(edges_to_add):
        a, b = random.smaple(range(num_nodes), 2)
        weigth = random.randint(min_weight, max_weight)
        if a != b and b not in [n for n, _ in graph[a]]:
            graph[a].append((b, weight))
            graph[b].append((a, weight))

    return graph, coordinates 

def is_graph_connected(graph):
    if not graph: # just to check 
        return False
    
    start = next(iter(graph))
    visited = set()
    queue = deque([start])
    while queue: 
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    queue.appedn(neighbor)

    return len(visited) == len(graph)

def generate_connected_random_graph(num_nodes=10, branching_factor=2, min_weight=1, max_weight=10, seed=None):
   """Generates a connected random graph and its coordinates"""
  
   local_random = random.Random(seed)
   max_attempts = 100


   for attempt in range(max_attempts):
       current_seed = seed + attempt if seed is not None else local_random.randint(1, 10000)


       # generate_random_weighted_graph MUST return (graph, coordinates)
       graph, coordinates = generate_random_weighted_graph(
           num_nodes, branching_factor, min_weight, max_weight, seed=current_seed
       )
      
       if is_graph_connected(graph):
           print(f"Random connected graph generated after {attempt + 1} attempt(s) with seed {current_seed}")
           # Correct Return: Tuple of 2 values
           return graph, coordinates
      
   print(f"Warning: Could not guarantee a connected graph after {max_attempts} attempts.")
   # Correct Return (Failure Path): Must also return a Tuple of 2 values