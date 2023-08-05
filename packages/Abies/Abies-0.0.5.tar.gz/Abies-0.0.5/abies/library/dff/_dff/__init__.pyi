"""Python Bindings"""
from abies.framework import Framework

__all__ = [
    "framework_version",
    "register_with",
]

def framework_version() -> int:
    pass

def register_with(framework: Framework, name: str) -> None:
    pass
