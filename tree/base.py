from typing import Iterable

import tree.iterations.base as iterations_base
import tree.node.base as node_base


class Tree:
    def __init__(self, root: node_base.Node):
        self.root = root
        self.iter_strategy: iterations_base.BaseIterationAlgo = None

    def __iter__(self) -> Iterable[node_base.Node]:
        assert self.iter_strategy is not None, "Please provide iter strategy."
        yield from self.iter_strategy.run(self.root)
