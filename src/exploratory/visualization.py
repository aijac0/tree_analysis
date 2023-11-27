import networkx as nx 
import matplotlib.pyplot as plt 
from collections import deque
from utilities.types.tree_node import TreeNode


def create_graph(tree : TreeNode):
    
    # Initialize graph
    G = nx.DiGraph()
    
    # BFS
    encountered = set()
    queue = deque([])
    queue.append(tree)
    while queue:
        curr = queue.popleft()
        if curr.name() in encountered: continue
        encountered.add(curr.name())
        for next in curr.children:
            G.add_edge(curr.name(), next.name())
            queue.append(next)
    
    return G
  
  
def visualize_graph(graph : nx.DiGraph):
    
    # Show graph
    nx.draw_networkx(graph) 
    plt.show() 