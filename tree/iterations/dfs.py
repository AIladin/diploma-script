import tree.iterations.base as base

import tree.node.base as node_base


class DFS(base.BaseIterationAlgo):
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def run(self, current_node: node_base.Node):
        yield current_node
        if not current_node.is_leaf():
            for child in current_node.childern:
                yield from self.run(child)
