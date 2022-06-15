import tree
import tree.iterations

if __name__ == "__main__":
    full_tree = tree.FullBinaryTree(tree.node.NamedNodeFactory(), 3)
    full_tree.iter_strategy = tree.iterations.DFS()

    for node in full_tree:
        print(node)
