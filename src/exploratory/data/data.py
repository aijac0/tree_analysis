from edge_counts import init_edge_counts
from adjacent_counts import init_adjacent_counts
from path_counts import init_path_counts
from node_classes import init_node_classes
from exploratory.tools.files import get_sources

def get_trees(filepaths : list[str]):
    """
    Get list of abstract syntax trees from Fortran source files under a root directory
    """
    
    # Get list of abstract syntax trees parsed from each source file
    #trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
    
    return trees


def init_data(src_rootdir : str, data_rootdir : str):
    """
    Initialize data parsed from source files
    """
    
    # Get source files
    filepaths = get_sources(src_rootdir)
    
    # Generate trees
    trees = get_trees(filepaths)
    
    # Get and write edge counts to file
    edge_counts = init_edge_counts(trees, data_rootdir)
    
    # Get and write adjacent counts to file
    adj_counts = init_adjacent_counts(trees, data_rootdir)
    
    # Get and write path counts to file
    path_counts = init_path_counts(trees, data_rootdir)
    
    # Get and write node class parameters and node class declarations to file
    node_classes = init_node_classes(edge_counts, adj_counts, data_rootdir)

    return edge_counts, adj_counts, path_counts
    
    
if __name__ == "__main__":

    # Initialize data
    src_rootdir = "codes"
    data_rootdir = "data"
    init_data(src_rootdir, data_rootdir)