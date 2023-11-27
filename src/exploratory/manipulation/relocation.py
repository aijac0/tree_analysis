from typing import Iterable
from collections import deque
from utilities.types.tree_node import TreeNode


def relocate(trees : Iterable[TreeNode]):
    """
    Create a tree that is structurally equivalent to a set of trees
    Assumes that two nodes are equal if and only if:
    1. They have the same identifier
    """
    
    # Handle arguments
    if not trees: return None
    
    # Intialize relocated tree
    root_id = trees[0].name
    relocated = TreeNode(root_id)
    
    # Dictionary mapping each identifier to its associated node in relocated tree
    node_map = dict()
    node_map[root_id] = relocated
    
    # Dictionary mapping each identifier to the set of identifiers of nodes adjacent
    adj_map = dict()
    adj_map[root_id] = set()
    
    # DFS trees
    stack = deque([(relocated, tree) for tree in trees])
    while stack:
        
        # Get current node from stack
        curr_reloc, curr = stack.pop()
        
        # Add each child of current node to stack
        for next in curr.childen:
            
            # Get node in relocated associated with same identifier as child
            if next.name not in node_map: 
                next_reloc = TreeNode(next.name)
                node_map[next.name] = next_reloc
                adj_map[next.name] = set()
            else:
                next_reloc = node_map[next.name]
                
            # Add node in relocated as child of node in relocated with same identifer as current node
            if next.name not in adj_map[curr.name]:
                curr_reloc.children.append(next_reloc)
                adj_map[curr.name].add(next.name)
                 
            # Add (node in relocated with same identifier as next node, next node) to stack
            stack.append((next_reloc, next))
                
    return relocated