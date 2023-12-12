from typing import Iterable, Type, TypeVar
from abc import ABC, abstractmethod
from io import StringIO
import re
from subprocess import check_output
from exploratory.basic.nodes import AbstractNode

# Type hinting variables
N = TypeVar("N", bound=AbstractNode)
V = TypeVar("V", int, str, float)
VAL = V | list[V] | None


class Parser(Iterable, ABC):
    
    def __init__(self, filepath : str):
        self.filepath = filepath
    
    def parse_value(self, value_str : str, value_cls : Type[V]) -> VAL:
        
        # Value is not None
        if len(value_str) > 0:
            
            # Value is a list
            if value_str[0] == "[" and value_str[-1] == "]":
                return list(value_cls(s.strip()) for s in value_str[1:-1].split(','))
            
            # Value is a scalar
            else:
                return value_cls(value_str.strip())
    
    @abstractmethod
    def __iter__(self) -> tuple[int, N]:
        pass
    

def StandardParser(node_cls : Type[N], value_cls : Type[V]) -> Type[Parser]:
    
    class __StandardParser(Parser):
        
        def __init__(self, filepath : str):
            Parser.__init__(self, filepath)
            
        def __iter__(self) -> tuple[int, N]:
    
            # Open file
            f = open(self.filepath, 'r')      
            
            # Iterate over each line
            for line in f.readlines():
                
                # Parse line
                s = re.search('[^| ].*$', line)
                res = re.split(' ', s.group(), maxsplit=1)
 
                # Get depth
                depth = int(s.start() / 2)

                # Get id
                id = res[0]
                
                # Get value
                value_str = res[1]
                value = self.parse_value(value_str, value_cls)
                
                # Create node
                node = node_cls(id, value)
                
                # Yield tuple
                yield depth, node
                
            # Close file
            f.close()
            
    return __StandardParser
        
        
def FlangParser(node_cls : Type[N]) -> Type[Parser]:
    
    class __FlangParser(Parser):
        
        def __init__(self, filepath : str):
            Parser.__init__(self, filepath)
        
        def __iter__(self) -> tuple[int, N]: 
            
            # Initialize variables
            head = None
            initial_program_unit = True
            depth_state = 0
            string_state = 1
            gap_state = 2
            keyword_state = 3

            # Current line number
            line_num = 1
            
            # Open file
            raw_parse_tree = check_output("flang-new -fc1 -fdebug-dump-parse-tree-no-sema {}".format(self.filepath), shell=True, text=True)      

            # Iterate over each line of output 
            for line in StringIO(raw_parse_tree).readlines():

                if not line: continue

                # Extract the depth of the node indicated by line and its associated "->" separated keywords
                curr_depth = 0
                keyword = ""
                keywords = []
                state = depth_state
                for i in range(len(line)):
                    c = line[i]
                    match state:
                        case 0:                                         # Depth state
                            match c:
                                case " ":
                                    continue
                                case "|":
                                    curr_depth += 1
                                case "'":
                                    keyword = c
                                    state = string_state
                                case default:
                                    keyword = c
                                    state = keyword_state
                        case 1:                                         # String state
                            match c:
                                case "'":
                                    keyword += c
                                    if i == len(line) - 1:
                                        keywords.append(keyword)
                                case default:
                                    keyword += c
                        case 2:                                         # Gap state
                            match c:
                                case " " | "=":
                                    continue
                                case "'":
                                    keyword = c
                                    state = string_state
                                case default:
                                    keyword = c
                                    state = keyword_state
                        case 3:                                         # Keyword state
                            match c:
                                case " ":
                                    keywords.append(keyword)
                                    state = gap_state
                                case default:
                                    keyword += c
                                    if i == len(line) - 1:
                                        keywords.append(keyword)

                # Add 1 to the depth of lines excluding the lines in the first program unit
                if curr_depth == 0 and head is not None:
                    initial_program_unit = False
                curr_depth += not initial_program_unit
            
                # Get the node associated with the current line
                for i in range(len(keywords)):
                    depth = curr_depth + i
                    kw = keywords[i]
                    if kw[0] == "'" and kw[-1] == "'": 
                        id = "StrVal"
                        value = kw[1:-1]
                    else:
                        id = kw
                        value = None
                    yield depth, node_cls(id, value)
                    
                # Update vars
                line_num += 1

            return head
        
    return __FlangParser