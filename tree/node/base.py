from abc import ABC, abstractmethod
from typing import Iterable


class NodeType:
    ROOT = "root"
    OMEGA_1 = "omega_1"
    OMEGA_2 = "omega_2"


class Node:
    __slots__ = (
        "node_type",
        "parent",
        "_omega_1_child",
        "_omega_2_child",
        "iter_strategy",
        "_level",
    )

    def __init__(
        self,
    ):
        self.node_type: NodeType = NodeType.ROOT
        self.parent = None
        self._omega_1_child = None
        self._omega_2_child = None
        self.iter_strategy = None
        self._level = None

    def __iter__(self) -> Iterable["Node"]:
        assert self.iter_strategy is not None, "Please provide iter strategy."
        yield from self.iter_strategy.run(self)

    @property
    def omega_1_child(self):
        return self._omega_1_child

    @omega_1_child.setter
    def omega_1_child(self, node: "Node"):
        node.node_type = NodeType.OMEGA_1
        node.parent = self
        self._omega_1_child = node

    @property
    def omega_2_child(self):
        return self._omega_2_child

    @omega_2_child.setter
    def omega_2_child(self, node: "Node"):
        node.node_type = NodeType.OMEGA_2
        node.parent = self
        self._omega_2_child = node

    def is_leaf(self):
        return self.omega_1_child is None and self._omega_2_child is None

    def is_root(self):
        return self.node_type == NodeType.ROOT

    @property
    def level(self) -> int:
        if self._level is None:
            if self.is_root():
                self._level = 0
            else:
                self._level = self.parent.level + 1
        return self._level

    def __str__(self):
        return f"{self.__class__.__name__} {str(self._dict_info())}"

    def _dict_info(self):
        return {
            "node_type": self.node_type,
            "level": self.level,
            "is_leaf": self.is_leaf(),
            "is_root": self.is_root(),
        }

    def iter_children(self) -> Iterable["Node"]:
        yield self.omega_1_child
        yield self.omega_2_child


class NodeFactory(ABC):
    @abstractmethod
    def create_node(self):
        return Node()
