from base_nodes import *

Parameter = type("Parameter", (LeafNode,), {"__init__" : constructor()})
Save = type("Save", (LeafNode,), {"__init__" : constructor()})
AttrSpec = type("AttrSpec", (SelectorNode,), {"__init__" : constructor(Parameter, Save)})
Program = type("Program", (MultiNode,), {"__init__" : constructor(Parameter, Save, AttrSpec)})

x = Parameter()
y = Save()
z = AttrSpec()
w = Program()


print(x.__class__)
print(x.adj)
print(y.__class__)
print(y.adj)
print(z.__class__)
z.add_adj(x)
print(z.adj)
print(w.__class__)
w.add_adj(x)
w.add_adj(y)
w.add_adj(z)
print(w.adj)