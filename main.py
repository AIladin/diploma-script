import tree
from tree.iterations import BFS
from tree.node import payment_functions

if __name__ == "__main__":
    full_tree = tree.FullBinaryTree(
        tree.node.CRRNodeFactory(
            s_0=102,
            b_0=1,
            a=-0.1,
            b=0.33,
            r=0.03,
            payment_function=payment_functions.CallPayment(0),
        ),
        3,
    )
    full_tree.iter_strategy = BFS()
    for node in full_tree:
        print(node, node.discounted_capital)
