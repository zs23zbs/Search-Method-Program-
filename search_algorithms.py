from collections import deque 
import heapq # For priority queue 
import math

"""Breadth First Search Function""" 
def bfs(graph, root):
    visited_nodes = set() # Set of nodes that have been visted, no duplicates 
    visit_order = [] 
    queue = deque() # To put nodes in when being visited 

    queue.append(root) # Starting with searching the root of tree, put into queue

    while queue: # while there are still nodes to search for 
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
def DLS(graph, start, target, limit): # Funciton to prevent the algorithm to search too deep into the search space 
    explored = set()

    def helper(node, depth): 
        if depth < 0: # if depth is a negative number 
            return None
        
        if node == target: # if the target node is found in search 
            return [node] # return the path explored
        
        explored.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in explored: 
                path = helper(neighbor, depth - 1) # Recursively reduces the depth of the search space 

                if path is not None: 
                    return [node] + path # build the now found path from start to target node 
            
        return None 
        
    return helper(start, limit - 1) 

def iddfs(graph,start, target, depth_limit):
    for depth in range(depth_limit + 1): # iterate through depth until the end of level of tree
        result = DLS(graph, start, target, depth) 
        if result is not None:
            return result  # returning the path if target is found
    return None

"""Best-First Search""" 

"""
Uses a priority queue 
Heuristic search
Amins to reach the goal from the initial state through the shortest path, being an informed algorithm (Greedy)
Uses two lists for tracking the traversal. 
    Open list that keeps track of the current immediate nodes that are available to be searched 
    Closed list that keeps tracks of the nodes that are already traversed"""

# The Euclidean Hearistics function, for Best First Algorithms informed aspect 
def Euclidean_heuristic(node, target):
   x1, y1 = node 
   x2, y2 = target 

   return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 

def best_first(graph, start_node, target_node):
    openList = []
    heapq.heappush(openList, (Euclidean_heuristic(start_node, target_node), start_node)) # adds item to the heap while maintaining the heap property 
    closedList = set()
    parent = {}

    while openList:
        _, top_node = heapq.heappop(openList) # removes and returns the smallest item from the heap, maintains the heap property 
        closedList.add(top_node)

        if top_node == target_node: 
            path = [] # start building the acutal path 
            while top_node in parent: 
                path.insert(0, top_node)
                top_node = parent[top_node]
            path.insert(0, start_node)
            return path 
        
        for neighbor in graph.get(top_node, []):
            if neighbor not in closedList:
                if not any(neighbor == n for _, n in openList):
                    parent[neighbor] = top_node
                    heapq.heappush(openList, (Euclidean_heuristic(neighbor, target_node), neighbor))

    return None

"""A* Search"""
def a_star_generator(start, goal, graph, coordinates):
    """A* search as a generator for animation."""
    def heuristic(n1, n2):
        lat1, lon1 = coordinates[n1]
        lat2, lon2 = coordinates[n2]
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    open_heap = []
    heapq.heappush(open_heap, (0, start))
    g_scores = {start: 0}
    parents = {start: None}
    visited = set()

    while open_heap:
        f, current = heapq.heappop(open_heap)
        visited.add(current)

        # Yield current state for animation
        yield current, list(visited), [n for _, n in open_heap], parents

        if current == goal:
            # Reconstruct path at the end
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parents[node]
            path.reverse()
            yield "done", path, visited, []
            return

        for neighbor in graph.get(current, []):
            tentative_g = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))
                parents[neighbor] = current

def reconstruct_path(parents, node):
    path = []
    while node is not None:
        path.append(node)
        node = parents.get(node)
    path.reverse()
    return path