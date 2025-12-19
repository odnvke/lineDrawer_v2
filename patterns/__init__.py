"""
Паттерны для параметрического рисования
"""
from .base_pattern import BasePattern
from .connect import ConnectPattern
from .connect_all import ConnectAllPattern
from .connect_to_next import ConnectToNextPattern
from .connect_closed import ConnectClosedPattern

__all__ = [
    'BasePattern',
    'ConnectPattern',
    'ConnectAllPattern',
    'ConnectToNextPattern',
    'ConnectClosedPattern'
]