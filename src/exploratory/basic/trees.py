from __future__ import annotations
from typing import Generator
from collections import deque, Counter
from exploratory.basic.nodes import Node, AbstractNode
from exploratory.basic.parsers import Parser, StandardParser


class Tree(Node):
    
    def __init__(self):
        Node.__init__(self, "head")
        
    """
    Depth first search tree, yielding depth and node at each step
    """
    def dfs(self) -> Generator[tuple[int, AbstractNode], None, None]:
        
        # Initialize stack
        stack : deque[tuple[int, AbstractNode]] = deque((0, adj) for adj in self.adj_gen)
        
        # DFS
        while stack:
            
            # Get (depth, node) pair from stack
            depth, node = stack.pop()
            yield depth, node
            
            # Add (next depth, node) pair for each adjacent node to stack 
            stack.extend((depth + 1, adj) for adj in node.adj_gen)
            
    """
    Enumerates each path from root to leaf or repeated node in tree
    Each node in a path is repeated no more than twice
    Instance of a path with a node repeated more than twice are recursively
    split into a path from root to first instance, 
    and a path from root up to first instance combined with path from second instance to leaf.
    """
    @property
    def paths(self) -> Generator[deque[AbstractNode], None, None]:

        # Iterate over each path in tree
        for full_path in self.complete_paths:

            # Possibly recursive paths
            paths : deque[deque[AbstractNode]] = deque()
            paths.append(full_path)
            
            # Repeat until all paths are yielded (reduced to a non-recursive representation)
            while paths:
                
                # Get next path
                path = paths.pop()
                
                # Initialize set of node ids visited along path
                visited : set[str] = set()
                
                # Iterate over each node in path
                for curr in path:
                    
                    # First instance of node
                    if curr.id not in visited:
                        visited.add(curr.id)
                        
                    # Second instance of node
                    # Node is not leaf
                    elif curr != path[-1]:
                        
                        # Initialize two new paths
                        new1 = deque()
                        new2 = deque()
                        
                        # Initialize path node iterator
                        path_iter = iter(node for node in path)
                        
                        # Add nodes to both paths from head to first instance of node
                        for node in path_iter:
                            new1.append(node)
                            new2.append(node)
                            if node.id == curr.id: break
                            
                        # Add nodes to first path from after first instance of node to second instance of node
                        for node in path_iter:
                            new1.append(node)
                            if node.id == curr.id: break
                            
                        # Add nodes to second path from after second instance of node to leaf
                        for node in path_iter:
                            new2.append(node)
                                                            
                        # Yield the first path
                        yield new1
                            
                        # Add second path to stack
                        paths.append(new2)
                        break
                    
                    # Node is leaf
                    if curr == path[-1]:
                        
                        # Yield path
                        yield path
                            

    """
    Enumerates each path from root to node in set of trees
    """
    @property
    def complete_paths(self) -> Generator[deque[AbstractNode], None, None]:
        
        # Initialize path
        maxlen = 32
        path : deque[AbstractNode] = deque(maxlen=maxlen)
        
        # Initialize previous depth
        prev_depth = -1
        
        # DFS
        for depth, node in self.dfs():

            # Backtrack path to proper depth
            if prev_depth >= depth:
                diff = prev_depth - depth + 1
                for i in range(diff): path.pop()
                    
            # Increase maximum size of path if necessary
            if len(path) == maxlen:               
                maxlen *= 2
                path = deque(path, maxlen=maxlen)
            
            # Add node to path
            path.append(node)
                
            # Yield path if node is a leaf node
            if not node.adj: yield path
                
            # Update depth
            prev_depth = depth   
            
    
    """
    Output text representation of tree to file
    """
    def to_file(self, filepath : str):
        
        # Open file
        f = open(filepath, 'w')
        
        # Initialize traversal generator
        traversal = self.dfs()
        
        # Iterate over each (depth, node) pair in traversal
        for depth, node in traversal:
            
            # Write to file
            id = node.id
            value = node.value if node.value is not None else ""
            f.write("{}{} {}\n".format('| ' * depth, id, value))
            
        # Close file
        f.close()
            
        
    """
    Initialize tree from parser
    """
    @classmethod
    def from_parser(cls, tp : Parser) -> Tree:
        
        # Initialize tree
        tree = cls()
        
        # Path from root to node and depth of previous node
        path : deque[AbstractNode] = deque()
        path.append(tree)
        prev_depth = -1
        
        # Parse tree
        for depth, node in tp:

            # Get parent of node
            for i in range((prev_depth - depth) + 1): path.pop()
            parent = path[-1]
            
            # Add node as child of parent
            parent.add_adj(node)
            
            # Update path and previous depth
            path.append(node)
            prev_depth = depth
            
        return tree
        
        
    """
    Initialize tree from text file
    """
    @classmethod
    def from_file(cls, filepath : str) -> Tree:

        # Parse filepath using standard parser
        tp = StandardParser(Node, str)(filepath)
        return cls.from_parser(tp)
    
    
    
