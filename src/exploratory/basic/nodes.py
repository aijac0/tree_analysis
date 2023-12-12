from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Union, Generator, TypeVar

V = TypeVar("V", int, str, float)
VAL = V | tuple[V] | list[V] | list[tuple[V]] | None


class AbstractNode(ABC):

    def __init__(self, id : str, adj : Union[list[AbstractNode], dict[str, AbstractNode]], value : VAL = None):
        self.id : str = id
        self.adj : Union[list[AbstractNode], dict[str, AbstractNode]] = adj
        self.value : VAL = value
    
    @abstractproperty
    def adj_gen(self) -> Generator[AbstractNode, None, None]:
        pass
    
    @abstractmethod
    def add_adj(self, node : AbstractNode):
        pass
    
    @abstractmethod
    def get_adj(self, id : str) -> AbstractNode:
        pass
        

class Node(AbstractNode):
    
    def __init__(self, id : str, value : VAL = None):
        AbstractNode.__init__(self, id, list(), value)
        
    @property
    def adj_gen(self) -> Generator[AbstractNode, None, None]:
        for c in reversed(self.adj):
            yield c

    def add_adj(self, node : AbstractNode):
        self.adj.append(node)
        
    def get_adj(self, id : str) -> AbstractNode:
        for adj in self.adj_gen:
            if adj.id == id:
                return adj
        

class HashNode(AbstractNode):
    
    def __init__(self, id : str, value : VAL = None):
        AbstractNode.__init__(self, id, dict(), value)
        
    @property
    def adj_gen(self) -> Generator[AbstractNode, None, None]:
        for c in reversed(self.adj.values()):
            yield c
            
    def add_adj(self, node : AbstractNode):
        self.adj[node.id] = node
        
    def get_adj(self, id : str) -> AbstractNode:
        return self.adj.get(id)