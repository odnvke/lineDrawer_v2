"""
Паттерн connectClosed - соединение точек с замыканием контура
Соединяет все точки последовательно и замыкает контур, соединяя последнюю точку с первой
"""
from typing import Dict, Any, List, Tuple
from .base_pattern import BasePattern

class ConnectClosedPattern(BasePattern):
    """
    Соединяет точки последовательно с замыканием контура
    
    Особенность: создает замкнутый контур (полигон), соединяя:
    1. Точку 0 с точкой 1
    2. Точку 1 с точкой 2
    ...
    N. Точку N-1 с точкой 0 (замыкание)
    
    Идеально для:
    - Создания замкнутых фигур и полигонов
    - Отрисовки контуров
    - Геометрических фигур с замыканием
    """
    
    def create_lines(self) -> List:
        """
        Создает линии, соединяющие все точки в замкнутый контур
        """
        self.lines.clear()
        
        if not self.batch:
            return []
        
        points_config = self.config.get('points', [])
        count = self.config.get('count', 36)
        
        if len(points_config) < 2:
            print("⚠ ConnectClosed requires at least 2 points")
            return []
        
        # Параметры стиля
        color_config = self.config.get('color', [255, 255, 255])
        color = self._parse_color(color_config)
        
        # Толщина линии
        self.config['line_width'] = float(self.config.get('width', 2.0))
        
        # Параметр для заполнения (будущая функция)
        fill = self.config.get('fill', False)
        
        # Для каждой итерации
        for n in range(count):
            # Вычисляем ВСЕ точки для этой итерации
            points = self._calculate_points_for_iteration(n)
            
            # Соединяем точки последовательно
            for i in range(len(points)):
                x1, y1 = points[i]
                
                # Определяем следующую точку
                if i == len(points) - 1:
                    # Замыкаем контур: последняя точка -> первая точка
                    x2, y2 = points[0]
                    point2_index = 0
                else:
                    # Обычное соединение: текущая точка -> следующая точка
                    x2, y2 = points[i + 1]
                    point2_index = i + 1
                
                # Создаем линию (БЕЗ width параметра!)
                line = self._create_line(x1, y1, x2, y2, color)
                
                # Сохраняем данные для анимации
                context = self._create_context(n, current_time=0)
                
                # Для замкнутого контура
                self._save_line_data_closed(
                    line, 
                    points_config[i], 
                    points_config[point2_index], 
                    n, 
                    context,
                    is_closing=(i == len(points) - 1)  # Флаг замыкания
                )
                
                self.lines.append(line)
        
        print(f"ConnectClosedPattern created {len(self.lines)} lines (closed contour)")
        return self.lines
    
    def _save_line_data_closed(self, line: pyglet.shapes.Line, 
                              point1_config: Dict[str, Any],
                              point2_config: Dict[str, Any],
                              n: int, 
                              context: Dict[str, Any],
                              is_closing: bool = False):
        """
        Сохраняет данные для анимации линии в замкнутом контуре
        """
        line.pattern_data = {
            'point1_config': point1_config,
            'point2_config': point2_config,
            'n': n,
            'context_base': context.copy(),
            'is_closing': is_closing  # Флаг линии замыкания
        }
    
    def _parse_color(self, color) -> Tuple[int, int, int]:
        """Парсит цвет в RGB кортеж"""
        if isinstance(color, list):
            if len(color) >= 3:
                return (color[0], color[1], color[2])
        elif isinstance(color, tuple):
            if len(color) >= 3:
                return color[:3]
        return (255, 255, 255)  # Белый по умолчанию