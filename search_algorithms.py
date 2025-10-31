from collections import deque
import heapq # to help with the priority queue 
import math

"""Breadth First Search Function""" 
def bfs(graph, root):
    visited_nodes = set() # Set of nodes that have been visted, no duplicates 
    visit_order = [] 
    queue = deque() # To put nodes in when being visited, top of the queue is of highest priority

    queue.append(root) # Starting with searching the root of tree, put into queue

    while queue: # while there are still nodes to search for, put into visit order + add as visited nodes
        node = queue.popleft()
        visit_order.append(node)
        visited_nodes.add(node) 

        for child in graph.get(node, []): # iterate through the child nodes of the ones that are visited
            if child not in visited_nodes:
                queue.append(child) 

    return visit_order # should return the order of which the nodes were visited 

"""Depth First Search Function"""
def dfs(graph, root_node):
    traversal_list = [] # container for traversal sequence
    nodes_visited = set() # container for all the nodes that've been visited 
    stack = [root_node] #Initiate "stack" with the root of search tree (LIFO)

    while stack: # while there are nodes to visit
        new_node = stack.pop() 
        if new_node not in nodes_visited: 
            traversal_list.append(new_node) 
            nodes_visited.add(new_node) 
        
            for adjacent_nodes in reversed(graph.get(new_node, [])): # ensures LIFO by looking at child/leaf nodes backwards in the search_tree
                if adjacent_nodes not in nodes_visited:
                    stack.append(adjacent_nodes) 

    return traversal_list

"""Iterative Deepening Depth First Search""" 
def DLS(graph, start, target, limit): # Funciton to prevent the algorithm to search too deep into the search space, prevent unecessary searching
    explored = set() # keeps tracks of hte nodes that are visited to avoid of cycles, should reset at each depth 

    def helper(node, depth): 
        if depth < 0: # if depth is a negative number, prevents recursions from the function going any deeper than needed 
            return None
        
        if node == target: # if the target node is found in search 
            return [node] # return the path explored from the target node (used for backtracking)
        
        explored.add(node)

        for neighbor in graph.get(node, []): 
            if neighbor not in explored: 
                path = helper(neighbor, depth - 1) # For each neighbor not explored yet at current depth, recurse the depth by decreasing by 1
                if path is not None:
                    return [node] + path # build the now found path from start to target node 
            
        return None 
        
    return helper(start, limit - 1) 

def iddfs(graph,start, target, depth_limit):
    for depth in range(depth_limit + 1): # iteratively increaed the depth limit
        result = DLS(graph, start, target, depth) # At each depth, call the DLS function 
        if result is not None:
            return result  # returning the path if target is found
    return None

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

def best_first(graph, start_node, target_node, coordinates):
    openList = [] 
    h_start = Eculidean_heuristic(start_node, target_node, coordinates)
    heapq.heappush(openList, (h_start, start_node))

    closedList = set()
    parent = {}

    while openList:
        _, top_node = heapq.heappop(openList) # removing based on heurisitc value, one's closer to the goal  
        closedList.add(top_node)

        if top_node == target_node: # if target node is found, make a new path from target to start and use parent to move backwards to create start to target path order
            path = []
            current = top_node 
            while current in parent: 
                path.insert(0, current)
                current = parent[current]
            path.insert(0, start_node)
            return path

        for neighbor, _ in graph.get(top_node, []): # for neighboring nodes of top_node
            if neighbor not in closedList:
                if not any(neighbor == n for _, n in openList): # if not any node in openList whose node is equal to neighbor
                    parent[neighbor] = top_node
                    h_neighbor = Eculidean_heuristic(neighbor, target_node, coordinates) 
                    heapq.heappush(openList, (h_neighbor, neighbor)) # add neighbor to openList along with its calculated h value, ensure that lower h values (closer to target) are prioritized
    return None

"""A* Search"""
def A_star(graph, start_node, target_node, coordinates):
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
        current_f, current_node = heapq.heappop(OPENlist)

        if current_node == target_node: 
            return reconstructed_path(current_node, parent)

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
                f_score[neighbor] = tentative_g + h

                heapq.heappush(OPENlist, (f_score[neighbor], neighbor))
    return None

def reconstructed_path(current_node, parent):
    path = [current_node]
    while current_node in parent: 
        current_node = parent[current_node]
        path.insert(0, current_node)
    return path 