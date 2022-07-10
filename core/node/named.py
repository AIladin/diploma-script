from typing import Optional

from . import base


class NamedNode(base.Node):
    __slots__ = ("name",)

    def __init__(self):
        self.name = None
        super().__init__()

    def _dict_info(self):
        dict_info = super()._dict_info()
        dict_info.update({"name": self.name})
        return dict_info


class NamedNodeFactory(base.NodeFactory):
    def __init__(self):
        self.last_node_name = 0

    def _create_root_node(self) -> NamedNode:
        node: NamedNode = super()._create_root_node()
        node.name = str(self.last_node_name)
        self.last_node_name += 1
        return node

    def _create_omega_1_node(self, parent: NamedNode) -> NamedNode:
        node: NamedNode = super()._create_omega_1_node(parent)
        node.name = str(self.last_node_name)
        self.last_node_name += 1
        return node

    def _create_omega_2_node(self, parent: NamedNode) -> NamedNode:
        node: NamedNode = super()._create_omega_2_node(parent)
        node.name = str(self.last_node_name)
        self.last_node_name += 1
        return node

    def create_node(
        self,
        parent: Optional[NamedNode] = None,
        node_type: Optional[base.NodeType] = base.NodeType.ROOT,
    ) -> NamedNode:
        return super().create_node(parent, node_type)
