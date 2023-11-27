from typing import Iterable
from utilities.types.tree_node import TreeNode


def consolidate(trees : Iterable[TreeNode]):
    """
    Create a tree that is structurally equivalent to a set of trees.
    Two nodes are equivalent if and only if:
    1. Their identifiers are equal
    2. The paths leading up to them are equal
    """

    # Handle arguments
    if not trees: return None
    
    # Assert all trees are rooted at the same node
    root_name = trees[0].name
    for tree in trees:
        assert tree.name == root_name
    
    # Consolidate trees
    return consolidate_helper(trees, root_name)
            
            
def consolidate_helper(nodes : Iterable[TreeNode], node_name : str):
    """
    Helper function for consolidate()
    """
    
    # Initialize consolidated node
    new = TreeNode(node_name)
    
    # Group children of nodes together that have the same name
    name_map = dict()
    for node in nodes:
        for child in node.children:
            if child.name not in name_map:
                name_map[child.name] = [child]
            else:
                name_map[child.name].append(child)
    
    # Call consolidate helper on each group and add result to children of consolidated node
    for child_name, children in name_map.items():
        new.children.append(consolidate_helper(children, child_name))
        
    return new