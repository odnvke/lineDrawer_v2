"""
Паттерн connectToNext - соединение точек между соседними итерациями
Создает замкнутый цикл: последняя итерация соединяется с первой
"""
from typing import Dict, Any, List, Tuple
from .base_pattern import BasePattern

class ConnectToNextPattern(BasePattern):
    """
    Соединяет точки текущей итерации с соответствующими точками следующей итерации
    
    Особенность: создает линии от точки i в итерации n к точке i в итерации n+1
    Последняя итерация соединяется с первой (замыкание цикла)
    
    Отлично подходит для:
    - Анимации морфинга между фигурами
    - Показа траекторий движения точек
    - Визуализации путей
    - Создания туннелей и трубчатых структур
    """
    
    def create_lines(self) -> List:
        """
        Создает линии, соединяющие точки текущей итерации 
        с соответствующими точками следующей итерации
        Замыкает цикл: последняя итерация соединяется с первой
        """
        self.lines.clear()
        
        if not self.batch:
            return []
        
        points_config = self.config.get('points', [])
        count = self.config.get('count', 36)
        
        # Нужно минимум 2 итерации для соединения
        if count < 2:
            print("⚠ ConnectToNext requires at least 2 iterations (count >= 2)")
            return []
        
        if len(points_config) == 0:
            return []
        
        # Параметры стиля
        color_config = self.config.get('color', [255, 255, 255])
        color = self._parse_color(color_config)
        
        # Толщина линии
        self.config['line_width'] = float(self.config.get('width', 2.0))
        
        # Параметр для замыкания цикла (по умолчанию включен)
        close_loop = self.config.get('close_loop', True)
        
        # Соединяем точки между соседними итерациями
        for n in range(count):
            # Вычисляем точки для текущей итерации
            points_current = self._calculate_points_for_iteration(n)
            
            # Определяем следующую итерацию
            next_n = n + 1
            if close_loop and n == count - 1:  # Последняя итерация
                next_n = 0  # Замыкаем с первой
            elif next_n >= count:
                continue  # Пропускаем, если не замыкаем
            
            points_next = self._calculate_points_for_iteration(next_n)
            
            # Соединяем соответствующие точки
            for i in range(len(points_current)):
                # Проверяем, что в следующей итерации есть такая же точка
                if i < len(points_next):
                    x1, y1 = points_current[i]
                    x2, y2 = points_next[i]
                    
                    # Создаем линию (БЕЗ width параметра!)
                    line = self._create_line(x1, y1, x2, y2, color)
                    
                    # Сохраняем данные для анимации
                    context_current = self._create_context(n, current_time=0)
                    context_next = self._create_context(next_n, current_time=0)
                    
                    # Специальная структура данных для connectToNext
                    line.pattern_data = {
                        'point_config': points_config[i],  # Один конфиг для обеих точек
                        'n_current': n,
                        'n_next': next_n,
                        'point_index': i,
                        'context_base_current': context_current,
                        'context_base_next': context_next,
                        'close_loop': close_loop
                    }
                    
                    self.lines.append(line)
                else:
                    # Если конфигурация точек меняется между итерациями, пропускаем
                    break
        
        print(f"ConnectToNextPattern created {len(self.lines)} lines (close_loop={close_loop})")
        return self.lines
    
    def _update_single_line(self, line: pyglet.shapes.Line, current_time: float):
        """
        Переопределяем обновление для connectToNext паттерна
        Нужно учитывать две разные итерации
        """
        data = line.pattern_data
        
        # Обновляем время в контекстах
        context_current = data['context_base_current'].copy()
        context_current['time'] = current_time
        
        context_next = data['context_base_next'].copy()
        context_next['time'] = current_time
        
        # Вычисляем точку для текущей итерации
        x1, y1 = self._calculate_single_point(data['point_config'], context_current)
        
        # Вычисляем ту же точку для следующей итерации
        x2, y2 = self._calculate_single_point(data['point_config'], context_next)
        
        # Автоматический центр
        center = self.config.get('center', self.auto_center)
        center_x, center_y = center[0], center[1]
        
        # Обновляем координаты линии
        line.x = x1 + center_x
        line.y = y1 + center_y
        line.x2 = x2 + center_x
        line.y2 = y2 + center_y
    
    def _parse_color(self, color) -> Tuple[int, int, int]:
        """Парсит цвет в RGB кортеж"""
        if isinstance(color, list):
            if len(color) >= 3:
                return (color[0], color[1], color[2])
        elif isinstance(color, tuple):
            if len(color) >= 3:
                return color[:3]
        return (255, 255, 255)  # Белый по умолчанию