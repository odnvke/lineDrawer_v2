"""
function_lib.py - Основная библиотека функций
"""
import math
from typing import Dict, Any, List

# ========== БАЗОВЫЙ КЛАСС ==========
class FunctionBase:
    """База для всех математических функций"""
    
    def __init__(self, function_lib=None):
        self.function_lib = function_lib
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any]) -> List[float]:
        """Вычисляет координаты точки"""
        raise NotImplementedError
    
    def _parse_param(self, value, context: Dict[str, Any]):
        """Парсит параметр (число или выражение)"""
        if isinstance(value, str):
            return self._evaluate_expression(value, context)
        return float(value)
    
    def _evaluate_expression(self, expr: str, context: Dict[str, Any]) -> float:
        """Вычисляет математическое выражение"""
        safe_dict = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'pi': math.pi, 'e': math.e, 'tau': math.tau, 'sqrt': math.sqrt,
            'abs': abs, 'pow': math.pow, 'exp': math.exp,
            'log': math.log, 'log10': math.log10,
            'floor': math.floor, 'ceil': math.ceil, 'round': round,
            **context
        }
        try:
            return float(eval(expr, {"__builtins__": {}}, safe_dict))
        except Exception as e:
            print(f"⚠ Expression evaluation error: {e} for '{expr}'")
            return 0.0

# ========== СУЩЕСТВУЮЩИЕ ФУНКЦИИ (без изменений) ==========

class CircleFunction(FunctionBase):
    """Окружность"""
    
    def evaluate(self, params, context):
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        return [
            size * math.cos(angle),
            size * math.sin(angle)
        ]

