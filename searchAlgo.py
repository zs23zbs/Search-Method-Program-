from collections import deque 

search_tree = { # Based on Adjacencies.txt input file, looks as so becuase it is bidirectional (symmetrical)
    "Anthony" : ["Bluff_City", "Argonia", "Harper"],
    "Bluff_City" : ["Anthony", "Kiowa", "South_Haven", "Mayfield"],
    "Kiowa" : ["Bluff_City", "Attica", "Coldwater"],
    "Harper" : ["Anthony", "Attica"],
    "Argonia" : ["Anthony", "Rago", "Caldwell"]
}

"""Breadth First Search Function"""
def bfs(search_tree, root):
    visited_nodes = set() # Set of nodes that have been visted, no duplicates since nodes can't be visited twice 
    visit_order = [] # List for the order of which the nodes are visited 
    queue = deque() # To put nodes in when being visited 

    queue.append(root) # Starting with searching the root of tree, put into queue

    while queue: # while there are still nodes to search for 
        node = queue.popleft() # get the left most node first 
        visit_order.append(node) # add visiting node to the visit order 
        visited_nodes.add(node) # add the now newly visited node into the visited container 

        for child in search_tree.get(node, []): # iterate through the child nodes of the ones that are visited
            if child not in visited_nodes: # if child node is not in queue 
                queue.append(child) # add child node to visit order container
    return visit_order # should return the order of which the nodes were visited 

#print("For Breadth First Search Algorithm: \n", bfs(search_tree,"Anthony"))

"""Depth First Search Function"""
def dfs(search_tree, root_node):
    traversal_list = [] # container for traversal sequence
    nodes_visited = set() # container for all the nodes that've been visited 
    stack = [root_node] #Initiate "stack" with the root of search tree (LIFO)

    while stack: # while there are nodes to visit
        new_node = stack.pop() # pop node from the top of the stack
        if new_node not in nodes_visited: # if the node if not in the visited list 
            traversal_list.append(new_node) # add new node to the traversal life 
            nodes_visited.add(new_node) # add new node is now a visited node
        
            for adjacent_nodes in reversed(search_tree.get(new_node, [])): # ensures LIFO by looking at child/leaf nodes backwards in the search_tree
                if adjacent_nodes not in nodes_visited: # if nodes have not been visited yet 
                    stack.append(adjacent_nodes) # add nodes to the stack 
    return traversal_list

# print("\nFor Depth First Search Algorithm: \n", dfs(search_tree,"Anthony"))

"""Iterative Deepening Depth First Search"""
def DLS(search_tree, start, target, limit):
    explored = set() # container for the visited nodes 

    def helper(node, depth): # new name for helper function
        if depth < 0: # if depth is a negative number 
            return None
        
        if node == target: 
            return [node] # return the path explored
        
        return explored.add(node) # keep adding node to container
        for neighbor in search_tree[node]:
            if neighbor not in explored: 
                path = helper(neighbor, depth-1)

            if path is not None: 
                return [node] + path
            
            return none 
        
    return helper(start, limit - 1)