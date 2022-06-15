from typing import Optional

import tree.node.base as base


class NamedNode(base.Node):
    def __init__(self, name: Optional[str] = None, **kwargs):
        self.name = name
        super().__init__(**kwargs)

    def _dict_info(self):
        dict_info = super()._dict_info()
        dict_info.update({"name": self.name})
        return dict_info


class NamedNodeFactory(base.NodeFactory):
    def __init__(self):
        self.last_node_name = 0

    def create_node(self):
        node = NamedNode(str(self.last_node_name))
        self.last_node_name += 1
        return node
