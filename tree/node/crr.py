import tree.node.base as base

from . import payment_functions


class CRRNode(base.Node):
    __slots__ = (
        "s_0",
        "b_0",
        "a",
        "b",
        "r",
        "payment_function",
        "_bank_account_evolution",
        "_stock_price_evolution",
        "_psi",
        "_measure",
        "_discounted_capital",
    )

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

        # vars for caching
        self._bank_account_evolution = None
        self._stock_price_evolution = None
        self._psi = None
        self._measure = None
        self._discounted_capital = None

        super().__init__()

    @property
    def bank_account_evolution(self) -> float:
        if self._bank_account_evolution is None:
            if self.is_root():
                self._bank_account_evolution = self.b_0
            self._bank_account_evolution = self.parent.bank_account_evolution * (
                1 + self.r
            )
        return self._bank_account_evolution

    @property
    def stock_price_evolution(self) -> float:
        if self._stock_price_evolution is None:
            if self.is_root():
                self._stock_price_evolution = self.s_0
            elif self.node_type == base.NodeType.OMEGA_1:
                self._stock_price_evolution = self.parent.stock_price_evolution * (
                    1 + self.a
                )
            elif self.node_type == base.NodeType.OMEGA_2:
                self._stock_price_evolution = self.parent.stock_price_evolution * (
                    1 + self.b
                )
            else:
                raise ValueError("Unknown node type.")
        return self._stock_price_evolution

    @property
    def psi(self):
        if self._psi is None:
            p_star = (self.r - self.a) / (self.b - self.a)
            if self.node_type == base.NodeType.OMEGA_1:
                self._psi = 1 - p_star
            elif self.node_type == base.NodeType.OMEGA_2:
                self._psi = p_star
            else:
                raise ValueError("Unknown node type.")
        return self._psi

    @property
    def measure(self):
        if self._measure is None:
            if self.is_root():
                self._measure = 1
            else:
                self._measure = self.psi * self.parent.measure
        return self._measure

    @property
    def discounted_capital(self):
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
