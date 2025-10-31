import csv

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