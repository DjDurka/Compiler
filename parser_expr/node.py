from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def print(self, p=1):
        pass