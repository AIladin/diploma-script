import tree
import tree.iterations
from tree.node import payment_functions

if __name__ == "__main__":
    full_tree = tree.FullBinaryTree(
        tree.node.CRRNodeFactory(
            s_0=102,
            b_0=1,
            a=-0.1,
            b=0.33,
            r=0.03,
            payment_function=payment_functions.CallPayment(100),
        ),
        5,
    )
    print(full_tree.root.fair_price / (1 + full_tree.root.r) ** 5)
