from typing import Iterable
from abc import ABC, abstractmethod
import re
from subprocess import check_output
from io import StringIO


class Parser(Iterable, ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __iter__(self) -> tuple[int, str]:
        pass
        

class StandardParser(Parser):
    
    def __init__(self, filepath : str):
        self.filepath = filepath 
        
    def __iter__(self) -> tuple[int, str]:
    
        # Open file
        f = open(self.filepath, 'r')      
        
        # Iterate over each line
        for line in f.readlines():
            
            # Get depth
            # Get identifier
            s = re.search('[^| ].*$', line)
            depth = int(s.start() / 2)
            identifier = s.group()
            yield depth, identifier
            
        # Close file
        f.close()
        
        
class FlangParser(Parser):
    
    def __init__(self, filepath : str):
        self.filepath = filepath 
        
    def __iter__(self) -> tuple[int, str]: 
        
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
                yield depth, kw
                
            # Update vars
            line_num += 1

        return head