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