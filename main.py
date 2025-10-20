from helper import load_graph, load_coordinates_csv, graph_visualization
import time 
from search_algorithms import bfs, dfs, iddfs, best_first, a_star_generator

# for the single search option 
def single_search(graph, coordinates):
    print(f"Load {len(graph)} nodes from the adjacency list.")
    print(f"Load {len(coordinates)} coordinates. \n")

    # print out the available cities 
    print("Available Cities:")
    print(", ".join(sorted(graph.keys())))

    # user input (invalid entry)
    start = input("\n Please enter the start city: ").strip()
    goal = input("Please enter the target city: ").strip()

    if start not in graph or goal not in graph: 
        print("Invalid entry. Please try again")
        exit(1)

    # print algorithm menu 
    print("""\nAlgorithms Menu:
          1. BFS
          2. DFS
          3. IDDFS
          4. Best-First
          5. A*""")
    user_choice = input("Select an algorithm of your choice [1-5]: ").strip()

    path = []
    visited_nodes = []
    start_time = time.perf_counter()

    # run the selection search (if-else)
    if user_choice == "1":
        bfs_graph = bfs(graph, start)
        if goal in bfs_graph: 
            goal_indx = bfs_graph.index(goal) + 1
            path = bfs_graph[:goal_indx]
        else: 
            path = bfs_graph
        visited_nodes =bfs_graph

    elif user_choice == "2":
        dfs_graph = dfs(graph, start)
        if goal in dfs_graph:
            goal_indx = dfs_graph.index(goal) + 1
            path = dfs_graph[goal_indx]
        else: 
            path = dfs_graph
        visited_nodes = dfs_graph
    
    elif user_choice == "3":
        path = iddfs(graph, start,goal, depth_limit=10)
        visited_nodes = path if path else []
    
    elif user_choice == "4":
        path = best_first(graph, start, goal)
        visited_nodes = path if path else []
    
    elif user_choice == "5":
        a_star_gen = a_star_generator(graph,start, goal, coordinates)

        for step in a_star_gen:
            current = step[0]
            if current == "done":
                path = list(step[1])
                visited_nodes = set(step[2])
                break
            visited_nodes = set(step[1])
    else: 
        print("Invalid choice, Default to BFS")
        path = bfs(graph, start, goal)
        visited_nodes = path
    
    elasped = time.perf_counter() - start_time

    # print the results 
    if path:
        print(f"\nShortest path from {start} to {goal}: ")
        print(" ->".join(path))
        print(f"Path Length: {len(path)}")
        print(f"Runtime: {elasped:.4f}s")
    else: 
        print("No path was found")

    # creating visualization 
    graph_visualization(graph, coordinates, path=path, visited_nodes=visited_nodes, frontier_node=[])