from functools import cached_property
from typing import Optional

from core.utils import payment_functions

from . import base


class CRRNode(base.Node):
    __slots__ = (
        "payment_function",
        "bank_account_evolution",
        "stock_price_evolution",
        "psi",
        "r",
        "_measure",
        "_discounted_capital",
    )

    def __init__(
        self,
    ):
        super().__init__()
        self.payment_function = None
        self.bank_account_evolution = None
        self.stock_price_evolution = None
        self.psi = None
        self.r = None
        self._measure = None
        self._discounted_capital = None

        super().__init__()

    @property
    def measure(self):
        # TODO rework
        if self._measure is None:
            if self.is_root():
                self._measure = 1
            else:
                self._measure = self.psi * self.parent.measure
        return self._measure

    @property
    def discounted_capital(self):
        # FIXME
        if self._discounted_capital is None:
            if self.is_leaf():
                self._discounted_capital = self.measure * self.payment_function(
                    self.stock_price_evolution
                )
            else:
                self._discounted_capital = (
                    self.omega_1_child.discounted_capital
                    + self.omega_2_child.discounted_capital
                ) / (1 + self.r)
        return self._discounted_capital


class CRRNodeFactory(base.NodeFactory):
    NODE_TYPE = CRRNode

    def __init__(
        self,
        s_0: float,
        b_0: float,
        a: float,
        b: float,
        r: float,
        payment_function: payment_functions.BasePayment,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        assert -1 < a < r < b

        self.s_0 = s_0
        self.b_0 = b_0
        self.a = a
        self.b = b
        self.r = r
        self.payment_function = payment_function

    @cached_property
    def p_star(self):
        return (self.r - self.a) / (self.b - self.a)

    def _create_root_node(self) -> CRRNode:
        node: CRRNode = super()._create_root_node()
        node.payment_function = self.payment_function
        node.bank_account_evolution = self.b_0
        node.stock_price_evolution = self.s_0
        node.r = self.r
        return node

    def _create_omega_1_node(self, parent: CRRNode) -> CRRNode:
        node: CRRNode = super()._create_omega_1_node(parent)
        node.payment_function = self.payment_function
        node.bank_account_evolution = parent.bank_account_evolution * (1 + self.r)
        node.stock_price_evolution = parent.stock_price_evolution * (1 + self.a)
        node.psi = 1 - self.p_star
        node.r = self.r
        return node

    def _create_omega_2_node(self, parent: CRRNode) -> CRRNode:
        node: CRRNode = super()._create_omega_2_node(parent)
        node.payment_function = self.payment_function
        node.bank_account_evolution = parent.bank_account_evolution * (1 + self.r)
        node.stock_price_evolution = parent.stock_price_evolution * (1 + self.b)
        node.psi = self.p_star
        node.r = self.r
        return node

    def create_node(
        self,
        parent: Optional[CRRNode] = None,
        node_type: Optional[base.NodeType] = base.NodeType.ROOT,
    ) -> CRRNode:
        return super().create_node(parent, node_type)
