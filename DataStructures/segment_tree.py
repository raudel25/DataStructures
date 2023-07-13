from typing import List
from .value import Value


class SegmentTree:
    def __init__(self, l: List[int | float | Value], prop: callable = lambda x, y, _: x + y):
        self.__values = l.copy()
        self.__p_values = [0]*(4*len(l))
        self.__prop = prop

        self.__build(1, 0, len(self.__values)-1)

    def set(self, index: int, value: int | float | Value):
        return self.__set(1, 0, len(self.__values) - 1, index, value)

    def query(self, l: int, r: int):
        return self.__query(1, 0, len(self.__values) - 1, l, r)

    @staticmethod
    def __left(p: int):
        return 2*p

    @staticmethod
    def __right(p: int):
        return 2*p+1

    def __build(self, p: int, l: int, r: int):

        if l == r:
            self.__p_values[p] = self.__values[l]
            return

        left, right = self.__left(p), self.__right(p)
        self.__build(left, l, (l+r)//2)
        self.__build(right, (l+r)//2 + 1, r)

        self.__p_values[p] = self.__prop(
            self.__p_values[left], self.__p_values[right], self.__values)

    def __set(self, p: int, l: int, r: int, index: int, value: int | float | Value):
        if l == r:
            self.__p_values[l] = self.__values[r]
            return

        left, right = self.__left(p), self.__right(p)

        if index <= (l+r)//2:
            self.__set(left, l, (l+r)//2, index, value)
        else:
            self.__set(right, (l+r)//2 + 1, r, index, value)

        self.__p_values[p] = self.__prop(
            self.__p_values[left], self.__p_values[right], self.__values)

    def __query(self, p: int, l: int, r: int, lq: int, rq: int) -> int | float | Value:
        if lq <= l and r <= rq:
            return self.__p_values[p]

        l1, r1 = l, (l+r)//2
        l2, r2 = (l+r)//2 + 1, r

        if l1 > rq or lq > r1:
            return self.__query(self.__right(p), l2, r2, lq, rq)
        if l2 > rq or lq > r2:
            return self.__query(self.__left(p), l1, r1, lq, rq)

        left, right = self.__query(self.__left(p), l1, r1, lq, rq), self.__query(
            self.__right(p), l2, r2, lq, rq)

        return self.__prop(left, right, self.__values)
