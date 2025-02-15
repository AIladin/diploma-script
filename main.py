from functools import lru_cache, partial
from typing import Callable, Optional

import numpy as np
from scipy.special import binom


class CRRModel:
    """Cox Ross Rubinstein model."""

    def __init__(
        self,
        s_0: float,
        b_0: float,
        a: float,
        b: float,
        r: float,
    ):
        assert -1 < a < r < b
        self.a = a
        self.b = b
        self.s_0 = s_0
        self.b_0 = b_0
        self.r = r

    @lru_cache(maxsize=None)
    def bank_account_evolution(self, n: int) -> float:
        if n == 0:
            return self.b_0
        return self.bank_account_evolution(n - 1) * (1 + self.r)

    @lru_cache(maxsize=None)
    def stock_price_evolution(self, n: int) -> np.ndarray:
        if n == 0:
            return np.array([self.s_0])
        previous_step = self.stock_price_evolution(n - 1)
        return np.concatenate(
            [
                previous_step * (1 + self.a),
                previous_step * (1 + self.b),
            ]
        )

    def discounted_evolution(self, n: int) -> np.ndarray:
        return self.stock_price_evolution(n) / self.bank_account_evolution(n)


PAYMENT_FUCTION_TYPE = Callable[[np.ndarray], np.ndarray]

cached_binom = lru_cache(maxsize=None)(binom)


class CRRModelCalculator:
    """Calculates fair price, gamma, beta, X, for Cox Ross Rubinstein model."""

    def __init__(
        self,
        model: CRRModel,
        payment_function: PAYMENT_FUCTION_TYPE,
        N: int,
    ):
        self.model = model
        self.payment_fuction = payment_function
        self.N = N

    @property
    def p_star(self) -> float:
        return (self.model.r - self.model.a) / (self.model.b - self.model.a)

    def f(self, m: int, x: float, p: float):
        """Helper function from monography page 56."""
        res = 0
        for k in range(0, m + 1):
            res += (
                self.payment_fuction(
                    x * (1 + self.model.b) ** k * (1 + self.model.a) ** (m - k)
                )
                * cached_binom(m, k)
                * p**k
                * (1 - p) ** (m - k)
            )
        return res

    @lru_cache(maxsize=None)
    def get_discounted_capital(self, n: int) -> np.ndarray:
        assert 0 <= n <= self.N
        stock_price_evolution = self.model.stock_price_evolution(n)
        print(self.f(
            self.N - n,
            stock_price_evolution,
            self.p_star,
        ))
        return (1 + self.model.r) ** (n - self.N) * self.f(
            self.N - n,
            stock_price_evolution,
            self.p_star,
        )

    def get_fair_price(self):
        return self.get_discounted_capital(0)

    @lru_cache(maxsize=None)
    def get_gamma(
        self,
        n: int,
    ) -> np.ndarray:
        assert 1 <= n <= self.N
        stock_price_evolution = self.model.stock_price_evolution(n - 1)
        return (
            (1 + self.model.r) ** (n - self.N)
            / stock_price_evolution
            / (self.model.b - self.model.a)
            * (
                self.f(
                    self.N - n,
                    stock_price_evolution * (1 + self.model.b),
                    self.p_star,
                )
                - self.f(
                    self.N - n,
                    stock_price_evolution * (1 + self.model.a),
                    self.p_star,
                )
            )
        )

    @lru_cache(maxsize=None)
    def get_beta(
        self,
        n: int,
    ) -> np.ndarray:
        assert 1 <= n <= self.N
        return (
            self.get_discounted_capital(n - 1)
            - self.get_gamma(n) * self.model.stock_price_evolution(n - 1)
        ) / self.model.bank_account_evolution(n - 1)


class CRRPlotter(CRRModelCalculator):
    def get_gamma(
        self,
        n: int,
        stock_price_evolution: np.ndarray,
    ) -> np.ndarray:
        assert 1 <= n <= self.N
        return (
            (1 + self.model.r) ** (n - self.N)
            / stock_price_evolution
            / (self.model.b - self.model.a)
            * (
                self.f(
                    self.N - n,
                    stock_price_evolution * (1 + self.model.b),
                    self.p_star,
                )
                - self.f(
                    self.N - n,
                    stock_price_evolution * (1 + self.model.a),
                    self.p_star,
                )
            )
        )

    def get_beta(
        self,
        n: int,
        stock_price_evolution: np.ndarray,
    ) -> np.ndarray:
        assert 1 <= n <= self.N
        return self.f(
            self.N - n + 1, stock_price_evolution, self.p_star
        ) / self.model.bank_account_evolution(self.N) - (1 + self.model.r) * (
            self.f(self.N - n, stock_price_evolution * (1 + self.model.b), self.p_star)
            - self.f(
                self.N - n, stock_price_evolution * (1 + self.model.a), self.p_star
            )
        ) / (
            self.model.bank_account_evolution(self.N) * (self.model.b - self.model.a)
        )


def put_fn(x: np.ndarray, k=0) -> np.ndarray:
    return (x - k).clip(0.0)

if __name__ == '__main__':
    model = CRRModel(102, 1, -0.1, 0.33, 0.03)
    fn = partial(put_fn, k=0)
    calculator = CRRModelCalculator(model, fn, 3)
    for i in range(4):
        print(calculator.get_discounted_capital(i))
