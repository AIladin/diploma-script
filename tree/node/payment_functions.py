from typing import Callable
from abc import ABC, abstractmethod

PAYMENT_FUNCTION_TYPE = Callable[[float], float]


class BasePayment(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class CallPayment(BasePayment):
    def __init__(self, k: float):
        self.k = k

    def __call__(self, s_n: float):
        return max(0.0, s_n - self.k)
