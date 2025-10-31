from collections import deque
import heapq # to help with the priority queue 
import math

"""Breadth First Search Function""" 
def bfs(graph, root, target):
    nodes_expanded = 0
    peak_memory_usage = 0
    
    visited_nodes = {root} # Set of nodes that have been visted, no duplicates 
    queue = deque([root]) # To put nodes in when being visited, top of the queue is of highest priority
    parent = {}

    while queue: # while there are still nodes to search for, put into visit order + add as visited nodes
        current_memory = len(queue) + len(visited_nodes)
        peak_memory_usage = max(peak_memory_usage, current_memory)

        node = queue.popleft()
        nodes_expanded += 1

        if node == target: 
            path = reconstructed_path(node, parent)
            return path, nodes_expanded, peak_memory_usage

        for child, _ in graph.get(node, []): # iterate through the child nodes of the ones that are visited
            if child not in visited_nodes:
                visited_nodes.add(child)
                parent[child] = node
                queue.append(child) 

    return None, nodes_expanded, peak_memory_usage # should return the order of which the nodes were visited 

"""Depth First Search Function"""
def dfs(graph, root_node, target):
    nodes_expanded = 0
    peak_memory_usage = 0

    nodes_visited = set() # container for all the nodes that've been visited 
    stack = [(root_node, None)] #Initiate "stack" with the root of search tree (LIFO)
    parent = {}

    while stack: # while there are nodes to visit
        current_memory = len(stack) + len(nodes_visited)
        peak_memory_usage = max(peak_memory_usage, current_memory)

        new_node, parent_node  = stack.pop() 

        if new_node not in nodes_visited: 
            nodes_expanded += 1 # <--- ADDED (Node is expanded)
            nodes_visited.add(new_node)

            if parent_node is not None: 
                parent[new_node] = parent_node

            if new_node == target:
                path = reconstructed_path(new_node, parent)
                return path, nodes_expanded, peak_memory_usage
        
            for adjacent_nodes, _ in reversed(graph.get(new_node, [])): # ensures LIFO by looking at child/leaf nodes backwards in the search_tree
                if adjacent_nodes not in nodes_visited:
                    stack.append((adjacent_nodes, new_node)) 

    return None, nodes_expanded, peak_memory_usage

"""Iterative Deepening Depth First Search""" 
def DLS(graph, start, target, limit, visitied_path): 
    if limit < 0:
        return None, 0
    if start == target:
        return [start], 1
    
    visitied_path.add(start) # track the path visited thus far

    expanded_in_depth = 1

    for neighbor, _ in graph.get(start, []): 
        if neighbor not in visitied_path: 
            path, expanded_sub = DLS(graph, neighbor, target, limit - 1, visitied_path)
            expanded_in_depth += expanded_sub

            if path is not None:
                return [start] + path, expanded_in_depth
    visitied_path.remove(start)
    return None, expanded_in_depth
 
def iddfs(graph,start, target, depth_limit):
    total_expanded = 0

    for depth in range(depth_limit + 1): # iteratively increaed the depth limit
        visited_path = set()

        result_path, expanded_in_depth = DLS(graph, start, target, depth, visited_path)
        total_expanded += expanded_in_depth 

        if result_path is not None:
            peak_memory_prox = depth
            return result_path, total_expanded, peak_memory_prox
        
    return None, total_expanded, 0

"""Best-First Search"""
#Heuristic Function - Using the Euclidean Distance 
def Eculidean_heuristic(node_id, target_id, coordinates):
    # Just in case, handle any errors 
    try: 
        x1, y1 = coordinates[node_id]
        x2, y2 = coordinates[target_id]

    except KeyError: 
        # Error for where a node might not have coordinates for whatever reason
        return float('inf')
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) # return the calculated value of Euclidean distance 

