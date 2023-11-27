from typing import Iterable
from collections import deque
from static_analysis.parsing import abstract_syntax_tree as ast, tree_parsing as tp
from utilities.types.tree_node import TreeNode


def enumerate_tree_paths(trees : Iterable[TreeNode]):
    """
    Generator that enumerates each path from root to node in set of trees
    Each path is a list of identifiers
    """
    
    # Initialize stack with depth
    stack = deque((0, tree) for tree in trees)
    
    # Initialize path
    maxlen = 32
    path = deque(maxlen=maxlen)
    
    # Initialize previous depth
    prev_depth = 0
    
    # DFS
    while stack:
        
        # Get current entry from stack
        curr_depth, curr = stack.pop()
        
        # Backtrack path
        if prev_depth > curr_depth:
            diff = prev_depth - curr_depth
            path = path[:-diff]
            
        # Proceed along path
        else:
            
            # Increase maximum size of path
            if len(path) == maxlen:
                maxlen *= 2
                path = deque(path, maxlen=maxlen)
                
            # Add current node to path
            path.append(curr.name)
            
        # Current node is a leaf node
        if not curr.children:
            yield path
            
        # Current node is an internal node
        else:
            
            # Add entries to stack
            next_depth = curr_depth + 1
            for next in curr.children:
                stack.append((next_depth, next))
        
        # Update depth
        prev_depth = curr_depth
            
            
            
def enumerate_path_nodes(path : TreeNode):
    """
    Generator that yields each node along a path
    Path is assumed to be linear (each node either has 0 or 1 children)
    """
    curr = path
    while curr.children:
        yield curr
        curr = curr.children[0]
    yield curr
    

def reconstruct_path(predecessors, new):
    path = [new]
    curr = new
    while True:
        if predecessors[curr] is None:
            break
        curr = predecessors[curr]
        path.append(curr)
        
    head = None
    prev = None
    for curr in reversed(path):
        new = TreeNode(curr.value)
        if head is None:
            head = new
            prev = new
        else:
            prev.children.append(new)
            prev = new
    return head
                

def parse_ast_variables(tree : TreeNode):
    variables = dict()
    variable_names = []
    tree = tree.step("ImplicitPart", exception_handling=False)
    if not tree: return variables
    
    for variable_name in [decl.leaf().value[1:-1] for decl in tree.walk("EntityDecl")]:
        variable_names.append(variable_name)
        
    for variable_name in variable_names:
        tree_copy = tree.deep_copy()
        variables[variable_name] = tree_copy
        queue = [(tree_copy, next) for next in tree_copy.children]
        while queue:
            prev, curr = queue.pop()
            leaves = set([leaf.value[1:-1] for leaf in curr.leaves()])
            skip = False
            if variable_name not in leaves:
                for other_vname in variable_names:
                    if other_vname in leaves:
                        skip = True
                        prev.children.remove(curr)
                        del curr
                        break
            if not skip:
                queue.extend([(curr, next) for next in curr.children])
        
            
    return variables        


def parse_file_variables(filepath):
    tree = ast.get_abstract_syntax_tree(filepath)
    routine_variables = dict()
    for subtree in tree.kins("ProgramUnit"):
        programunit = tp.parse_programunit(subtree)
        routine_variables[programunit.name] = parse_ast_variables(subtree)
    return routine_variables


def find_trees(path, trees):
    if not len(path): return []
    matching_trees = []
    for tree in trees:
        subtrees = tree.walk(path[0])
        if tree.name == path[0]:
            subtrees.append(tree)
        for subtree in subtrees:
            contains_path = True
            curr = subtree
            for i in range(1, len(path)):
                curr = curr.step(path[i])
                if not curr:
                    contains_path = False
                    break
            if contains_path: 
                matching_trees.append(tree)
                break
    return matching_trees


def get_path(tree : TreeNode, path : list[str]):
    stack = [(tree, 0)]
    while stack:
        curr, depth = stack.pop()
        if depth + 1 == len(path):
            head = TreeNode(path[0])
            prev = head
            for node_name in path[1:-1]:
                next = TreeNode(node_name)
                prev.children.append(next)
                prev = next
            prev.children.append(curr)
            return head
        stack.extend([(c, depth + 1) for c in curr.children if c.name == path[depth + 1]])
    return None


def has_path(tree : TreeNode, path : list[str]):
    stack = [(tree, 0)]
    while stack:
        curr, depth = stack.pop()
        if depth + 1 == len(path): return True
        stack.extend([(c, depth + 1) for c in curr.children if c.name == path[depth + 1]])
    return False