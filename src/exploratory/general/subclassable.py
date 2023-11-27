from __future__ import annotations
from abc import ABC, abstractclassmethod
from typing import Type

class Subclassable(ABC):

    @abstractclassmethod
    def create_subclass(cls, clsname, *args, **kwargs) -> Type[Subclassable]:
        pass