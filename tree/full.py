from typing import Optional, Type

import tree.base as base
import tree.node.base as node_base


class FullTree(base.Tree):
    @classmethod
    def _build_full_tree(
        cls,
        node_class: Type[node_base.Node],
        n_ary: int,
        n_levels: int,
        current_node: Optional[node_base.Node] = None,
    ) -> node_base.Node:
        if current_node is None:
            current_node = node_class()

        if n_levels > 1:

            for i in range(n_ary):
                child = node_class(parent=current_node)
                current_node.childern.append(
                    cls._build_full_tree(
                        node_class,
                        n_ary,
                        n_levels - 1,
                        child,
                    )
                )

        return current_node

    def __init__(
        self,
        node_class: Type[node_base.Node],
        n_ary: int,
        n_levels: int,
    ):
        super().__init__(self._build_full_tree(node_class, n_ary, n_levels))
