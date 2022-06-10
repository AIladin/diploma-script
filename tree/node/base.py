from typing import List, Optional


class Node:
    def __init__(
        self,
        parent: Optional["Node"] = None,
        childern: Optional[List["Node"]] = None,
    ):
        self.parent = parent
        self.childern = childern if childern is not None else []

    def is_leaf(self):
        return len(self.childern) == 0
