from base_nodes import ElementaryNode, ValueNode
from elementary_containers import *

# Shared parse methods
simple_parse = lambda self : self.datacls()

# Attribute nodes
Target = ElementaryNode.create_subclass('Target', isTarget, simple_parse)
Save = ElementaryNode.create_subclass('Save', isSave, simple_parse)
Parameter = ElementaryNode.create_subclass('Parameter', isParameter, simple_parse)
Allocatable = ElementaryNode.create_subclass('Allocatable', isAllocatable, simple_parse)
Pointer = ElementaryNode.create_subclass('Pointer', isPointer, simple_parse)
Optional = ElementaryNode.create_subclass('Optional', isOptional, simple_parse)

# Intent nodes
In = ElementaryNode.create_subclass('In', Intent, lambda _ : InIntent)
Out = ElementaryNode.create_subclass('Out', Intent, lambda _ : OutIntent)
InOut = ElementaryNode.create_subclass('InOut', Intent, lambda _ : InOutIntent)

# Type nodes
Complex = ElementaryNode.create_subclass("Complex", Type, lambda _ : Intent.create_all('complex'))
Double = ElementaryNode.create_subclass("Double", Type, lambda _ : Intent.create_all('double'))

# Constant nodes
Star = ElementaryNode.create_subclass("Star", Indicator, lambda _ : Indicator.create_all('star'))

# Value nodes
CharVal = ElementaryNode.create_subclass("CharVal", str, lambda _ : ['a'])           # Flang does not store value of chars for some reason
BoolVal = ElementaryNode.create_subclass("BoolVal", bool, lambda _ : [True])          # Flang does not store value of booleans for some reason
StrVal = ValueNode.create_subclass("StrVal", str, lambda self : [self.val])
IntVal = ValueNode.create_subclass("IntVal", int, lambda self : [int(self.val)])