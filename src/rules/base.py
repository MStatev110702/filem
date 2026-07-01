from pathlib import Path
from abc import ABC, abstractmethod

class rule(ABC):
    @abstractmethod
    def match(self, path: Path) -> bool:
        ...