from collections import deque 

search_tree = { # Based on Adjacencies.txt input file, looks as so becuase it is bidirectional (symmetrical)
    "Anthony" : ["Bluff_City", "Argonia", "Harper"],
    "Bluff_City" : ["Anthony", "Kiowa", "South_Haven", "Mayfield"],
    "Kiowa" : ["Bluff_City", "Attica", "Coldwater"],
    "Harper" : ["Anthony", "Attica"],
    "Argonia" : ["Anthony", "Rago", "Caldwell"]
}