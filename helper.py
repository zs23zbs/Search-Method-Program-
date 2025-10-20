import csv 

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
        for row in read:
            if row[0].lower() == "city": # Skip the header with row label "city"
                continue
            city = row[0].strip()
            latitude = float(row[1])
            longitude =  float(row[2])
            coordinates[city] (latitude, longitude)
            
    return coordinates