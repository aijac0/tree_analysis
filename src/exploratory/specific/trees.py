from typing import Iterable
from collections import deque
from nodes import Node
from parsers import Parser, StandardParser

class Tree(Node):
    
    def __init__(self):
        self.node : Node = None
    
    @property
    def adj_gen(self):
        return self.node.adj_gen()
    
    def add_adj(self, node : Node):
        self.node = node
        return True
    
    def to_file(self, filepath : str):
        
        # Open file
        f = open(filepath, 'w')
        
        # Stack of (depth, node) pairs
        stack : deque[tuple[int, Node]] = deque()
        stack.append((0, self.node))

        # DFS
        while len(stack):
            
            # Get node from stack
            depth, node = stack.pop()
            
            # Add children to stack
            stack.extend((depth + 1, next) for next in node.adj_gen)
            
            # Write to file
            f.write('| ' * depth)
            f.write(node.id)
            f.write('\n')
            
        # Close file
        f.close()
        
    @classmethod
    def from_file(cls, filepath : str):
        
        # Parse filepath using standard parser
        tp = StandardParser(filepath)
        return cls.from_tree_parser(tp)
    
    @classmethod
    def from_tree_parser(cls, tp : Parser):
        
        # Initialize tree
        tree = Tree()
        
        # Path from root to node and depth of previous node
        path : Iterable[Node] = deque()
        path.append(tree)
        prev_depth = -1
        
        # Parse tree
        for depth, identifier in tp:
            
            # Create node
            node = Node(identifier)
            
            # Get parent of node
            for i in range((prev_depth - depth) + 1): path.pop()
            parent = path[-1]
            
            # Add node as child of parent
            parent.add_adj(node)
            
            # Update path and previous depth
            path.append(node)
            prev_depth = depth
            
        return tree


if __name__ == "__main__":
 
    fpt = StandardParser("data/SubroutineSubprogram.txt")
    tree = Tree.from_tree_parser(fpt)
    tree.to_file("data/test.txt")
    