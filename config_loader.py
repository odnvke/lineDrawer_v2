"""
Загрузчик конфигурации JSON
"""
import json
from typing import Dict, Any

class ConfigLoader:
    """Загрузка JSON файлов"""
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Загрузка JSON из файла"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded config from {filepath}")
                return data
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {}