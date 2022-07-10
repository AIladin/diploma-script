from collections import deque


from . import base


class BFS(base.BaseIterationAlgo):
    def run(self, current_node):
        queue = deque()
        queue.appendleft(current_node)

        while queue:
            current_node = queue.pop()
            yield current_node
            if not current_node.is_leaf():
                for child in current_node.iter_children():
                    queue.appendleft(child)
