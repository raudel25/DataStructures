from abc import ABC, abstractclassmethod


class Element(ABC):
    def __add__(self, other):
        self.add(other)

    def __sub__(self, other):
        self.sub(other)

    def __lt__(self, other):
        return self.compare(other) == -1

    def __gt__(self, other):
        return self.compare(other) == 1

    def __le__(self, other):
        compare: int = self.compare(other)
        return compare == -1 or compare == 0

    def __ge__(self, other):
        compare: int = self.compare(other)
        return compare == 1 or compare == 0

    def __eq__(self, other):
        return self.compare(other) == 0

    @abstractclassmethod
    def add(self, _) -> int | float:
        pass

    @abstractclassmethod
    def sub(self, _) -> int | float:
        pass

    @abstractclassmethod
    def compare(self, _) -> int:
        pass
