import tree.iterations.base as base
import tree.node.base as node_base
from collections import deque


class BFS(base.BaseIterationAlgo):
    def run(self, current_node: node_base.Node):
        queue = deque()
        queue.appendleft(current_node)

        while queue:
            current_node: node_base.Node = queue.pop()
            yield current_node
            if not current_node.is_leaf():
                for child in current_node.children:
                    queue.appendleft(child)
