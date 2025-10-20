from helper import load_graph, load_coordinates_csv, graph_visualization

# for the single search option 
def single_search(graph, coordinates):
    print(f"Load {len(graph)} nodes from the adjacency list.")
    print(f"Load {len(coordinates)} coordinates. \n")

    # print out the available cities 
    print("Available Cities:")
    print(", ".join(sorted(graph.keys())))

    # user input 
    start = input("\n Please enter the start city: ").strip()
    goal = input("Please enter the target city: ").strip()

    if start not in graph or goal not in graph: 
        print("Invalid entry. Please try again")
        exit(1)