"""def best_first(graph, start_node, target_node, coordinates):
    nodes_expanded = 0
    peak_memory_usage = 0
    
    openList = [] 
    h_start = Eculidean_heuristic(start_node, target_node, coordinates)
    heapq.heappush(openList, (h_start, start_node))

    inside_openList = {start_node}
    closedList = set()
    parent = {}

    while openList:
        current_memory = len(openList) + len(closedList)
        peak_memory_usage = max(peak_memory_usage, current_memory)

        _, top_node = heapq.heappop(openList) # removing based on heurisitc value, one's closer to the goal  
        closedList.add(top_node)

        if top_node == target_node: # if target node is found, make a new path from target to start and use parent to move backwards to create start to target path order
            path = reconstructed_path(top_node, parent)
            return path, nodes_expanded, peak_memory_usage

        for neighbor, _ in graph.get(top_node, []): # for neighboring nodes of top_node
            if neighbor not in closedList:
                if not any(neighbor == n for _, n in openList): # if not any node in openList whose node is equal to neighbor
                    parent[neighbor] = top_node
                    h_neighbor = Eculidean_heuristic(neighbor, target_node, coordinates) 
                    heapq.heappush(openList, (h_neighbor, neighbor)) # add neighbor to openList along with its calculated h value, ensure that lower h values (closer to target) are prioritized
                    inside_openList.add(neighbor)

    return None, nodes_expanded, peak_memory_usage
"""

def best_first(graph, start_node, target_node, coordinates):
    nodes_expanded = 0
    peak_memory_usage = 0
    
    h_start = Eculidean_heuristic(start_node, target_node, coordinates)
    openList = [(h_start, start_node)]

    closedList = set()
    parent = {}

    while openList:
        current_memory = len(openList) + len(closedList)
        peak_memory_usage = max(peak_memory_usage, current_memory)

        _, current_node = heapq.heappop(openList)

        if current_node in closedList:
            continue 

        nodes_expanded += 1
        closedList.add(current_node)

        if current_node == target_node:
            path = reconstructed_path(current_node, parent)
            return path, nodes_expanded, peak_memory_usage
        
        for neighbor, _ in graph.get(current_node, []):
            if neighbor not in closedList:
                h_neighbor = Eculidean_heuristic(neighbor, target_node, coordinates)
                if neighbor not in parent: 
                    parent[neighbor] = current_node

                heapq.heappush(openList, (h_neighbor, neighbor))

    return None, nodes_expanded, peak_memory_usage

"""A* Search"""
def A_star(graph, start_node, target_node, coordinates):
    nodes_expanded = 0 
    peak_memory_usage = 0

    OPENlist = []
    CLOSEDlist = set()

    # Create the start and current nodes
    g_score = {node: float('inf') for node in graph} # new dicionary to represent cost ('inf') of path from start to target
    g_score[start_node] = 0 # cost for start_node is zero 

    # Total estimated cost, help decided which path to explore 
    f_score = {node: float('inf') for node in graph}
    f_score[start_node] = Eculidean_heuristic(start_node, target_node, coordinates) 

    heapq.heappush(OPENlist, (f_score[start_node], start_node))
    parent = {}

    while len(OPENlist) > 0: # make sure the list is not empty
        current_memory = len(OPENlist) + len(CLOSEDlist) # <--- ADDED/CHANGED
        peak_memory_usage = max(peak_memory_usage, current_memory)

        current_f, current_node = heapq.heappop(OPENlist)
        nodes_expanded += 1

        if current_node == target_node: 
            return reconstructed_path(current_node, parent), nodes_expanded, peak_memory_usage

        if current_node in CLOSEDlist:
            continue 

        CLOSEDlist.add(current_node)

        for neighbor, weigth in graph.get(current_node, []):
            if neighbor in CLOSEDlist: 
                continue 

            tentative_g = g_score[current_node] + weigth # g(n) = cost to reach the curent node + move cost to the neighbor 

            if tentative_g < g_score.get(neighbor, float('inf')): # check if path is better to explore
                parent[neighbor] = current_node
                g_score[neighbor] = tentative_g

                h = Eculidean_heuristic(neighbor, target_node, coordinates)
                new_f_score = tentative_g
                f_score[neighbor] = new_f_score

                heapq.heappush(OPENlist, (new_f_score, neighbor))
    
    return None, nodes_expanded, peak_memory_usage

def reconstructed_path(current_node, parent):
    path = [current_node]
    while current_node in parent: 
        current_node = parent[current_node]
        path.insert(0, current_node)
    return path 
