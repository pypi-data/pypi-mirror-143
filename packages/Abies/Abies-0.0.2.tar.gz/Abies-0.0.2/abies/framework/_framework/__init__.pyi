"""Framework Python Bindings"""
from pathlib import Path

__all__ = ["Framework"]

class Framework:
    def __init__(self, log_dir: Path = Path("logs")) -> None: ...
    def initialize(self, netlist: list[tuple[str, str]]) -> None: ...
    def run(self, duration: int = 1) -> None: ...
    @property
    def log_level(self) -> str:
        """
        :type: str
        """
    @log_level.setter
    def log_level(self, arg1: str) -> None:
        pass
    @property
    def trace(self) -> bool:
        """
        :type: bool
        """
    @trace.setter
    def trace(self, arg1: bool) -> None:
        pass
    pass
