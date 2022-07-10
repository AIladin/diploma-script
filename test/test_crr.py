from functools import partial

import numpy as np
import pandas as pd

from main import CRRModel, CRRModelCalculator

CRR_TESTS = "test/data/CRR_tests.csv"


def csv_reader():
    df = pd.read_csv(CRR_TESTS, index_col=0)
    for i, row in df.iterrows():
        yield (row[0], 1, row[1], row[3], row[2]), row[4], row[5], row[6]


def put_fn(x: np.ndarray, k=0) -> np.ndarray:
    return (x - k).clip(0.0)


def test_fair_price():
    for node_args, k, n, cn in csv_reader():
        model = CRRModel(*node_args)
        payment_fn = partial(put_fn, k=k)
        calculator = CRRModelCalculator(model, payment_fn, int(n))
        assert np.allclose(calculator.get_fair_price()[0], cn)


def test_k_zero():
    for node_args, k, n, cn in csv_reader():
        model = CRRModel(*node_args)
        payment_fn = partial(put_fn, k=0)
        calculator = CRRModelCalculator(model, payment_fn, int(n))
        assert np.allclose(
            calculator.get_fair_price()[0], node_args[0]
        ), f"{node_args, k, n, cn}"
