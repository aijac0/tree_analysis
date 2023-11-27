from base_containers import Container
from elementary_containers import *

# Argument definition lambda functions (Classes -> (Classes, is_optional, is_array))
req_single = lambda *xs : (xs, False, False)    # Required / single argument
req_array = lambda *xs : (xs, False, True)      # Required / array argument
opt_single = lambda *xs : (xs, True, False)     # Optional / single argument
opt_array = lambda *xs : (xs, True, True)       # Optional / array argument

# Types
RealType = Container.create_subclass("RealType", kind=opt_single(Expression, str))
IntType = Container.create_subclass("IntType", kind=opt_single(Expression, str))
LogicalType = Container.create_subclass("LogicalType", kind=opt_single(Expression))
CharacterType = Container.create_subclass("CharacterType", length=opt_single(Expression, StarIndicator))
DerivedType = Container.create_subclass("DerivedType", name=req_single(str))
Types = (RealType, IntType, LogicalType, CharacterType, ComplexType, DoubleType, DerivedType)

# Attributes
AttrSpec = Container.create_subclass("AttrSpec", target=opt_single(isTarget), save=opt_single(isSave), 
                    parameter=opt_single(isParameter), allocatable=opt_single(isAllocatable), 
                    pointer=opt_single(isPointer), optional=opt_single(isOptional))

# Dimensions
Dimension = Container.create_subclass("Dim", req_single(Expression))

# Variable node
Variable = Container.create_subclass("Variable", 
    name=req_single(str), attrs=opt_single(AttrSpec), type=req_single(*Types), 
    dims=opt_array(Dimension), assignment=opt_single(Expression))


















# Container classes
Name = Container.create_subclass("Name", val=str)
Type = Container.create_subclass("Type", val=str)
Dimension = Container.create_subclass("Dimension", val=int)
Assignment = Container.create_subclass("Assignment", val=int)
Variable = Container.create_subclass("Variable", name=Name, type=Type, dimension=Dimension, assignment=Assignment)

# Names
var1 = Name(val="var1")
var2 = Name(val="var2")
var3 = Name(val="var3")
var4 = Name(val="var4")
var5 = Name(val="var5")

# Types
type1 = Type(val="int")
type2 = Type(val="real")

# Dimensions
dimension1 = Dimension(val=1)

# Assignment
assignment1 = Assignment(val=5)
assignment2 = Assignment(val=10)

variable_args1 = [
    [var1, var2, var3, var4, var5],
    [type1],
    [dimension1],
    [assignment1],
]

variable_args2 = [
    [var1, var2, var3, var4, var5],
    [type1, type2],
    [dimension1],
    [assignment1],
]

variable_args3 = [
    [var1, var2, var3, var4, var5],
    [type1],
    [dimension1],
    [],
]


vars = Variable.create_all(*variable_args1)
for var in vars:
    for arg_name, arg in var.__dict__.items():
        print(arg_name, arg.val)
    print()
