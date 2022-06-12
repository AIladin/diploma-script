from abc import ABC, abstractmethod
from typing import Iterable

import tree.node.base as node_base


class BaseIterationAlgo(ABC):
    @abstractmethod
    def run(self, current_node: node_base.Node) -> Iterable[node_base.Node]:
        pass
