from typing import Iterable, Mapping

# Node class declaration format string
CLASS_DECLARATION = "type('{node}', ({cls},), {'__init__' : constructor({neighbors})})\n"

# Node superclasses
leafnode_supercls = "LeafNode"
multinode_supercls = "MultiNode"
selectornode_supercls = "SelectorNode"


def get_node_classes(edge_counts : Mapping[str, Mapping[str, tuple[int, int]]], adj_counts : Mapping[str, tuple[int, int]]):
    """
    For each distinct node n, get the following:
    1. Name of class that n belongs to (name of n)
    2. Name of superclass of the class that n belongs to (based on its edge_counts and adj_counts properties)
    3. List of all possible nodes adjacent to n
    Return list of tuples containing these 3 parameters
    For each index of list, the list of adjacents will only contain nodes associated with a previous index of list
    """

    # Initialize list of class declarations parameters
    node_classes = list()
    
    # Iterate over each node in reverse order
    for node in reversed(edge_counts):
        
        # Get list and counts of all adjacent nodes
        neighbors = [neighbor for neighbor in edge_counts[node]]
        
        # Minimum and maximum number of adjacent nodes for any one instance of node
        mn_count, mx_count = adj_counts[node]
        
        # Node is a LeafNode (no instance of node has children)
        if not neighbors:
            supercls = leafnode_supercls
            
        # Node is a MultiNode (node either has a variable number of children or a static number of children that is greater than 1)
        elif mn_count != mx_count or mn_count != 1:
            supercls = multinode_supercls
                
        # Node is a SelectorNode (every instance of node has 1 child)
        else:
            supercls = selectornode_supercls
        
        # Add class declaration parameters
        node_classes.append((node, supercls, neighbors))    
            
    return node_classes

    
def write_node_classes(node_classes : Iterable[tuple[str, str, Iterable[str]]], data_rootdir : str):
    """
    Write node class parameters and node class declarations to file
    """
    
    # Open files
    param_f = open(data_rootdir + '/' + "node_class_parameters.txt", 'w')
    decl_f = open(data_rootdir + '/' + "node_class_declarations.txt", 'w')
    
    # Iterate over each set of class declaration parameters
    for node, supercls, neighbors in node_classes:
        
        # Comma separated neighbors
        neighbors_str = ', '.join(neighbors)
        
        # Write class parameters
        cls_param = "{} {} ({})\n".format(node, supercls, neighbors_str)
        param_f.write(cls_param)
        
        # Write class declaration
        cls_decl = CLASS_DECLARATION.format(node=node, cls=supercls, neighbors=neighbors_str)
        decl_f.write(cls_decl)
    
    # Close files
    param_f.close()
    decl_f.close()
    
    
def read_node_classes(data_rootdir : str):
    """
    Read node class parameters from file
    """
    
    # List of node class parameters
    path_counts = list()
    
    # Open file
    f = open(data_rootdir + '/' + "node_class_parameters.txt", 'r')
    
    # Iterate over each line in file
    for line in f.readlines():
    
        # Parse line for class parameters
        prefix, postfix = line.split('(')
        node, supercls = prefix.split(' ')
        neighbors = postfix[:-1].split(', ')
        
        # Add parameters to list
        path_counts.append((node, supercls, neighbors))


def init_edge_counts(edge_counts : Mapping[str, Mapping[str, tuple[int, int]]], adj_counts : Mapping[str, tuple[int, int]], data_rootdir : str):
    """
    Get and write node class parameters and node class declarations to file
    """
    
    # Get node class parameters
    node_classes = get_node_classes(edge_counts, adj_counts)
    
    # Write node class parameters and node class declarations to file
    write_node_classes(node_classes, data_rootdir)
    
    return node_classes