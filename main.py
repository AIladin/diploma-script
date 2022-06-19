import tree
import tree.iterations
from tree.node import payment_functions

if __name__ == "__main__":
    full_tree = tree.FullBinaryTree(tree.node.CRRNodeFactory(s_0 = 100,
                                                             b_0 = 50,
                                                             a = -0.5,
                                                             b = 0.5,
                                                             r = 0.1,
                                                             payment_function=payment_functions.CallPayment(10)),
                                                             21,
                                                             )
    #full_tree.iter_strategy = tree.iterations.BFS()
    print(full_tree.root.fair_price)
#    for node in full_tree:
 #       print(node, node.discounted_evolution)
