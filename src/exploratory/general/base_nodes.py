from __future__ import annotations
from abc import ABC, abstractproperty, abstractmethod
from typing import Type, Iterable, Mapping, Callable, Self
from numpy import ndarray as np_ndarray, empty as np_empty
from subclassable import Subclassable
from base_containers import ArgumentList, AbstractContainer


"""
List of nodes belonging to the same node class
Defines a 'parse' method to combine the results of calling 'parse' on each node into a single list
"""
class AdjacencyList(list):
    
    def __init__(self, node_cls : Type[AbstractNode]):
        list.__init__(self)
        self.node_cls = node_cls        
    
    def parse(self) -> ArgumentList:
        return ArgumentList.combine(self.node_cls.datacls, *(adj.parse() for adj in self))


"""
Abstract node
Supports an arbitrary number of adjacent nodes grouped together based on their membership to an arbitrary set of classes
Supports the 'add_adj' method to add a new node to the group of adjacent nodes belonging to the same class
Supports an arbitrary 'parse' method to create objects from an arbitrary class
Descendent classes will define the 'adj_classes' property to restrict the set of classes of adjacent nodes
Descendent classes will define the 'datacls' property to define the class of objects created by the 'parse' method
Descendent classes will define the 'parse' method to instantiate members of the class specified by the 'datacls' property
"""
class AbstractNode(ABC):
        
    def __init__(self):
        self.adj : np_ndarray[AdjacencyList[Node]] = np_empty(len(self.adj_classes), dtype=AdjacencyList)
        for adj_cls, idx in self.adj_classes.items(): self.adj[idx] = AdjacencyList(adj_cls)
            
    @abstractproperty
    def adj_classes(self) -> Mapping[Type[Node], int]:
        pass
    
    @abstractproperty
    def datacls(self) -> Type[AbstractContainer]:
        pass

    @abstractmethod
    def parse(self) -> Iterable[AbstractContainer]:
        pass

    def add_adj(self, node : Node):
        idx = self.adj_classes[node.__class__]
        self.adj[idx].append(node)


"""
Abstract node
Defines the 'parse' method to instantiate members of the class specified by the 'datacls' property
using the objects recursively parsed from the adjacent nodes
Defers the definition of the 'adj_classes' property to descendent classes
Defers the definition of the 'datacls' property to descendent classes
Non-abstract subclasses can be created using the 'create_subclass' class method
"""    
class Node(AbstractNode, Subclassable, ABC):
    
    def __init__(self):
        AbstractNode.__init__(self)
    
    def parse(self) -> ArgumentList:
        args = [self.adj[idx].parse() for idx in self.adj_classes.values()]
        return self.datacls.create_all(*args)
    
    @classmethod
    def create_subclass(cls, clsname : str, datacls : Type[AbstractContainer], *adj_classes : Type[Node]) -> Type[AbstractNode]:
        clsdict = {
            "__init__" : cls.__init__,
            "adj_classes" : {adj_classes[i] : i for i in range(len(adj_classes))},
            "datacls" : datacls
        }
        return type(clsname, (cls,), clsdict)


"""
Abstract node
Defers the definition of the 'adj_classes' property to descendent classes
Defers the definition of the 'datacls' property to descendent classes
Defers the definition of the 'parse' method to descendent classes
Non-abstract subclasses can be created using the 'create_subclass' class method
"""
class ElementaryNode(AbstractNode, Subclassable, ABC):
    
    def __init__(self):
        AbstractNode.__init__(self)
    
    @classmethod
    def create_subclass(cls, clsname : str, datacls : Type, parse : Callable[[Self], ArgumentList], *adj_classes : Type[Node]) -> Type[AbstractNode]:
        clsdict = {
            "__init__" : cls.__init__,
            "adj_classes" : {adj_classes[i] : i for i in range(len(adj_classes))},
            "datacls" : datacls,
            "parse" : parse,
        }
        return type(clsname, (cls,), clsdict)
    

"""
Abstract node 
Supports a string literal attribute
Defers the definition of the 'adj_classes' property to descendent classes
Defers the definition of the 'datacls' property to descendent classes
Defers the definition of the 'parse' method to descendent classes
Non-abstract subclasses can be created using the 'create_subclass' class method
"""
class ValueNode(ElementaryNode, ABC):
    
    def __init__(self, val : str):
        ElementaryNode.__init__(self)
        self.val : str = val