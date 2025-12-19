"""
advanced_functions.py - Продвинутые математические функции
"""
import math
from typing import Dict, Any, List

# Определяем базовый класс здесь, чтобы избежать импорта
class FunctionBaseAdvanced:
    """База для всех продвинутых математических функций"""
    
    def __init__(self, function_lib=None):
        self.function_lib = function_lib
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any]) -> List[float]:
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
            'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt,
            'abs': abs, 'pow': math.pow, 'exp': math.exp,
            'log': math.log, 'log10': math.log10,
            'floor': math.floor, 'ceil': math.ceil, 'round': round,
            **context
        }
        try:
            return float(eval(expr, {"__builtins__": {}}, safe_dict))
        except:
            return 0.0

# ========== 2. ЭЛЛИПС ==========
class EllipseFunction(FunctionBaseAdvanced):
    """Эллипс"""
    
    def evaluate(self, params, context):
        a = self._parse_param(params.get('a', 100), context)
        b = self._parse_param(params.get('b', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        return [
            a * math.cos(angle),
            b * math.sin(angle)
        ]

# ========== 3. СУПЕРЭЛЛИПС (КРИВАЯ ЛАМЕ) ==========
class SuperEllipseFunction(FunctionBaseAdvanced):
    """Суперэллипс (кривая Ламе)"""
    
    def evaluate(self, params, context):
        a = self._parse_param(params.get('a', 100), context)
        b = self._parse_param(params.get('b', 100), context)
        n = self._parse_param(params.get('n', 2), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        if abs(n) < 0.001:
            n = 0.001
        
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        if n >= 2:
            if abs(cos_a) < 0.001:
                x = 0.0
                y = b * (1 if sin_a >= 0 else -1)
            elif abs(sin_a) < 0.001:
                x = a * (1 if cos_a >= 0 else -1)
                y = 0.0
            else:
                denom = (abs(cos_a/a)**n + abs(sin_a/b)**n)
                if denom > 0:
                    r = 1.0 / (denom ** (1.0/n))
                    x = r * math.copysign(abs(cos_a), cos_a)
                    y = r * math.copysign(abs(sin_a), sin_a)
                else:
                    x = 0.0
                    y = 0.0
        else:
            sign_cos = 1 if cos_a >= 0 else -1
            sign_sin = 1 if sin_a >= 0 else -1
            x = a * sign_cos * (abs(math.cos(angle)) ** (2.0/n))
            y = b * sign_sin * (abs(math.sin(angle)) ** (2.0/n))
        
        return [x, y]

# ========== 4. ГИПОЦИКЛОИДА ==========
class HypocycloidFunction(FunctionBaseAdvanced):
    """Гипоциклоида (астроида)"""
    
    def evaluate(self, params, context):
        R = self._parse_param(params.get('R', 100), context)
        r = self._parse_param(params.get('r', 25), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        if abs(r) > 0.001:
            ratio = (R - r) / r
            x = (R - r) * math.cos(t) + r * math.cos(ratio * t)
            y = (R - r) * math.sin(t) - r * math.sin(ratio * t)
        else:
            x = R * math.cos(t)
            y = R * math.sin(t)
        
        return [x, y]

# ========== 5. ЭПИЦИКЛОИДА ==========
class EpicycloidFunction(FunctionBaseAdvanced):
    """Эпициклоида"""
    
    def evaluate(self, params, context):
        R = self._parse_param(params.get('R', 100), context)
        r = self._parse_param(params.get('r', 30), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        if abs(r) > 0.001:
            ratio = (R + r) / r
            x = (R + r) * math.cos(t) - r * math.cos(ratio * t)
            y = (R + r) * math.sin(t) - r * math.sin(ratio * t)
        else:
            x = R * math.cos(t)
            y = R * math.sin(t)
        
        return [x, y]

# ========== 6. ЛИССАЖУ ==========
class LissajousFunction(FunctionBaseAdvanced):
    """Кривые Лиссажу"""
    
    def evaluate(self, params, context):
        a = self._parse_param(params.get('a', 200), context)
        b = self._parse_param(params.get('b', 150), context)
        A = self._parse_param(params.get('A', 3), context)
        B = self._parse_param(params.get('B', 2), context)
        delta = self._parse_param(params.get('delta', 0), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        x = a * math.sin(A * t + delta)
        y = b * math.sin(B * t)
        
        return [x, y]

# ========== 7. БАБОЧКА ==========
class ButterflyFunction(FunctionBaseAdvanced):
    """Butterfly curve"""
    
    def evaluate(self, params, context):
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        r = math.exp(math.cos(t)) - 2 * math.cos(4 * t) + math.sin(t/12)**5
        
        x = size * r * math.cos(t)
        y = size * r * math.sin(t)
        
        return [x, y]

# ========== 8. КАРДИОИДА ==========
class CardioidFunction(FunctionBaseAdvanced):
    """Кардиоида"""
    
    def evaluate(self, params, context):
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        r = size * (1 - math.cos(t))
        
        x = r * math.cos(t)
        y = r * math.sin(t)
        
        return [x, y]

# ========== 9. РОЗЫ (ROSE CURVES) ==========
class RoseFunction(FunctionBaseAdvanced):
    """Розы (Rose curves)"""
    
    def evaluate(self, params, context):
        k = self._parse_param(params.get('k', 2), context)
        size = self._parse_param(params.get('size', 100), context)
        angle = self._parse_param(params.get('angle', 0), context)
        
        t = angle
        if abs(k) < 0.001:
            r = 0.0
        else:
            r = size * math.cos(k * t)
        
        x = r * math.cos(t)
        y = r * math.sin(t)
        
        return [x, y]

def register_advanced_functions(library):
    """Регистрация всех продвинутых функций"""
    
    # Создаем экземпляры
    functions = {
        'ellipse': EllipseFunction(),
        'superellipse': SuperEllipseFunction(),
        'hypocycloid': HypocycloidFunction(),
        'epicycloid': EpicycloidFunction(),
        'lissajous': LissajousFunction(),
        'butterfly': ButterflyFunction(),
        'cardioid': CardioidFunction(),
        'rose': RoseFunction(),
    }
    
    # Регистрируем
    for name, func in functions.items():
        library.register(name, func)
        func.function_lib = library
    
    print(f"✓ Registered {len(functions)} advanced functions")
    return functions