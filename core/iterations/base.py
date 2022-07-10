from abc import ABC, abstractmethod
from typing import Iterable


class BaseIterationAlgo(ABC):
    @abstractmethod
    def run(self, current_node) -> Iterable:
        pass
