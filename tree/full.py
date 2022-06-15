from collections import deque
from typing import Optional, Type

from tqdm import tqdm

import tree.base as base
import tree.node.base as node_base


class FullBinaryTree(base.Tree):
    @classmethod
    def _build_full_tree(
        cls,
        node_factory: node_base.NodeFactory,
        n_levels: int,
        root_node: Optional[node_base.Node] = None,
    ) -> node_base.Node:
        required_nodes = 2 ** (n_levels) - 1

        pbar = tqdm(
            desc=f"Buliding full binary tree with {n_levels} levels",
            total=required_nodes,
        )

        if root_node is None:
            root_node = node_factory.create_node()
        pbar.update(1)
        required_nodes -= 1

        queue = deque()
        queue.appendleft(root_node)

        while required_nodes > 0:
            current_node: node_base.Node = queue.pop()

            child_1 = node_factory.create_node()
            current_node.omega_1_child = child_1
            queue.appendleft(child_1)
            pbar.update(1)

            child_2 = node_factory.create_node()
            current_node.omega_2_child = child_2
            queue.appendleft(child_2)
            pbar.update(1)
            required_nodes -= 2

        return root_node

    def __init__(
        self,
        node_factory: node_base.NodeFactory,
        n_levels: int,
        root_node: Optional[node_base.Node] = None,
    ):
        super().__init__(
            self._build_full_tree(
                node_factory,
                n_levels,
                root_node,
            )
        )
