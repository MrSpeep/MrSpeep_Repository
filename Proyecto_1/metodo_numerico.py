from abc import ABC, abstractmethod

class MetodoNumerico(ABC):
    @abstractmethod
    def solve(self, t_span, y0):
        pass