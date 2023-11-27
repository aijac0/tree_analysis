from typing import Iterable, Mapping, Hashable
from collections import OrderedDict, Counter
from utilities.types.tree_node import TreeNode
from exploratory.tools import enumerate_tree_paths

def get_path_counts(trees : Iterable[TreeNode]):
    """
    For each distinct node n, get the following:
    1. Minimum number of times n appears on a path for which it appears at least once 
    2. Maximum number of times n appears on a path for which it appears at least once
    Return dictionary mapping (n -> (min, max))
    Mapping will have an entry (n -> (min, max)) for all n
    """
    
    # Initialize dictionary containing min/max counts
    path_counts = OrderedDict()
    
    # Enumerate paths from root to leaf in all trees
    for path in enumerate_tree_paths(trees):
        
        # Initialize dict with number of times each node appears on path
        node_counts = Counter()
        
        # Iterate over each node in path
        for node in path:
            
            # Increment node count
            node_counts(node)
        
        # Update path counts
        for node, count in node_counts.total():
            if node not in path_counts:
                path_counts[node] = (count, count)
            else:
                mn, mx = path_counts[node]
                path_counts[node] = (min(count, mn), max(count, mx))
                    
    return path_counts


def write_path_counts(path_counts : Mapping[Hashable, tuple[int, int]], data_rootdir : str):
    """
    Write path counts to file
    """
    
    # Open file
    f = open(data_rootdir + '/' + "path_counts.txt", 'w')
    
    # Iterate over each (node, counts) pair
    for node, counts in path_counts.items():
            
            # Get min, max counts
            mn, mx = counts
                
            # Write min, max counts
            entry = "{} {} {}\n".format(node, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()


def read_path_counts(data_rootdir : str):
    """
    Read path counts from file
    """
    
    # List of nodes and dictionary containing min/max counts
    path_counts = OrderedDict()
    
    # Open file
    f = open(data_rootdir + '/' + "path_counts.txt", 'r')
    
    # Iterate over each line in file
    for line in f.readlines():
    
        # Parse line for path count
        node, mn, mx = line.split(' ')
        
        # Add adjacency to dict
        path_counts[node] = (mn, mx)
    
    # Close file
    f.close()
    
    
def init_path_counts(trees : Iterable[TreeNode], data_rootdir : str):
    """
    Get and write path counts to file
    """
    
    # Get path counts
    path_counts = get_path_counts(trees)
    
    # Write path counts
    write_path_counts(path_counts, data_rootdir)
    
    return path_counts