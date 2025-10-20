import csv 
import networkx as nx
import matplotlib.pyplot as plt 

# Load input file from graphs 
def load_graph(filename):
    graph = {} # Dictionary 
    with open(filename,'r') as f: # Open file 
        for line in f: 
            a, b = line.strip().split() # Collects first and second city 
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []

            # Makes graph bidirectional 
            graph[a].append(b)
            graph[b].append(a)

    return graph

# Load coordinates from CSV file 
def load_coordinates_csv(filename):
    coordinates = {}
    with open(filename, newline='') as csvfile: 
        read = csv.reader(csvfile)
        for row in read: # get each city with their corresponding latitudes and longitudes and store them into coordinates
            city = row[0].strip()
            latitude = float(row[1])
            longitude =  float(row[2])
            coordinates[city] = (latitude, longitude)

    return coordinates

def graph_visualization(graph, coordinates, path=None, visited_node=None, frontier_node=None):

    G = nx.Graph() 
    # iterate through dictionary, both key and value. Create edge betwen two nodes 
    for nodes, neighbors in graph.items():
        for n in neighbors: 
            G.add_edge(nodes, n)

    position = coordinates

    # create layout of graph 
    figure, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.2)

    # draw the base edges
    nx.draw_networkx_edges(G, position, alpha=0.3, ax=ax)
    nx.draw_networkx_labels(G, position, font_size=8, ax=ax)

     # the animation control variables 
    frame_index = [0]
    paused = [False]

    # convert the visited_nodes into lists if a set 
    if visited_node:
        visited_list = list(visited_node)
    else: 
        visited_list = [] 