"""
    
        # Initialize path
        maxlen = 32
        path : deque[AbstractNode] = deque(maxlen=maxlen)
        recursed : deque[AbstractNode] = deque()
        
        # Initialize mapping of node ids to whether or not they have been visited
        counts = Counter()
        is_recursed = dict()
        
        # Initialize previous depth
        prev_depth = 0
        
        # Initialize depth of recursive portion of path
        recursive_depth = 0
        
        # DFS
        for depth, node in self.dfs():
            #print(prev_depth, depth, recursive_depth, prev_depth - depth - recursive_depth > 0)
            # Backtrack to desired depth
            if prev_depth > depth:
                print({"prev_depth":prev_depth, "depth":depth, "recursive_depth":recursive_depth})
                
                diff = prev_depth - depth + 1
                if diff >= recursive_depth:
                    diff -= recursive_depth
                    depth -= recursive_depth
                    recursive_depth = 0
                else:
                    depth -= diff
                    recursive_depth -= diff
                    
                prevs = []
                for i in range(diff): 
                    prev = path.pop()
                    if counts[prev.id] > 1: 
                        counts[prev.id] -= 1
                    elif counts[prev.id] == 1:
                        counts[prev.id] -= 1
                        is_recursed[prev.id] = False
                    prevs.append(prev)
    
                for p in reversed(prevs):
                    print("- Node ({})".format(p.id))
                for p in path:
                    print(p.id)
                    
                    
            # Node is recursed
            if node.id in counts and counts[node.id] > 0:
                is_recursed[node.id] = True
                
                # Check is the most recent recursed node
                for prev in reversed(path):
                    
                    # Node is the most recent recursed node
                    if prev.id == node.id:
                        
                        # Yield singly recursed path
                        path.append(node)
                        yield path
                        path.pop()
                        
                        # Backtrack to previous instance (but do not remove)
                        prevs = []
                        while path[-1].id != node.id:
                            prev = path.pop()
                            if counts[prev.id] > 1: 
                                counts[prev.id] -= 1
                            elif counts[prev.id] == 1:
                                counts[prev.id] -= 1
                                is_recursed[prev.id] = False
                            prevs.append(prev)
                            recursive_depth += 1
                        recursive_depth += 1
                        for p in reversed(prevs):
                            print("- Node ({})".format(p.id))
                        for p in path:
                            if p.id == node.id:
                                print("Recursed ({})".format(p.id))
                            else:
                                print("Node ({})".format(p.id))
                        break
                        
                    # Node is not the most recent recused node
                    elif is_recursed[prev.id]:
                        break
                    
            # Node is not repeated
            else:
                
                # Increase maximum size of path if necessary
                if len(path) == maxlen:               
                    maxlen *= 2
                    path = deque(path, maxlen=maxlen)
                
                # Add node id to path and is_visited dict
                path.append(node)
                is_visited[node.id] = True
                    
                # Yield path if node is a leaf node
                if not node.adj: 
                    yield path
                    print("+ Leaf ({})".format(node.id))
                else:
                    print("+ Node ({})".format(node.id))
                
            # Update depth
            prev_depth = depth
            
"""