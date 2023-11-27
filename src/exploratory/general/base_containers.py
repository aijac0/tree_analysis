from __future__ import annotations
from abc import ABC, abstractproperty, abstractclassmethod
from typing import Type, Iterable, Callable, Self, Any, Optional
from collections import deque
from numpy import ndarray as np_ndarray, empty as np_empty
from subclassable import Subclassable
from itertools import product as it_product


"""
List of objects with a specified maximum size belonging to the same class
"""
class ArgumentList(np_ndarray):
    
    def __init__(self, arg_cls : Type, maxsize : int):
        np_ndarray.__init__(self, maxsize, dtype=arg_cls)
        self.__size = 0
        self.__maxsize = maxsize
    
    def append(self, e):
        self[self.curr_size] = e
        self.__size += 1
        
    def __len__(self):
        return self.__size
        
    def __iter__(self):
        for i in range(self.__size): yield self[i]
        
    @classmethod
    def combine(cls, arg_cls : Type, *arg_lists : ArgumentList) -> ArgumentList:
        maxsize = 1
        for arg_ls in arg_lists: maxsize *= len(arg_ls)
        rlist = ArgumentList(arg_cls, maxsize=maxsize)
        for arg_ls in arg_lists:
            for c in arg_ls:
                rlist.append(c)
        return rlist
        
"""
Abstract container
"""
class AbstractContainer(ABC):
    
    def __init__(self, **kwargs : Any):
        for arg_name, arg in kwargs.items():
            setattr(self, arg_name, arg)
            
    @property
    def kwargs(self) -> dict[str, Any]:
        return self.__dict__
            
    @abstractproperty
    def arg_classes(self) -> dict[Type[AbstractContainer], str]:
        pass
    
    @abstractclassmethod
    def create_all(cls, *arg_lists : Iterable[ArgumentList]) -> ArgumentList:
        pass


class Container(AbstractContainer, Subclassable, ABC):

    def __init__(self, **kwargs : Any):
        AbstractContainer.__init__(self, **kwargs)

    @classmethod
    def create_all(cls, *arg_lists : Iterable[ArgumentList]) -> ArgumentList:
        
        # Create a container using all the singular argument lists (arg is an array or only one arg is given)
        # Make list of repeat argument lists (arg is not an array and multiple args are given)
        kwargs = dict()
        n_containers = 1
        repeat_arg_names = list()
        repeat_arg_lists = list()
        for i in range(len(arg_lists)):
            arg_ls = arg_lists[i]
            arg_name, is_optional, is_array = cls.arg_classes[arg_ls.arg_cls]
            if len(arg_ls) == 0:
                if is_optional:                     # Arg is optional and not given -> Set to None
                    kwargs[arg_name] = None
                else:                               # Arg is not optional and not given -> Return empty list of containers
                    return ArgumentList(cls, maxsize=0)
            elif is_array:                          # Arg is an array and is given -> Singular
                kwargs[arg_name] = arg_ls
            elif len(arg_ls) == 1:                  # Arg is not an array and one arg is given -> Singular
                kwargs[arg_name] = arg_ls[0]
            else:                                   # Arg is not an array and multiple args are given -> Repeated
                repeat_arg_names.append(arg_name)
                repeat_arg_lists.append(arg_ls)
                n_containers *= len(arg_ls)
                
        # Initialize list of containers to return
        rlist = ArgumentList(cls, maxsize=n_containers)
    
        # Create each container by taking one arg from each repeat arg list (no repeat_arg_lists yields empty tuple)
        for args in it_product(*repeat_arg_lists):
        
            # Set arguments
            for i in range(len(args)):
                kwargs[repeat_arg_names[i]] = args[i]
                
            # Create container
            new = cls(**kwargs)
            rlist.append(new)
            
        return rlist
                
    
    @classmethod
    def create_subclass(cls, clsname : str, **arg_classes : tuple[Iterable[Type], bool, bool]) -> Type[Container]:
        clsdict = {
            "__init__" : cls.__init__,
            "arg_classes" : {arg_cls : (arg_name, is_optional, is_array) for arg_name, arg_spec in arg_classes.items() for arg_cls, is_optional, is_array in arg_spec}
        }
        for arg_name, arg_spec in arg_classes.items():
            for arg_cls_ls, is_optional, is_array in arg_spec:
                for arg_cls in arg_cls_ls:
                    clsdict["arg_classes"][arg_cls] = (arg_name, is_optional, is_array)
        return type(clsname, (cls,), clsdict)
    
    
class ElementaryContainer(AbstractContainer, Subclassable, ABC):
    
    def __init__(self, **kwargs : Any):
        AbstractContainer.__init__(self, **kwargs)    
    
    @classmethod
    def create_subclass(cls, clsname : str, create_all : Callable[[Type[ElementaryContainer], Iterable[ArgumentList]], ArgumentList],
                        **arg_classes : tuple[Iterable[Type], bool, bool]) -> Type[ElementaryContainer]:
        clsdict = {
            "__init__" : cls.__init__,
            "arg_classes" : dict(),
            "create_all" : create_all
        }
        for arg_name, arg_spec in arg_classes.items():
            for arg_cls_ls, is_optional, is_array in arg_spec:
                for arg_cls in arg_cls_ls:
                    clsdict["arg_classes"][arg_cls] = (arg_name, is_optional, is_array)
        return type(clsname, (cls,), clsdict)