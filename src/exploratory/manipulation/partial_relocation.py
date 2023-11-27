from typing import Iterable
from collections import deque
from specific.nodes import Node, ValueNode
from specific.trees import Tree
from frtt.initial.initialize import initialize
from frtt.static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree


def partially_relocate(trees : Iterable[TreeNode]):
    """
    Create a tree that is structurally equivalent to a set of trees
    Assumes that two nodes are equal if and only if:
    1. They have the same identifier
    2. Identifier is not statically recursive
    """
    pass




if __name__ == "__main__":
    
    # Get source files
    filepaths = initialize("../lilac/source")
    
    # Iterate over each flang parse tree
    for i in range(len(filepaths)):
        print("{} / {}".format(i+1, len(filepaths)))
        filepath = filepaths[i]
        tree = get_abstract_syntax_tree(filepath, is_source=True)
        
        with open("data/raw/{}.txt".format(i+1)) as f:
            f.write(str(tree))
