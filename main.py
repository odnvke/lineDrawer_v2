#!/usr/bin/env python3
"""
Главный файл приложения
"""

from core import LineDrawerApp

def main():
    # Создаем приложение
    app = LineDrawerApp("example_parametric.json", width=1024, height=768)
    
    # Запускаем
    app.run()

if __name__ == "__main__":
    main()