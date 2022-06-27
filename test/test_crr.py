import tree
import pandas as pd
from tree.node import payment_functions


CRR_TESTS = 'data/CRR_tests.csv'


def csv_reader():
    df = pd.read_csv(CRR_TESTS, index_col=0)
    for i, row in df.iterrows():
        yield (row[0], 1, row[1], row[3], row[2]), row[4], row[5], row[6]


def test_fair_price():
    for node_args, k, n, cn in csv_reader():
        full_tree = tree.FullBinaryTree(tree.node.CRRNodeFactory(*node_args,
                                                                 payment_function=payment_functions.CallPayment(k)), n,)
        assert full_tree.root.fair_price == cn


def test_k_zero():
    for node_args, k, n, cn in csv_reader():
        full_tree = tree.FullBinaryTree(tree.node.CRRNodeFactory(*node_args,
                                                                 payment_function=payment_functions.CallPayment(0)),
                                        n, )
        assert full_tree.root.fair_price == node_args[0]
