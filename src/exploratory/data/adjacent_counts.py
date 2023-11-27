from typing import Iterable, Mapping, Hashable
from collections import deque, OrderedDict, Counter
from utilities.types.tree_node import TreeNode


def get_adjacent_counts(trees : Iterable[TreeNode]):
    """
    For each distinct node n, get the following:
    1. Minimum number of nodes adjacent to n
    2. Maximum number of nodes adjacent to n
    Return dictionary mapping (n -> (min, max))
    Mapping will have an entry (n -> (min, max)) for all n
    """
    
    # Initialize dictionary containing min/max counts
    counts = OrderedDict()
    
    # Initialize stack
    stack = deque(trees)
        
    # DFS
    while stack:
        
        # Get current node from stack
        curr = stack.pop()
            
        # Add entry to counts
        count = len(curr.children)
        if curr.name not in counts:
            counts[curr.name] = (count, count)
        else:
            mn, mx = counts[curr.name]
            counts[curr.name] = (min(count, mn), max(count, mx))
        
        # Add children to stack
        stack.extend(curr.children)
                    
    return counts


def write_adjacent_counts(adj_counts : Mapping[Hashable, tuple[int, int]], data_rootdir : str):
    """
    Write adjacent counts to file
    """
    
    # Open file
    f = open(data_rootdir + '/' + "adjacent_counts.txt", 'w')
    
    # Iterate over each (node, counts pair)
    for node, counts in adj_counts.items():
            
            # Get min, max counts
            mn, mx = counts
                
            # Write min, max counts
            entry = "{} {} {}\n".format(node, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()
    
    
def read_adjacent_counts(data_rootdir : str):
    """
    Read adjacent counts from file
    """
    
    # Dictionary containing min/max counts
    adj_counts = OrderedDict()
    
    # Open file
    f = open(data_rootdir + '/' + "adjacent_counts.txt", 'r')
    
    # Iterate over each line in file
    for line in f.readlines():
    
        # Parse line for adjacent count
        node, mn_str, mx_str = line.split(' ')
        mn = int(mn_str)
        mx = int(mx_str)
        
        # Add adjacent count to dict
        adj_counts[node] = (mn, mx)
    
    # Close file
    f.close()
    
    return adj_counts


def init_adjacent_counts(trees : Iterable[TreeNode], data_rootdir : str):
    """
    Get and write adjacent counts to file
    """
    
    # Get adjacent counts
    adj_counts = get_adjacent_counts(trees)
    
    # Write adjacent counts
    write_adjacent_counts(adj_counts, data_rootdir)
    
    return adj_counts