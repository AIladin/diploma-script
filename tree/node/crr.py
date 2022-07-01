from functools import cached_property

import tree.node.base as base

from . import payment_functions


class CRRNode(base.Node):
    def __init__(
        self,
        s_0: float,
        b_0: float,
        a: float,
        b: float,
        r: float,
        payment_function: payment_functions.BasePayment,
    ):
        assert -1 < a < r < b

        self.s_0 = s_0
        self.b_0 = b_0
        self.a = a
        self.b = b
        self.r = r
        self.payment_function = payment_function
        super().__init__()

    @cached_property
    def bank_account_evolution(self) -> float:
        if self.is_root():
            return self.b_0
        return self.parent.bank_account_evolution * (1 + self.r)

    @cached_property
    def stock_price_evolution(self) -> float:
        if self.is_root():
            return self.s_0

        if self.node_type == base.NodeType.OMEGA_1:
            return self.parent.stock_price_evolution * (1 + self.a)
        elif self.node_type == base.NodeType.OMEGA_2:
            return self.parent.stock_price_evolution * (1 + self.b)
        else:
            raise ValueError("Unknown node type.")

    @property
    def discounted_evolution(self) -> float:
        return self.stock_price_evolution / self.bank_account_evolution

    @cached_property
    def psi(self):
        p_star = (self.b - self.r) / (self.b - self.a)
        if self.node_type == base.NodeType.OMEGA_1:
            return p_star  # TODO ask swapped here
        elif self.node_type == base.NodeType.OMEGA_2:
            return 1 - p_star
        else:
            raise ValueError("Unknown node type.")

    @cached_property
    def measure(self):
        if self.is_root():
            return 1
        return self.psi * self.parent.measure

    @cached_property
    def fair_price(self):
        if self.is_leaf():
            return self.measure * self.payment_function(self.stock_price_evolution)
        else:
            return self.omega_1_child.fair_price + self.omega_2_child.fair_price


class CRRNodeFactory(base.NodeFactory):
    def __init__(
        self,
        s_0: float,
        b_0: float,
        a: float,
        b: float,
        r: float,
        payment_function: payment_functions.BasePayment,
    ):
        assert -1 < a < r < b

        self.s_0 = s_0
        self.b_0 = b_0
        self.a = a
        self.b = b
        self.r = r
        self.payment_function = payment_function

    def create_node(self):
        return CRRNode(
            self.s_0, self.b_0, self.a, self.b, self.r, self.payment_function
        )
