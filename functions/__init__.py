"""
Функции - математические примитивы
"""
from .function_lib import FunctionLibrary, FunctionBase
from .function_lib import (
    CircleFunction, SquareFunction, NGonFunction, FixedFunction,
    SumFunction, MultiplyFunction, MorphFunction, DirectedLineFunction
)

# Пробуем импортировать продвинутые функции
try:
    from .advanced_functions import (
        EllipseFunction, SuperEllipseFunction, HypocycloidFunction,
        EpicycloidFunction, LissajousFunction, ButterflyFunction,
        CardioidFunction, RoseFunction, SpiralFunction
    )
    HAS_ADVANCED = True
except ImportError:
    HAS_ADVANCED = False

__all__ = [
    'FunctionLibrary',
    'FunctionBase',
    'CircleFunction',
    'SquareFunction',
    'NGonFunction',
    'FixedFunction',
    'SumFunction',
    'MultiplyFunction',
    'MorphFunction',
    'DirectedLineFunction',
]

if HAS_ADVANCED:
    __all__.extend([
        'EllipseFunction',
        'SuperEllipseFunction', 
        'HypocycloidFunction',
        'EpicycloidFunction',
        'LissajousFunction',
        'ButterflyFunction',
        'CardioidFunction',
        'RoseFunction',
        'SpiralFunction'
    ])