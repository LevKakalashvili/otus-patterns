from abc import ABC, abstractmethod


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


class IMovable(ABC):
    @abstractmethod
    def get_position(self) -> Vector:
        pass

    @abstractmethod
    def set_position(self, new_value: Vector):
        pass

    @abstractmethod
    def get_velocity(self) -> Vector:
        pass

    @abstractmethod
    def finish(self):
        pass