class SquareFunction(FunctionBase):
    """Квадрат"""
    
    def evaluate(self, params, context):
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        side = int(angle // (math.pi/2)) % 4
        t = (angle % (math.pi/2)) / (math.pi/2)
        
        if side == 0:
            return [size * (1 - 2*t), size]
        elif side == 1:
            return [size, size * (1 - 2*t)]
        elif side == 2:
            return [size * (-1 + 2*t), -size]
        else:
            return [-size, size * (-1 + 2*t)]

class NGonFunction(FunctionBase):
    """N-угольник с поддержкой дробных сторон"""
    
    def evaluate(self, params, context):
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        sides = self._parse_param(params.get('sides', 5), context)
        
        # Нормализуем угол
        normalized_angle = angle % (2 * math.pi)
        
        # Для дробных сторон мы интерполируем между двумя ближайшими целыми значениями
        if sides != int(sides):
            # Находим два ближайших целых значения
            floor_sides = int(math.floor(sides))
            ceil_sides = int(math.ceil(sides))
            fraction = sides - floor_sides  # дробная часть от 0 до 1
            
            # Если стороны меньше 2, но больше 1.5, работаем с 2 и 3 сторонами
            if floor_sides < 2:
                floor_sides = 2
                ceil_sides = 3
                fraction = max(0, sides - 2)  # нормализуем дробную часть
            
            # Вычисляем координаты для нижнего значения
            if floor_sides == 2:
                # Для 2 сторон - это просто линия
                x1, y1 = self._get_ngon_point(floor_sides, size, normalized_angle)
            else:
                x1, y1 = self._get_ngon_point(floor_sides, size, normalized_angle)
            
            # Вычисляем координаты для верхнего значения
            x2, y2 = self._get_ngon_point(ceil_sides, size, normalized_angle)
            
            # Линейная интерполяция
            return [
                x1 + fraction * (x2 - x1),
                y1 + fraction * (y2 - y1)
            ]
        else:
            # Целое число сторон
            return self._get_ngon_point(int(sides), size, normalized_angle)
    
    def _get_ngon_point(self, sides_int, size, angle):
        """Вспомогательный метод для вычисления точки правильного многоугольника"""
        if sides_int < 2:
            # Для 1 стороны или меньше возвращаем центр
            if sides_int < 1:
                return [0.0, 0.0]
            else:
                # Для "1 стороны" - это просто точка на окружности
                return [
                    size * math.cos(angle),
                    size * math.sin(angle)
                ]
        elif sides_int == 2:
            # Для 2 сторон - это линия (отрезок)
            # Преобразуем угол в параметр t от -1 до 1
            t = (angle / (2 * math.pi)) * 2 - 1
            return [size * t, 0.0]
        else:
            # Для 3 и более сторон - правильный многоугольник
            side_angle = 2 * math.pi / sides_int
            side = int(angle // side_angle) % sides_int
            t = (angle % side_angle) / side_angle
            
            angle1 = side * side_angle
            angle2 = ((side + 1) % sides_int) * side_angle
            
            x1 = size * math.cos(angle1)
            y1 = size * math.sin(angle1)
            x2 = size * math.cos(angle2)
            y2 = size * math.sin(angle2)
            
            return [
                x1 + t * (x2 - x1),
                y1 + t * (y2 - y1)
            ]

class FixedFunction(FunctionBase):
    """Фиксированная точка"""
    
    def evaluate(self, params, context):
        x = self._parse_param(params.get('x', 0), context)
        y = self._parse_param(params.get('y', 0), context)
        return [x, y]

class SumFunction(FunctionBase):
    """Сумма нескольких функций"""
    
    def evaluate(self, params, context):
        functions_config = params.get('functions', [])
        total_x, total_y = 0.0, 0.0
        
        for func_config in functions_config:
            func_name = func_config.get('func', 'circle')
            func = self.function_lib.get(func_name)
            x, y = func.evaluate(func_config, context)
            total_x += x
            total_y += y
        
        return [total_x, total_y]

class MultiplyFunction(FunctionBase):
    """Умножение функций"""
    
    def evaluate(self, params, context):
        functions_config = params.get('functions', [])
        operation = params.get('operation', 'elementwise')
        
        if not functions_config:
            return [0.0, 0.0]
        
        # Первая функция
        func_config = functions_config[0]
        func_name = func_config.get('func', 'circle')
        func = self.function_lib.get(func_name)
        result_x, result_y = func.evaluate(func_config, context)
        
        # Умножаем на остальные
        for func_config in functions_config[1:]:
            func_name = func_config.get('func', 'circle')
            func = self.function_lib.get(func_name)
            x, y = func.evaluate(func_config, context)
            
            if operation == 'elementwise':
                result_x *= x
                result_y *= y
            elif operation == 'scalar_x':
                result_x *= x
            elif operation == 'scalar_y':
                result_y *= y
        
        return [result_x, result_y]

class MorphFunction(FunctionBase):
    """Морфинг между функциями"""
    
    def evaluate(self, params, context):
        functions_config = params.get('functions', [])
        t = self._parse_param(params.get('t', 0), context)
        
        if not functions_config:
            return [0.0, 0.0]
        
        t = max(0.0, min(1.0, t))
        
        if len(functions_config) == 1:
            func_config = functions_config[0]
            func_name = func_config.get('func', 'circle')
            func = self.function_lib.get(func_name)
            return func.evaluate(func_config, context)
        
        segment = t * (len(functions_config) - 1)
        idx1 = int(segment)
        fraction = segment - idx1
        
        if idx1 >= len(functions_config) - 1:
            idx1 = len(functions_config) - 2
            fraction = 1.0
        
        func_config1 = functions_config[idx1]
        func_name1 = func_config1.get('func', 'circle')
        func1 = self.function_lib.get(func_name1)
        x1, y1 = func1.evaluate(func_config1, context)
        
        func_config2 = functions_config[idx1 + 1]
        func_name2 = func_config2.get('func', 'circle')
        func2 = self.function_lib.get(func_name2)
        x2, y2 = func2.evaluate(func_config2, context)
        
        return [
            x1 + fraction * (x2 - x1),
            y1 + fraction * (y2 - y1)
        ]

class DirectedLineFunction(FunctionBase):
    """Точка на линии между двумя функциями"""
    
    def evaluate(self, params, context):
        from_config = params.get('from', {'func': 'fixed', 'x': -50, 'y': 0})
        to_config = params.get('to', {'func': 'fixed', 'x': 50, 'y': 0})
        distance = self._parse_param(params.get('distance', 0), context)
        offset = self._parse_param(params.get('offset', 0), context)
        rotation = self._parse_param(params.get('rotation', 0), context)
        
        from_func = self.function_lib.get(from_config.get('func', 'fixed'))
        to_func = self.function_lib.get(to_config.get('func', 'fixed'))
        
        x1, y1 = from_func.evaluate(from_config, context)
        x2, y2 = to_func.evaluate(to_config, context)
        
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length < 0.0001:
            return [x1, y1]
        
        dir_x = dx / length
        dir_y = dy / length
        
        if rotation != 0:
            cos_r = math.cos(rotation)
            sin_r = math.sin(rotation)
            dir_x_rot = dir_x * cos_r - dir_y * sin_r
            dir_y_rot = dir_x * sin_r + dir_y * cos_r
            dir_x, dir_y = dir_x_rot, dir_y_rot
        
        point_x = x1 + dir_x * distance
        point_y = y1 + dir_y * distance
        
        if offset != 0:
            perp_x = -dir_y
            perp_y = dir_x
            point_x += perp_x * offset
            point_y += perp_y * offset
        
        return [point_x, point_y]

# ========== БИБЛИОТЕКА ФУНКЦИЙ ==========
class FunctionLibrary:
    """Реестр математических функций"""
    
    def __init__(self):
        self.functions = {}
        self._register_builtin_functions()
        self._register_advanced_functions()
    
    def _register_builtin_functions(self):
        """Регистрация встроенных функций"""
        # Создаем экземпляры
        circle = CircleFunction()
        square = SquareFunction()
        ngon = NGonFunction()
        fixed = FixedFunction()
        
        # Регистрируем простые
        self.register('circle', circle)
        self.register('square', square)
        self.register('ngon', ngon)
        self.register('fixed', fixed)
        
        # Создаем композитные с ссылкой на себя
        self.register('sum', SumFunction(self))
        self.register('multiply', MultiplyFunction(self))
        self.register('morph', MorphFunction(self))
        self.register('directed_line', DirectedLineFunction(self))
        
        print(f"✓ Registered built-in functions")
    
    def _register_advanced_functions(self):
        """Регистрация продвинутых функций"""
        try:
            from .advanced_functions import (
                EllipseFunction, SuperEllipseFunction, HypocycloidFunction,
                EpicycloidFunction, LissajousFunction, ButterflyFunction,
                CardioidFunction, RoseFunction
            )
            
            # Создаем и регистрируем продвинутые функции
            ellipse = EllipseFunction()
            superellipse = SuperEllipseFunction()
            hypocycloid = HypocycloidFunction()
            epicycloid = EpicycloidFunction()
            lissajous = LissajousFunction()
            butterfly = ButterflyFunction()
            cardioid = CardioidFunction()
            rose = RoseFunction()
            
            # Регистрируем
            self.register('ellipse', ellipse)
            self.register('superellipse', superellipse)
            self.register('hypocycloid', hypocycloid)
            self.register('epicycloid', epicycloid)
            self.register('lissajous', lissajous)
            self.register('butterfly', butterfly)
            self.register('cardioid', cardioid)
            self.register('rose', rose)
            
            # Альтернативные имена
            self.register('astroida', hypocycloid)
            self.register('roses', rose)
            self.register('lamé', superellipse)
            
            print(f"✓ Registered advanced functions")
            
        except ImportError as e:
            print(f"⚠ Advanced functions not available: {e}")
    
    def register(self, name: str, func: FunctionBase):
        """Регистрация функции"""
        self.functions[name] = func
        # Убедимся, что функция имеет ссылку на библиотеку
        func.function_lib = self
    
    def get(self, name: str) -> FunctionBase:
        """Получение функции по имени"""
        if name not in self.functions:
            print(f"⚠ Function '{name}' not found, using 'circle' as fallback")
            return self.functions.get('circle')
        return self.functions[name]
    
    def evaluate(self, function_name: str, params: Dict[str, Any], 
                context: Dict[str, Any]) -> List[float]:
        """Вычисляет функцию по имени"""
        func = self.get(function_name)
        try:
            return func.evaluate(params, context)
        except Exception as e:
            print(f"⚠ Error evaluating '{function_name}': {e}")
            return [0.0, 0.0]
    
    def list_functions(self):
        """Список всех доступных функций"""
        return sorted(list(self.functions.keys()))