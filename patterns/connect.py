"""
Паттерн connect - соединение соседних точек
"""
from typing import Dict, Any, List, Tuple
from .base_pattern import BasePattern

class ConnectPattern(BasePattern):
    """Соединяет соседние точки линиями"""
    
    def create_lines(self) -> List:
        """Создает линии, соединяющие соседние точки"""
        self.lines.clear()
        
        if not self.batch:
            return []
        
        points_config = self.config.get('points', [])
        count = self.config.get('count', 36)
        
        if len(points_config) < 2:
            return []
        
        # Цвет линий из конфига или белый по умолчанию
        color_config = self.config.get('color', [255, 255, 255])
        color = self._parse_color(color_config)
        
        # Толщина линии
        self.config['line_width'] = float(self.config.get('width', 2.0))
        
        # Для каждой итерации
        for n in range(count):
            # Вычисляем ВСЕ точки для этой итерации
            points = self._calculate_points_for_iteration(n)
            
            # Соединяем соседние точки
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Создаем линию (БЕЗ width параметра!)
                line = self._create_line(x1, y1, x2, y2, color)
                
                # Сохраняем данные для анимации
                context = self._create_context(n, current_time=0)
                self._save_line_data(
                    line, 
                    points_config[i], 
                    points_config[i + 1], 
                    n, 
                    context
                )
                
                self.lines.append(line)
        
        print(f"ConnectPattern created {len(self.lines)} lines")
        return self.lines
    
    def _parse_color(self, color) -> Tuple[int, int, int]:
        """Парсит цвет в RGB кортеж"""
        if isinstance(color, list):
            if len(color) >= 3:
                return (color[0], color[1], color[2])
        elif isinstance(color, tuple):
            if len(color) >= 3:
                return color[:3]
        return (255, 255, 255)  # Белый по умолчанию