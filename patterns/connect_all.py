"""
Паттерн connect_all - соединяет КАЖДУЮ точку с КАЖДОЙ
"""
from typing import Dict, Any, List, Tuple
from .base_pattern import BasePattern

class ConnectAllPattern(BasePattern):
    """Соединяет каждую точку со всеми остальными (полный граф)"""
    
    def create_lines(self) -> List:
        """
        Создает линии, соединяющие КАЖДУЮ точку с КАЖДОЙ
        Для N точек создает N*(N-1)/2 линий
        """
        self.lines.clear()
        
        if not self.batch:
            return []
        
        points_config = self.config.get('points', [])
        count = self.config.get('count', 12)  # Меньше чем у connect, т.к. линий много
        
        if len(points_config) < 2:
            return []
        
        # Параметры стиля
        color_config = self.config.get('color', [255, 255, 255])
        color = self._parse_color(color_config)
        
        # Толщина линии (хранится в config для draw())
        self.config['line_width'] = float(self.config.get('width', 0.5))
        
        # Оптимизация: предупреждение при большом количестве линий
        total_lines = count * len(points_config) * (len(points_config) - 1) // 2
        if total_lines > 1000:
            print(f"Warning: ConnectAll will create {total_lines} lines (may affect performance)")
        
        # Для каждой итерации
        for n in range(count):
            # Вычисляем ВСЕ точки для этой итерации
            points = self._calculate_points_for_iteration(n)
            
            # СОЕДИНЯЕМ КАЖДУЮ ТОЧКУ С КАЖДОЙ
            for i in range(len(points)):
                for j in range(i + 1, len(points)):  # Только уникальные пары
                    x1, y1 = points[i]
                    x2, y2 = points[j]
                    
                    # Создаем линию (БЕЗ width параметра!)
                    line = self._create_line(x1, y1, x2, y2, color)
                    
                    # Сохраняем данные для анимации
                    context = self._create_context(n, current_time=0)
                    self._save_line_data(
                        line, 
                        points_config[i], 
                        points_config[j], 
                        n, 
                        context
                    )
                    
                    self.lines.append(line)
        
        print(f"ConnectAllPattern created {len(self.lines)} lines")
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