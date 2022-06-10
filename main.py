import tree

if __name__ == "__main__":
    full_tree = tree.FullTree(tree.node.NamedNode, 2, 3)
    full_tree.iter_strategy = tree.iterations.DFS()

    for node in full_tree:
        print(node, node.is_leaf())
