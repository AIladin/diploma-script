import numpy as np
import pandas as pd

from core import node, tree
from core.utils import payment_functions

CRR_TESTS = "test/data/CRR_tests.csv"


def csv_reader():
    df = pd.read_csv(CRR_TESTS, index_col=0)
    for i, row in df.iterrows():
        yield (row[0], 1, row[1], row[3], row[2]), row[4], row[5], row[6]


def test_fair_price():
    for node_args, k, n, cn in csv_reader():
        tree_builder = tree.FullBinaryTreeBuilder(
            node.CRRNodeFactory(
                *node_args, payment_function=payment_functions.CallPayment(k)
            ),
            n,
        )
        tree_root = tree_builder.build_full_tree()
        assert np.allclose(tree_root.discounted_capital, cn)


def test_k_zero():
    for node_args, k, n, cn in csv_reader():
        tree_builder = tree.FullBinaryTreeBuilder(
            node.CRRNodeFactory(
                *node_args, payment_function=payment_functions.CallPayment(0)
            ),
            n,
        )
        tree_root = tree_builder.build_full_tree()
        assert np.allclose(tree_root.discounted_capital, node_args[0])
