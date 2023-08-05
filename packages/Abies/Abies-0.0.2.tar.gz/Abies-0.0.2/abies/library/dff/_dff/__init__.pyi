"""Python Bindings"""
from __future__ import annotations
import abies.library.dff._dff
import typing
import abies.framework._framework

__all__ = [
    "framework_version",
    "register_with"
]


def framework_version() -> int:
    pass
def register_with(framework: abies.framework._framework.Framework, name: str) -> None:
    pass
