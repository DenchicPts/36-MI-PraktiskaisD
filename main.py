import sys
import os

# Get the absolute path to the logica folder and add it to Python's search path.
base_path = os.path.dirname(os.path.abspath(__file__))
logica_path = os.path.join(base_path, 'logica')

sys.path.append(logica_path)

from logica.math import run_game

if __name__ == "__main__":
    run_game()

