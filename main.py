from core import iterations, node, tree
from core.utils import payment_functions

if __name__ == "__main__":
    full_tree = tree.FullBinaryTreeBuilder(
        node.CRRNodeFactory(
            s_0=102,
            b_0=1,
            a=-0.1,
            b=0.33,
            r=0.03,
            payment_function=payment_functions.CallPayment(0),
        ),
        3,
    ).build_full_tree()
    full_tree.iter_strategy = iterations.BFS()
    for crr_node in full_tree:
        print(
            crr_node,
            f"{crr_node.discounted_capital=}",
            f"{crr_node.stock_price_evolution=}",
            f"{crr_node.measure=}",
        )
