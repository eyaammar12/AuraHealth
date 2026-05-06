from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    """
    Abstract Base Class for AI Providers.
    Ensures all providers implement the analyze method.
    """
    @abstractmethod
    def analyze(self, symptoms: list, severity: int, duration: int, notes: str = "") -> dict:
        pass
