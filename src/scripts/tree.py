from exploratory.basic.trees import Tree
from exploratory.basic.nodes import Node
from exploratory.basic.parsers import StandardParser
from exploratory.basic.structures import TreeStructure, StructureQueryTool
from exploratory.tools.files import get_files
from collections import deque

def test1():
    
    filepath = "data/raw/CASL/Futility/cmake/tribits/examples/TribitsExampleProject/packages/mixed_lang/src/Parameters.txt"
    structure = TreeStructure()
    tree = Tree.from_file(filepath)
    tree_id = structure.add_tree(tree)
    structure = structure.restructure("Expr")
    structure.to_file("test_structure.txt")

def test2():
    structure = TreeStructure()
    for filepath in get_files("data", "txt")[:100]:
        tree = Tree.from_file(filepath)
        tree_id = structure.add_tree(tree)
        print(tree_id)
    """s = structure.restructure("Expr")
    s.to_file("expr_structure.txt")
    s = structure.restructure("TypeDeclarationStmt")
    s.to_file("typedeclarationstmt_structure.txt")
    s = structure.restructure("SpecificationPart")
    s.to_file("specificationpart_structure.txt")"""
    s = structure.restructure("Expr")
    s.to_file("test_structure.txt")

    
def test3():
    
    structure = TreeStructure()
    i = 1
    for filepath in get_files("data", "txt")[:100]:
        tree = Tree.from_file(filepath)
        for path in tree.paths():
            visited = set()
            for node in path:
                if node.id not in visited:
                    visited.add(node.id)
                elif node != path[-1]:
                    print(filepath)
                    print(node.id)
                    print(" ".join(i.id for i in path))
                    print()
    
    
def test4():
    structure = TreeStructure()
    for filepath in get_files("data", "txt")[:1000]:
        tree = Tree.from_file(filepath)
        tree_id = structure.add_tree(tree)
        print(tree_id)
    """s = structure.restructure("Expr")
    s.to_file("expr_structure.txt")
    s = structure.restructure("TypeDeclarationStmt")
    s.to_file("typedeclarationstmt_structure.txt")
    s = structure.restructure("SpecificationPart")
    s.to_file("specificationpart_structure.txt")"""
    s = structure.restructure("Expr")
    s.to_file("test_structure.txt")

def test5():
    
    paths = []
    paths.append(["Expr"])
    paths.append(["Expr", "Subtract", "Expr", "Subtract"])
    d = deque()
    for path in paths:
        p = deque()
        for id in path:
            new = Node(id)
            p.append(new)
        d.append(p)
        
    a = lambda X : X[0] > 0 and X[1] > 0
        
    structure = TreeStructure()
    for filepath in get_files("data", "txt")[:500]:
        tree = Tree.from_file(filepath)
        tree_id = structure.add_tree(tree)
        print(tree_id)
    
    s = structure.restructure("Expr")
    sqt = StructureQueryTool(s)
    q = sqt.query(d, a)
    print(q)

if __name__ == "__main__":    
    
    test5()