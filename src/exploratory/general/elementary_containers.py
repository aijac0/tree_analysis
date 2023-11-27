from base_containers import ElementaryContainer
from enum import Enum

# create_all() class method for existential containers
tautology = lambda cls : [True]
contradiction = lambda cls : [False]

# Intent enum
IntentEnum = Enum('IntentEnum', ['in', 'out', 'inout'])
InIntent = IntentEnum['in']
OutIntent = IntentEnum['out']
InOutIntent = IntentEnum['inout']

# Type enum
TypeEnum = Enum('TypeEnum', ['complex', 'double'])
ComplexType = TypeEnum['complex']
DoubleType = TypeEnum['double']

# Indicator enum
IndicatorEnum = Enum['IndicatorEnum', ['star']]
StarIndicator = IndicatorEnum['star']

# Attribute existential containers
isTarget = ElementaryContainer('isTarget', tautology)
isSave = ElementaryContainer('isSave', tautology)
isParameter = ElementaryContainer('isParameter', tautology)
isAllocatable = ElementaryContainer('isAllocatable', tautology)
isPointer = ElementaryContainer('isPointer', tautology)
isOptional = ElementaryContainer('isOptional', tautology)

# Intent container
Intent = ElementaryContainer('Intent', lambda key : [IntentEnum[key]])

# Type container
Type = ElementaryContainer('Type', lambda key : [TypeEnum[key]])

# Indicator container
Indicator = ElementaryContainer('Indicator', lambda key : [IndicatorEnum[key]])