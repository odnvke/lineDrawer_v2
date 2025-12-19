"""
Основной класс приложения
"""
import pyglet
from pyglet.math import Mat4
from engine import ParametricEngine
from config_loader import ConfigLoader

class LineDrawerApp:
    """Основное окно приложения"""
    
    def __init__(self, config_file: str, width: int = 800, height: int = 600):
        self.config_file = config_file
        self.width = width
        self.height = height
        
        # Создаем движок
        self.engine = ParametricEngine(width, height)
        
        # Создаем окно
        config = pyglet.gl.Config(sample_buffers=1, samples=8)
        self.window = pyglet.window.Window(
            width, height, 
            "Parametric Line Drawer", 
            resizable=True,
            config=config
        )
        
        # Настройки OpenGL
        self.window.projection = Mat4.orthogonal_projection(0, width, 0, height, -1, 1)
        
        # События
        self.setup_events()
        
        # Загружаем конфигурацию
        self.load_config()
        
        # Таймер для обновления анимации
        pyglet.clock.schedule_interval(self.update, 1/60)
    
    def setup_events(self):
        """Настройка обработчиков событий"""
        
        @self.window.event
        def on_draw():
            self.window.clear()
            self.engine.draw()
        
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.R:
                self.load_config()
            elif symbol == pyglet.window.key.ESCAPE:
                self.window.close()
        
        @self.window.event
        def on_resize(width, height):
            self.width = width
            self.height = height
            self.window.projection = Mat4.orthogonal_projection(0, width, 0, height, -1, 1)
            self.engine.update_window_size(width, height)
    
    def load_config(self):
        """Загрузка конфигурации"""
        data = ConfigLoader.load_json(self.config_file)
        if data:
            self.engine.load_config(data)
    
    def update(self, dt):
        """Обновление анимации"""
        self.engine.update(dt)
    
    def run(self):
        """Запуск приложения"""
        print("="*50)
        print("Parametric Line Drawer")
        print("Controls: R - reload, ESC - exit")
        print("="*50)
        pyglet.app.run()