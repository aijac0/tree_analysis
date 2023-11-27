from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Hashable, Any


class AbstractNode(ABC):
    
    def __init__(self, id : Hashable):
        self.id = id
        
    @property
    def value(self):
        return None

    @abstractproperty
    def adj(self):
        pass
        
    @abstractproperty
    def adj_gen(self):
        pass
    
    @abstractmethod
    def add_adj(self, node : AbstractNode):
        pass



class Node(AbstractNode):
    
    def __init__(self, id : Hashable):
        AbstractNode.__init__(self, id)
        self.adj = list()
        
    @property
    def adj_gen(self):
        for c in reversed(self.adj):
            yield c

    def add_adj(self, node : AbstractNode):
        self.adj.append(node)


class ValueNode(Node):
    
    def __init__(self, id : Hashable, value = None):
        Node.__init__(self, id)
        self.value = value
        

class HashNode(AbstractNode):
    
    def __init__(self, id : Hashable):
        super().__init__(self, id)
        self.adj = dict()
        
    @property
    def adj_gen(self):
        for c in self.adj.values():
            yield c
            
    def add_adj(self, node : AbstractNode):
        self.adj[node.id] = node
        
    def get_adj(self, id : Hashable):
        return self.adj.get(id)
        
        
class ValueHashNode(HashNode):
    
    def __init__(self, id : Hashable, value = None):
        HashNode.__init__(self, id)
        self.value = value