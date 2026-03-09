import sys
import os

# Получаем абсолютный путь к папке logica
base_path = os.path.dirname(os.path.abspath(__file__))
logica_path = os.path.join(base_path, 'logica')

# Добавляем её в пути поиска Python
sys.path.append(logica_path)

from logica.math import run_game

if __name__ == "__main__":
    run_game()

