"""Abies Plugin Module"""
from abies.framework._framework import Framework

def framework_version() -> str:
    """Return the version of the framework api that this plugin was built with."""
    pass

def register_with(framework: Framework, name: str) -> None:
    """Function to register this module in the Abies framework."""
    pass
