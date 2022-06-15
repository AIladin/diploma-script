import tree
import tree.iterations

if __name__ == "__main__":
    full_tree = tree.FullBinaryTree(tree.node.CRRNodeFactory(s_0 = 100,
    b_0 = 50,
    a = -0.5,
    b = 0.5,
    r = 0.1,), 21)
    full_tree.iter_strategy = tree.iterations.DFS()

    for node in full_tree:
        print(node, node.discounted_evolution)
