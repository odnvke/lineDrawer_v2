"""
Главный движок параметрического рисования
"""
import pyglet
import time
from typing import Dict, Any
from patterns import ConnectPattern, ConnectAllPattern, ConnectToNextPattern
from functions import FunctionLibrary

class ParametricEngine:
    """Управляет всей параметрической графикой"""
    
# В методе __init__ класса ParametricEngine добавляем:
from patterns import ConnectClosedPattern

class ParametricEngine:
    """Управляет всей параметрической графикой"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Библиотека функций
        self.function_lib = FunctionLibrary()
        
        # Паттерны с передачей размеров окна
        self.patterns = {
            'connect': ConnectPattern(self.function_lib, width, height),
            'connectAll': ConnectAllPattern(self.function_lib, width, height),
            'connectToNext': ConnectToNextPattern(self.function_lib, width, height),
            'connectClosed': ConnectClosedPattern(self.function_lib, width, height)
        }
        
        # Состояние
        self.current_pattern = None
        self.lines_batch = pyglet.graphics.Batch()
        self.start_time = time.time()
        self.config = {}
    
    def update_window_size(self, width: int, height: int):
        """Обновление при изменении размера окна"""
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Обновляем все паттерны
        for pattern in self.patterns.values():
            pattern.update_window_size(width, height)
        
        # Пересоздаем линии с новым центром
        if self.config:
            self._create_lines(self.config)
    
    def load_config(self, data: Dict[str, Any]):
        """Загрузка конфигурации из JSON"""
        self.config = data.get('parametric_lines', {})
        self._create_lines(self.config)
    
    def _create_lines(self, config: Dict[str, Any]):
        """Создание линий по конфигурации"""
        # Получаем имя паттерна
        pattern_name = config.get('pattern', 'connect')
        
        # Получаем паттерн
        if pattern_name not in self.patterns:
            print(f"Pattern '{pattern_name}' not found. Available: {list(self.patterns.keys())}")
            pattern_name = 'connect'  # Fallback
        
        pattern = self.patterns[pattern_name]
        self.current_pattern = pattern
        
        # Настраиваем паттерн
        pattern.set_config(config)
        pattern.set_batch(self.lines_batch)
        
        # Создаем линии
        pattern.create_lines()
        print(f"Pattern '{pattern_name}' created {pattern.get_line_count()} lines")  # ← Теперь работает!
    
    def update(self, dt: float):
        """Обновление анимации"""
        if not self.current_pattern:
            return
        
        current_time = time.time() - self.start_time
        self.current_pattern.update_lines(current_time)
    
    def draw(self):
        """Отрисовка всех линий"""
        if self.current_pattern:
            self.current_pattern.draw()