from exploratory.tools.files import get_files, get_sources
from exploratory.basic.trees import Tree
from exploratory.basic.nodes import Node
import os

def convert_extension_to_txt():
    
    # Get filepaths
    filepaths = get_sources("data")
    
    # Rename filepaths
    for filepath in filepaths: 
        new_filepath = ".".join(filepath.split(".")[:-1]) + ".txt"
        os.rename(filepath, new_filepath)
    

def convert_raw_text_files():
    
    # Get filepaths
    filepaths = get_files("data", "txt")
    
    # Iterate over each filepath
    for i in range(len(filepaths)):
        filepath = filepaths[i]
        print("{} / {}".format(i+1, len(filepaths)))
        
        # Load tree
        tree = Tree.from_file(filepath)

        # DFS
        for _, node in tree.dfs():
            
            # Change value & id
            if len(node.id) > 1:
                if node.id[0] == "'" and node.id[-1] == "'":
                    node.value = node.id[1:-1]
                    node.id = "ValueStr"
                elif node.id[0] == "'":
                    node.value = node.id[1:]
                    node.id = "ValueStr"    
                elif node.id[-1] == "'":
                    node.value = node.id[:-1]
                    node.id = "ValueStr"
              
        # Write to file
        tree.to_file(filepath)
        
        
        
convert_extension_to_txt()
convert_raw_text_files()