from typing import Iterable
from collections import deque
from exploratory.basic.nodes import Node, ValueNode
from exploratory.basic.trees import Tree
from exploratory.tools.trees import enumerate_tree_paths
from exploratory.tools.files import get_files


def partially_relocate(trees):
    """
    Create a tree that is structurally equivalent to a set of trees
    Assumes that two nodes are equal if and only if:
    1. They have the same identifier
    2. Identifier is not statically recursive
    """
    pass



def get_variably_recursive_ids(trees : Iterable[Tree]):
    
    # Initialize set of variably recursive nodes
    variably_recursive = set()
    
    # Initialize counts of each node ids along all paths (until two different counts are found)
    counts = dict()
    
    # Iterate over each path in tree
    for path in enumerate_tree_paths(trees):
        
        # Initialize counts of node ids along all paths
        temp_counts = dict()
        
        # Iterate over each node id in tree
        for id in path:
            
            # Ignore if id is already seen to be variably recursive
            if id in variably_recursive: continue
            
            # Increment count
            if id not in temp_counts:
                temp_counts[id] = 1
            else:
                temp_counts[id] += 1
                
        # Update counts. If counts differ, node is variably recursive
        for id, count in temp_counts.items():
            
            # Add count if it does not exist
            if id not in counts:
                counts[id] = count
            
            # Add id to set of variably recursive ids if it differs
            elif counts[id] != count:
                variably_recursive.add(id)
                
    return variably_recursive


def transform(tree : Iterable[Tree], variably_recursive : set):
    pass



if __name__ == "__main__":
    
    # Get files
    filepaths = get_files("../fortran_regression_testing_tool/data", "txt")
    
    # Get list of trees
    trees = [Tree.from_file(filepath) for filepath in filepaths]
    print(len(trees))
    
    # Get set of variably recursive nodes
    variably_recursive = get_variably_recursive_ids(trees)
    
    for id in variably_recursive:
        print(variably_recursive)
        
    with open("variably_recursive.txt", 'w') as f:
        for id in variably_recursive:
            f.write(id + '\n')
    
    
"""    # Iterate over each source file
    for i in range(len(filepaths)):
        
        # Get input filepath
        in_filepath = filepaths[i]
        print("{} / {}".format(i+1, len(filepaths)))
        
        # Get input tree
        in_tree = Tree.from_file(in_filepath)
        
        # Get output filename
        out_filepath = in_filepath.replace("raw/", "")
        
        # Get output tree
        out_tree = transform(in_tree)
        
        # Create dirctory for output filepath
        dirpath = "/".join(out_filepath.split('/')[:-1])
        os.makedirs(dirpath)
        
        # Write tree to file
        out_tree.to_file(out_filepath)
"""