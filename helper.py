import csv 
import networkx as nx
import matplotlib.pyplot as plt 
from matplotlib.widgets import Button, Slider

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
    # for every node and its neighbors, make an edge 
    for nodes, neighbors in graph.items():
        for n in neighbors: 
            G.add_edge(nodes, n)

    position = coordinates

    # create layout window of graph 
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.2)

    # draw the base edges in graph, at position
    nx.draw_networkx_edges(G, position, alpha=0.3, ax=ax)
    nx.draw_networkx_labels(G, position, font_size=8, ax=ax)

     # the animation control variables, step of animation & pause/resume
    frame_index = [0]
    paused = [False]

    if visited_node:
        visited_list = list(visited_node)
    else: 
        visited_list = [] 
    
     # function to update to frame
    def update(frame):
        # clear and then draw edges for every frame 
        ax.clear()
        nx.draw_networkx_edges(G, position, alpha=0.3, ax=ax)
        nx.draw_networkx_labels(G, position, font_size=8, ax=ax)

        # draw the visited nodes to the current frame 
        if visited_list:
            nx.draw_networkx_nodes(G, position,
                nodelist = visited_list[:frame+1],
                node_color = "lightblue",
                label = "Visited",
                ax=ax
            )
        # draw the frontier nodes if there are any 
        if frontier_node:
            nx.draw_networkx_nodes(G, position,
             nodelist=frontier_node,
             node_color= "yellow",
             label="Frontier",
             ax=ax
             )
            
        # draw final path
        if path:
            nx.draw_networkx_nodes(G, position,
                nodelist=path,
                node_color="red",
                label="Path",
                ax=ax
            )
            path_edges = list(zip(path[:-1], path[1:])) # drawing nodes along the path 
            nx.draw_networkx_edges(G, position, edgelist=path_edges,width=3, edge_color="red", ax=ax)

        ax.set_title("Visualization for Graph")
        ax.axis("off")
        ax.legend(scatterpoints=1)
    
    #for the buttons
    def while_paused(event):
        paused[0] = not paused[0]
    
    def restarting(event):
        frame_index[0] = 0
        update(0)
        plt.draw()

    def on_step(event):
        if frame_index[0] < len(visited_list) -1:
            frame_index[0] += 1
            update(frame_index[0])
            plt.draw()
    
    # slider button
    def on_slider(val):
        index = int(speed_slider.val)
        update(index)
        plt.draw()

    # pause button
    ax_pause = plt.axes([0.7, 0.03, 0.1, 0.03])
    pause_button = Button(ax_pause, "Play/Plause")
    pause_button.on_clicked(while_paused)

    # step button
    ax_step = plt.axes([0.81, 0.05, 0.1, 0.05])
    step_button = Button(ax_step, "Step")
    step_button.on_clicked(on_step)

    # restart button
    ax_restart = plt.axes([0.59, 0.05, 0.1, 0.05])
    restart_button = Button(ax_restart, "Restart")
    restart_button.on_clicked(restarting)

    # slider speed button
    ax_slider = plt.axes([0.1, 0.05, 0.4, 0.05])
    speed_slider = Slider(ax_slider, "Frame", 0, max(len(visited_list) -1, 1), valinit=0, valstep=1)
    speed_slider.on_changed(on_slider)

    # loop for automatic play
    while True: 
        if not paused[0] and frame_index[0] < len(visited_list) -1:
            frame_index[0] += 1
            update(frame_index[0])
            speed= 0.5 
            plt.pause(speed)
        plt.pause(0.01)