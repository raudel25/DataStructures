from abc import ABC, abstractmethod
from .value import Value
from typing import List


class Property(ABC):
    def __init__(self):
        self._values = []

    def assign_values(self, values: List[int | float | Value]):
        self._values = values

    @abstractmethod
    def prop(self, x: int | float | Value, y: int | float | Value) -> int | float | Value:
        pass

    @abstractmethod
    def simple_node(self, index: int) -> int | float | Value:
        pass


class PropertySum(Property):
    def prop(self, x: int | float | Value, y: int | float | Value) -> int | float | Value:
        return x + y

    def simple_node(self, index: int) -> int | float | Value:
        return self._values[index]


class PropertyRmq(Property):
    def prop(self, x: int | float | Value, y: int | float | Value) -> int | float | Value:
        return x if self._values[x] <= self._values[y] else y

    def simple_node(self, index: int) -> int | float | Value:
        return index


class PropertyLazy(ABC):
    def __init__(self):
        self._values = []

    def assign_values(self, values: List[int | float | Value]):
        self._values = values

    @abstractmethod
    def prop_lazy(self, x: int | float | Value, y: int | float | Value) -> int | float | Value:
        pass

    @abstractmethod
    def prop_lazy_up(self, x: int | float | Value, y: int | float | Value, s: int) -> int | float | Value:
        pass


class PropertyLazySum(PropertyLazy):
    def prop_lazy(self, x: int | float | Value, y: int | float | Value) -> int | float | Value:
        return x + y

    def prop_lazy_up(self, x: int | float | Value, y: int | float | Value, s: int) -> int | float | Value:
        return x + y * s
