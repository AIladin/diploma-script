from collections import deque
from typing import Optional

from tqdm import tqdm

from tree.node.base import Node, NodeFactory, NodeType


class FullBinaryTreeBuilder:
    def __init__(
        self,
        node_factory: NodeFactory,
        n_levels: int,
        root_node: Optional[Node] = None,
    ):
        self.node_factory = node_factory
        self.n_levels = n_levels
        self.root_node = (
            root_node if root_node is not None else node_factory.create_node()
        )

    def reset(self):
        self.root_node = self.node_factory.create_node()

    def build_full_tree(
        self,
    ) -> Node:
        required_nodes = 2 ** (self.n_levels + 1) - 1

        pbar = tqdm(
            desc=f"Buliding full binary tree with {self.n_levels} levels.",
            total=required_nodes,
        )

        print(self.root_node)
        queue = deque()
        queue.appendleft(self.root_node)
        pbar.update(1)
        required_nodes -= 1

        while required_nodes > 0:
            current_node: Node = queue.pop()

            child_1 = self.node_factory.create_node(current_node, NodeType.OMEGA_1)
            queue.appendleft(child_1)
            pbar.update(1)

            child_2 = self.node_factory.create_node(current_node, NodeType.OMEGA_2)
            queue.appendleft(child_2)
            pbar.update(1)
            required_nodes -= 2

        return self.root_node
