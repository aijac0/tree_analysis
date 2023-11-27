from typing import Iterable
from utilities.types.tree_node import TreeNode


def combination(trees : Iterable[TreeNode]):
    """
    Create a tree that is structurally equivalent to a set of trees.
    Two nodes are equal if and only if:
    1. They are both root nodes
    """
    
    # Handle arguments
    if not trees: return None
    
    # Initialize combined node
    root_id = trees[0].name
    combined = TreeNode(root_id)
    
    # Iterate over each tree
    for tree in trees:
        
        # Add children of tree as children of result
        combined.children.extend(tree.children)
        
    return combined