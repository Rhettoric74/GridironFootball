from abc import ABC, abstractmethod

class GameSimulator(ABC):
    @abstractmethod
    def simulate_game(self, turn_time = 0, turtle = None):
        pass