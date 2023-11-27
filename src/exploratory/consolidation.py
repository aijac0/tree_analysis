from typing import Union
from utilities.types.tree_node import TreeNode


def consolidate(trees : Union[TreeNode, list[TreeNode]], start_node = None, ignore_nodes = None):
    """_
    Consolidate a set of trees into a single tree
    1. The set of complete paths in the consolidated tree is equal to the union of the set of trees in each tree
    2. Every complete path in the consolidated tree is distinct (no two complete paths have the same sequence of nodes)
    * A 'complete path' is a path from root to leaf
    """
    
    # Handle arguments
    if type(trees) == TreeNode: trees = [trees]
    if ignore_nodes is None: ignore_nodes = []

    # List of trees to consolidate
    source_trees = []
    
    # Start node is given
    # Get all subtrees rooted at start_node
    if start_node is not None:
        for tree in trees:
            source_trees.extend(tree.walk(start_node))
            if tree.name == start_node: source_trees.append(tree)
    
    # Start node is not given
    # Assert all trees are rooted at the same node
    else:
        start_node = trees[0].name
        for tree in trees: assert tree.name == start_node
        source_trees = trees
    
    # Consolidate trees
    return consolidate_helper(source_trees, start_node, ignore_nodes)
            
            
def consolidate_helper(nodes : list[TreeNode], node_name : str, ignore_nodes : list[str]):
    """
    Consolidate a set of nodes (helper function for consolidate)
    1. Create a new node
    2. Group all children of nodes together that have the same name
    3. Recursively consolidate each disjoint group of children
    4. Add each consolidated child as a child of new node
    """
    
    # Initialize consolidated node
    new = TreeNode(node_name)
    
    # Ignore children of current node if it is one of the ignore_nodes
    if node_name in ignore_nodes:
        return new
    
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
        new.children.append(consolidate_helper(children, child_name, ignore_nodes))
        
    return new