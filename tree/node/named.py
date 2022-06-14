from typing import Optional

import tree.node.base as base

LAST_NODE_NAME = 0


class NamedNode(base.Node):
    __slots__ = ("name",)

    def __init__(self, name: Optional[str] = None, **kwargs):
        global LAST_NODE_NAME

        if name is None:
            self.name = str(LAST_NODE_NAME)
            LAST_NODE_NAME += 1
        else:
            self.name = name

        super().__init__(**kwargs)

    def _dict_info(self):
        dict_info = super()._dict_info()
        dict_info.update({"name": self.name})
        return dict_info
