from __future__ import annotations
from typing import Callable, Iterable, Optional
from collections import deque, Counter
from exploratory.basic.trees import Tree
from exploratory.basic.nodes import HashNode, AbstractNode
    

class TreeStructure(Tree):
    
    def __init__(self, n_trees : int = 0):
        Tree.__init__(self)
        self.n_trees : int = n_trees
    
    def add_tree(self, tree : Tree):
        
        # Create unique identifier for tree
        tree_id = self.n_trees
        self.n_trees += 1
        
        # Iterate over each path in the tree
        for path in tree.paths:
            
            # Increment count of tree_id in the value of each node along path
            self.add_path(path, tree_id)
            
        # Return the id of tree
        return tree_id
      
    def add_path(self, path : deque[AbstractNode], tree_id : int):
        
        # Traverse path
        curr = self
        for node in path:
            
            # Get next id in path
            id = node.id
            
            # Get the node in self associated with id
            adj = curr.get_adj(id)
            
            # Create node if it does not exist
            if adj is None: adj = HashNode(id, Counter())

            # Increment count of tree_id in node value                          
            adj.value[tree_id] += 1
                
            # Continue traversal
            curr = adj
            
    def add_counts(self, other : TreeStructure):

        # Iterate over each complete path in structure
        for path in other.complete_paths:
            
            # Traverse path
            curr = self
            for node in path:
                
                # Get next id in path
                id = node.id
                
                # Get the node in structure associated with current id
                adj = curr.get_adj(id)
                
                # Create node if it does not exist
                if adj is None: adj = HashNode(id, Counter())

                # Update counts in node
                adj.value.update(node.value)
                
                # Continue traversal
                curr = adj

    def restructure(self, id : str):
        
        # Initialize combined structure
        combined = TreeStructure(self.n_trees)

        # Initialize stack with head nodes in structure
        stack : list[AbstractNode] = deque(adj for adj in self.adj_gen)
        
        # DFS
        while stack:
            
            # Get node from stack
            node = stack.pop()
            
            # Node has target id
            if node.id == id: 
                
               # Create structure rooted at node
               structure = TreeStructure(self.n_trees)
               structure.add_adj(node)
               
               # Add counts in new structure to combined structure
               combined.add_counts(structure)
               
               # Stop traversal of node descendents
               continue
            
            # Continue traversal
            stack.extend(adj for adj in node.adj_gen)
                        
        return combined
    
                    
"""
A query made to a tree structure has the following semantics:

    Let X be the set of distinct paths {x1 ... xN}
    Let T be the set of trees {t1 ... tM}
    Let S be the structure X x T = {(x1, t1) ... (x1, tM) ... (xN, tM)} = {s11 ... s1M ... sNM}
    Let C be the count function S -> [0, +inf)
        where C(sij) = C(xi, tj) is the number of times path xi appears in tree tj
    Given a subset of distinct paths Y = {y1 ... yK}
    Given an activation function A : {C(Y, tj) for j in [0, M]} -> {0, 1} 
        where C(Y, tj) = {C(yi, tj) for i in [0, K]}
    Let Q be the query function Q(Y, T, A) that outputs a subset of [0, M] x [0, K] 
        where (p, q) in Q(Y, T, A) indicates that A(C(Y, tj)) = 1 for p trees tj exactly q times
"""     
class StructureQueryTool:
    
    def __init__(self, structure : TreeStructure):
        self.structure : TreeStructure = structure
        
    def matrix(self, paths : Optional(Iterable[Iterable[str]]), trees : Optional(Iterable[int])):
        
        # Initialize iterator that gets the node in structure at the end of each path
        # paths == None references all paths beginning at the structure root
        if paths is None:
            pnode_iter = self.dfs()
        else:  
            pnode_iter = (self.get_path(path) for path in paths)
            
        # Initialize counter for total counts of each tree in all paths
        counter = Counter()
        
        # Iterate over each pnode
        for pnode in pnode_iter:
            
            # Update counter with counts of each tree at pnode
            # trees == None references all trees in structure
            if trees is None:
                counter.update(pnode.value)
            else:
                counter.update({tree : pnode.value[tree] for tree in trees})
                
        return counter
            
        
    def query(self, paths : deque[str], activation : Callable[..., bool]):
        
        # Initialize list of nodes where the ith node is the node at the end of the ith path in structure 
        nodes : list[HashNode] = list()
        
        # Iterate over each path
        for path in paths:
            
            # Add node at the end of path to nodes
            node = self.structure.get_path(path)[-1]
            nodes.append(node)
            
        # Initialize number of trees for which the counts of each path in paths satisfies the activation function
        n_activations : int = 0
        
        # Iterate over each tree id
        for t in range(self.structure.n_trees):    
            
            # Initialize list of counts for the number of times each path appears
            counts : list[int] = list()
            
            # Iterate over each end of path node
            for node in nodes:
                
                # Get number of times path appears in tree
                count = node.value[t] if node.value is not None and t in node.value else 0
                counts.append(count)
                
            # If counts for each relevant path in tree satisfies the activation function
            if activation(counts):
                
                # Increment activation count
                n_activations += 1
                
        return n_activations