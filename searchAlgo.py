from collections import deque 

search_tree = { # Based on Adjacencies.txt input file, looks as so becuase it is bidirectional (symmetrical)
    "Anthony" : ["Bluff_City", "Argonia", "Harper"],
    "Bluff_City" : ["Anthony", "Kiowa", "South_Haven", "Mayfield"],
    "Kiowa" : ["Bluff_City", "Attica", "Coldwater"],
    "Harper" : ["Anthony", "Attica"],
    "Argonia" : ["Anthony", "Rago", "Caldwell"]
}

"""Breadth First Search Function"""
def bfs (search_tree, root):
    visited_nodes = set() # Set of nodes that have been visted, no duplicates since nodes can't be visited twice 
    visit_order = [] # List for the order of which the nodes are visited 
    queue = deque() # To put nodes in when being visited 

    queue.append(root) # Starting with searching the root of tree, put into queue

    while queue: # while there are still nodes to search for 
        node = queue.popleft() # get the left most node first 
        visit_order.append(node) # add visiting node to the visit order 
        visited_nodes.append(node) # add the now newly visited node into the visited container 

        for child in search_tree[child]: # iterate through the child nodes of the ones that are visited 
            if child not in queue: # if child node is not in queue 
                visit_order.append(child) # add child node to visit order container
    return visit_order         