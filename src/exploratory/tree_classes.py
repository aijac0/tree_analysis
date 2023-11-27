from abc import ABC, abstractproperty, abstractmethod
from typing import Iterable, Hashable
from specific.nodes import HashNode, ValueHashNode
from collections import deque


class HashTree:
    
    def __init__(self, head_id : Hashable):
        self.head : ValueHashNode = ValueHashNode(head_id)
        self.n_hashes : int = 0
    
    def hash_path(self, path : deque[Hashable]):
        
        # Traverse path
        curr = self.head
        while path:
            
            # Get the node associated with current id on path
            id = path[0]
            adj = curr.get_adj(id)
            
            # Create path and return new path hash if it does not exist
            if adj is None: 
                return self.add_path(curr, path)
            
            # Continue along path
            path.popleft()
            curr = adj
            
        # Check if last node has a value, return value if true
        if curr.value is not None: return curr.value
        
        # Create hash for path and return created value
        return self.add_path(curr, path)
    
    def add_path(self, node : ValueHashNode, path : deque):
        
        # Traverse path
        curr = node
        while path:
            
            # Create node associated with current id on path
            id = path.popleft()
            adj = ValueHashNode(id)
            curr.add_adj(adj)
            
            # Continue along path
            curr = adj
            
        # Create hash for path
        hash = self.n_hashes
        self.n_hashes += 1
        
        # Set new hash as value of last node in path and return value
        curr.value = hash
        return hash