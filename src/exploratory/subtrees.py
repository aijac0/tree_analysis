from collections import deque
from typing import Union
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from utilities.types.tree_node import TreeNode
from exploratory.tools import enumerate_tree_paths, enumerate_path_nodes
from consolidation import consolidate


def find_subtrees(trees : Union[TreeNode, list[TreeNode]]):
    """
    For each internal node, find the consolidated representation of all subtrees rooted at that node.
    1.) Exactly one subtree for each distinct internal node (node that is not exclusively a leaf node)
    2.) A cyclic node is never an internal node, unless it is the root
    3.) Each subtree is consolidated, besides each path being shortened at a cyclic node (see consolidated.py)
    * An 'internal node' is a node that is not exclusively a leaf node
    """
    
    # Consolidate trees
    # A single tree does not need to be consolidated because duplicate paths will be removed
    tree = consolidate(trees) if type(trees) == list else trees
    
    # List of all subpaths in tree
    subpaths = find_subpaths(tree)
    
    # Group subpaths rooted at the same node together
    node_subpath_map = dict()
    for subpath in subpaths:
        if subpath.name not in node_subpath_map: node_subpath_map[subpath.name] = []
        node_subpath_map[subpath.name].append(subpath)
    
    # Consolidate each group of rooted subpaths into a rooted subtree
    subtrees = []
    for node_subpaths in node_subpath_map.values():
        subtree = consolidate(node_subpaths)
        subtrees.append(subtree)
            
    return subtrees


def find_subpaths(tree : TreeNode):
    """
    Find all subpaths of a tree
    1.) All paths are linear (each node has 0 .. 1 children)
    2.) Some paths will be cyclic (A -> B -> C -> ... -> A)
    3.) May return duplicate paths
    """
    
    # List of subpaths of tree
    subpaths = list()
    
    # Set of nodes that have been found to be cyclic
    cyclic_nodes = set()

    # Iterate over each path from root to leaf in tree
    for path in iter(enumerate_tree_paths(tree)):
        
        # Get all subpaths of path
        subpaths.extend(__find_subpaths_helper(path, cyclic_nodes))
                
    # Shorten subpaths that contain a cyclic node (not including the root)
    for subpath in subpaths:
        prev = None
        for curr in iter(enumerate_path_nodes(subpath)):
            if curr != subpath and curr.name in cyclic_nodes and curr.children:
                new = TreeNode(curr.name)
                prev.children = [new]
                break
            prev = curr

    return subpaths


def __find_subpaths_helper(path : TreeNode, cyclic_nodes : set[str]):
    """
    Find all subpaths of a path (used as a subroutine of find_subpaths)
    1.) All paths are linear (each node has 0 .. 1 children)
    2.) Some paths will be cyclic (A -> B -> C -> ... -> A)
    3.) May return duplicate paths
    """
    
    # List of acyclic subpaths of path
    subpaths = list()
    
    # Stack containing subpaths to check
    stack = deque()
    stack.append(path)

    # Iterate over each subpath
    while stack:
        subpath = stack.pop()
        
        # Keep track of nodes seen along subpath
        visited = set()
        
        # Traverse path searching for cycles
        is_acyclic = True
        prev_node = None
        for node in iter(enumerate_path_nodes(subpath)):
            
            # Path contains a cycle on node
            if node.name in visited:
                
                # Recreate of the cycle path, inner path, and external path
                #   Let (A -> ... -> B -> C -> ... -> B -> ... -> D) is the full subpath
                #   Let (B -> ... -> B) be the cycle path
                #   Let (A -> ... -> B -> ... -> C) be external path
                #   Let (C -> ... -> B) be the internal path
                # Cycle will be added to subpaths, all others will be added to stack

                # Get leaf and root nodes of the cycle path
                cycle_start_parent = None
                cycle_start = None
                cycle_end_parent = prev_node
                cycle_end = node
                for cycle_start in iter(enumerate_path_nodes(subpath)):
                    if cycle_start.name == cycle_end.name: break
                    cycle_start_parent = cycle_start
                
                # Inner path exists if the cycle path is not unary
                # Root of inner path is the child of the root of the cycle path
                # Leaf of inner path is the leaf of the cycle path
                if cycle_end_parent != cycle_start:
                
                    # Get the inner path
                    inner_path = cycle_start.children[0]
                    stack.append(inner_path)

                # Root of the cycle path is the root of the full subpath
                # Root of the excluded path is the leaf of the cycle path
                if cycle_start_parent is None:
                    
                    # Get the cycle path
                    cycle_path = subpath
                    new = TreeNode(cycle_end.name)
                    cycle_end_parent.children = [new]
                    subpaths.append(cycle_path)
                                        
                    # Get the excluded path
                    excluded_path = cycle_end
                    stack.append(excluded_path)
                
                # Root of the excluded path is the root of the full subpath
                # Child of the parent of root of the cycle path becomes leaf of cycle path
                else:
                    
                    # Get the cycle path
                    cycle_path = cycle_start
                    new = TreeNode(cycle_end.name)
                    cycle_end_parent.children = [new]
                    subpaths.append(cycle_path)
                    
                    # Get the excluded path
                    excluded_path = subpath
                    cycle_start_parent.children = [cycle_end]
                    stack.append(excluded_path)
                        
                # Discontinue search of current path to prevent detecting cycles caused by a cycle on a different node
                # Example:
                #   Path P : A -> B -> C -> A -> B
                #   Cycle S: A -> B -> C -> A
                #   Cycle R: B -> C -> A -> B
                #   S causes R
                is_acyclic = False
                cyclic_nodes.add(node.name)
                break
                
            # Continue along path
            prev_node = node
            visited.add(node.name)
            
        # Path does not contain a cycle
        if is_acyclic:
            
            # Add each subpath of path to list (excluding the final node, which would be a path of length 1)
            for node in iter(enumerate_path_nodes(subpath)):
                if node != prev_node:
                    subpaths.append(node)
    
    return subpaths