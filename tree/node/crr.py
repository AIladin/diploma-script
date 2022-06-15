import tree.node.base as base
from functools import cached_property


class CRRNode(base.Node):
    def __init__(self, s_0: float, b_0: float, a: float, b: float, r: float):
        assert -1 < a < r < b

        self.s_0 = s_0
        self.b_0 = b_0
        self.a = a
        self.b = b
        self.r = r
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


class CRRNodeFactory(base.NodeFactory):
    def __init__(self, s_0: float, b_0: float, a: float, b: float, r: float):
        assert -1 < a < r < b

        self.s_0 = s_0
        self.b_0 = b_0
        self.a = a
        self.b = b
        self.r = r

    def create_node(self):
        return CRRNode(self.s_0,
                       self.b_0,
                       self.a,
                       self.b,
                       self.r)
