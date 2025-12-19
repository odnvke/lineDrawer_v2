"""
Базовый класс для ВСЕХ паттернов
"""
import math
import pyglet
from typing import Dict, Any, List, Tuple

class BasePattern:
    """Базовый класс с общей логикой для всех паттернов"""
    
    def __init__(self, function_lib, window_width: int = 800, window_height: int = 600):
        self.function_lib = function_lib
        self.config = {}
        self.batch = None
        self.lines = []
        self.window_width = window_width
        self.window_height = window_height
        self.auto_center = [window_width // 2, window_height // 2]
    
    def set_config(self, config: Dict[str, Any]):
        """Установка конфигурации (общая для всех)"""
        self.config = config
        
        # Автоматически устанавливаем центр, если не задан
        if 'center' not in self.config:
            self.config['center'] = self.auto_center.copy()
            print(f"Auto-center: {self.config['center']}")
    
    def update_window_size(self, width: int, height: int):
        """Обновление размера окна"""
        self.window_width = width
        self.window_height = height
        self.auto_center = [width // 2, height // 2]
    
    def set_batch(self, batch: pyglet.graphics.Batch):
        """Установка batch для рисования"""
        self.batch = batch
    
    def create_lines(self) -> List:
        """Создание линий - АБСТРАКТНЫЙ метод"""
        raise NotImplementedError("Паттерн должен реализовать create_lines()")
    
    # ========== ОБЩИЕ МЕТОДЫ (DRY) ==========
    
    def _calculate_points_for_iteration(self, n: int, current_time: float = 0) -> List[Tuple[float, float]]:
        """
        Вычисляет ВСЕ точки для итерации n
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        points_config = self.config.get('points', [])
        if not points_config:
            return []
        
        # Параметры из конфига
        count = self.config.get('count', 36)
        
        # Автоматический центр (если не задан явно)
        center = self.config.get('center', self.auto_center)
        center_x, center_y = center[0], center[1]
        
        # Создаем контекст для выражений
        context = self._create_context(n, current_time)
        
        # Вычисляем каждую точку
        points = []
        for point_config in points_config:
            x, y = self._calculate_single_point(point_config, context)
            points.append((x + center_x, y + center_y))
        
        return points
    
    def _calculate_single_point(self, point_config: Dict[str, Any], 
                               context: Dict[str, Any]) -> Tuple[float, float]:
        """
        Вычисляет одну точку по конфигурации
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        func_name = point_config.get('func', 'circle')
        
        try:
            # Используем библиотеку функций
            coords = self.function_lib.evaluate(func_name, point_config, context)
            if len(coords) >= 2:
                return coords[0], coords[1]
        except Exception as e:
            print(f"Error calculating point: {e}")
        
        return 0.0, 0.0
    
    def _create_context(self, n: int, current_time: float) -> Dict[str, Any]:
        """
        Создает контекст для выражений
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        count = self.config.get('count', 36)
        angle_step = 2 * math.pi / count if count > 0 else 0
        
        return {
            'n': n,
            'time': current_time,
            'count': count,
            'angle_step': angle_step,
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau
        }
    
    def _create_line(self, x1: float, y1: float, x2: float, y2: float,
                    color: Tuple[int, int, int] = (255, 255, 255)) -> pyglet.shapes.Line:
        """
        Создает линию
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        if not self.batch:
            self.batch = pyglet.graphics.Batch()
        
        # Создаем линию (pyglet.shapes.Line не принимает width)
        line = pyglet.shapes.Line(
            x1, y1, x2, y2,
            color=color,
            batch=self.batch
        )
        
        return line
    
    def _save_line_data(self, line: pyglet.shapes.Line, 
                       point1_config: Dict[str, Any],
                       point2_config: Dict[str, Any],
                       n: int, context: Dict[str, Any]):
        """
        Сохраняет данные для анимации линии
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        line.pattern_data = {
            'point1_config': point1_config,
            'point2_config': point2_config,
            'n': n,
            'context_base': context.copy()
        }
    
    def update_lines(self, current_time: float):
        """
        Обновляет ВСЕ линии для анимации
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        for line in self.lines:
            if hasattr(line, 'pattern_data'):
                self._update_single_line(line, current_time)
    
    def _update_single_line(self, line: pyglet.shapes.Line, current_time: float):
        """
        Обновляет одну линию
        ОБЩАЯ ЛОГИКА для всех паттернов
        """
        data = line.pattern_data
        
        # Обновляем время в контексте
        context = data['context_base'].copy()
        context['time'] = current_time
        
        # Вычисляем первую точку
        x1, y1 = self._calculate_single_point(data['point1_config'], context)
        
        # Вычисляем вторую точку
        x2, y2 = self._calculate_single_point(data['point2_config'], context)
        
        # Автоматический центр (если не задан явно)
        center = self.config.get('center', self.auto_center)
        center_x, center_y = center[0], center[1]
        
        # Обновляем координаты линии
        line.x = x1 + center_x
        line.y = y1 + center_y
        line.x2 = x2 + center_x
        line.y2 = y2 + center_y
    
    def clear_lines(self):
        """Очищает все линии"""
        self.lines.clear()
        if self.batch:
            self.batch = None
    
    def draw(self):
        """Рисует все линии"""
        if self.batch and self.lines:
            # Устанавливаем толщину линии
            line_width = float(self.config.get('line_width', 1.0))
            pyglet.gl.glLineWidth(line_width)
            
            # Рисуем
            self.batch.draw()
            
            # Возвращаем толщину к значению по умолчанию
            pyglet.gl.glLineWidth(1.0)
    
    def get_line_count(self) -> int:
        """Возвращает количество линий в паттерне"""
        return len(self.lines)