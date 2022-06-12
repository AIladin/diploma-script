import tree.iterations.base as base

import tree.node.base as node_base


class DFS(base.BaseIterationAlgo):
    def run(self, current_node: node_base.Node):
        yield current_node
        if not current_node.is_leaf():
            for child in current_node.children:
                yield from self.run(child)
