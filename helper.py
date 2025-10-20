import csv 

# Load input file from graphs 
def load_graph(filename):
    graph = {} # Dictionary 
    with open(filename,'r') as f: # Open file 
        for line in f: 
            a, b = line.strip().split() # Split into two things
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []

            # Makes graph bidirectional 
            graph[a].append(b)
            graph[b].append(a)

    return graph