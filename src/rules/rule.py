from pathlib import Path
from abc import ABC, abstractmethod

class Rule(ABC):
    @abstractmethod
    def match(self, path: Path) -> bool:
        raise NotImplementedError