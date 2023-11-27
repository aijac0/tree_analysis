from typing import Iterable
from collections import deque
from exploratory.basic.trees import Tree

def enumerate_tree_paths(trees : Iterable[Tree]):
    """
    Generator that enumerates each path from root to node in set of trees
    Each path is a list of identifiers
    """
    
    # Initialize stack with depth
    stack = deque((0, tree) for tree in trees)
    
    # Initialize path
    maxlen = 32
    path = deque(maxlen=maxlen)
    
    # Initialize previous depth
    prev_depth = 0
    
    # DFS
    while stack:
        
        # Get current entry from stack
        curr_depth, curr = stack.pop()
        
        # Backtrack path
        if prev_depth > curr_depth:
            diff = prev_depth - curr_depth
            path = path[:-diff]
            
        # Proceed along path
        else:
            
            # Increase maximum size of path
            if len(path) == maxlen:
                maxlen *= 2
                path = deque(path, maxlen=maxlen)
                
            # Add current node to path
            path.append(curr.id)
            
        # Current node is a leaf node
        if not curr.adj:
            yield path
            
        # Current node is an internal node
        else:
            
            # Add entries to stack
            next_depth = curr_depth + 1
            for next in curr.adj_gen:
                stack.append((next_depth, next))
        
        # Update depth
        prev_depth = curr_depth