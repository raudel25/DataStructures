from typing import List
from .value import Value


class SegmentTree:
    def __init__(self, l: List[int | float | Value], prop: callable = lambda x, y, _: x + y):
        self._values = l.copy()
        self._p_values = [0]*(4*len(l))
        self._prop = prop

        self._build(1, 0, len(self._values)-1)

    def set(self, index: int, value: int | float | Value):
        return self._set(1, 0, len(self._values) - 1, index, value)

    def query(self, l: int, r: int):
        return self._query(1, 0, len(self._values) - 1, l, r)

    @staticmethod
    def _left(p: int):
        return 2*p

    @staticmethod
    def _right(p: int):
        return 2*p+1

    def _build(self, p: int, l: int, r: int):

        if l == r:
            self._p_values[p] = self._values[l]
            return

        left, right = self._left(p), self._right(p)
        self._build(left, l, (l+r)//2)
        self._build(right, (l+r)//2 + 1, r)

        self._p_values[p] = self._prop(
            self._p_values[left], self._p_values[right], self._values)

    def _set(self, p: int, l: int, r: int, index: int, value: int | float | Value):
        if l == r:
            self._values[l] = value
            self._p_values[p] = self._values[l]
            return

        left, right = self._left(p), self._right(p)

        if index <= (l+r)//2:
            self._set(left, l, (l+r)//2, index, value)
        else:
            self._set(right, (l+r)//2 + 1, r, index, value)

        self._p_values[p] = self._prop(
            self._p_values[left], self._p_values[right], self._values)

    def _query(self, p: int, l: int, r: int, lq: int, rq: int) -> int | float | Value:
        if lq <= l and r <= rq:
            return self._p_values[p]

        l1, r1 = l, (l+r)//2
        l2, r2 = (l+r)//2 + 1, r

        if l1 > rq or lq > r1:
            return self._query(self._right(p), l2, r2, lq, rq)
        if l2 > rq or lq > r2:
            return self._query(self._left(p), l1, r1, lq, rq)

        left, right = self._query(self._left(p), l1, r1, lq, rq), self._query(
            self._right(p), l2, r2, lq, rq)

        return self._prop(left, right, self._values)


class SegmentTreeLazy(SegmentTree):
    def __init__(self, l: List[int | float | Value], prop: callable = lambda x, y, _: x + y, prop_lazy: callable = lambda x, y: x+y, prop_lazy_up: callable = lambda x, y, s, _: y + x*s):
        super().__init__(l, prop)

        self._prop_lazy_up = prop_lazy_up
        self._prop_lazy = prop_lazy
        self._lazy = [False]*(4*len(l))
        self._l_values = [0]*(4*len(l))

    def set_rank(self, l: int, r: int, value: int | float | Value):
        return self._set_rank(1, 0, len(self._values) - 1, l, r, value)

    def _update_lazy(self, p: int, l: int, r: int, value: int | float | Value):
        # print(self._l_values[p], self._p_values[p])
        self._p_values[p] = self._prop_lazy_up(
            value, self._p_values[p], r - l + 1, self._values)

    def _propagate_lazy(self, p: int, l: int, r: int):
        self._lazy[p] = False

        if l == r:
            return

        left, right = self._left(p), self._right(p)

        self._l_values[left] = self._prop_lazy(
            self._l_values[left], self._l_values[p]) if self._lazy[left] else self._l_values[p]
        self._l_values[right] = self._prop_lazy(
            self._l_values[right], self._l_values[p]) if self._lazy[right] else self._l_values[p]

        self._lazy[left] = True
        self._lazy[right] = True

        self._update_lazy(left, l, (l + r)//2, self._l_values[p])
        self._update_lazy(right, (l + r)//2 + 1, r, self._l_values[p])

    def _set(self, p: int, l: int, r: int, index: int, value: int | float | Value):
        if self._lazy[p]:
            self._propagate_lazy(p, l, r)

        if l == r:
            self._values[l] = value
            self._p_values[p] = self._values[l]
            return

        left, right = self._left(p), self._right(p)

        if index <= (l+r)//2:
            self._set(left, l, (l+r)//2, index, value)
        else:
            self._set(right, (l+r)//2 + 1, r, index, value)

        self._p_values[p] = self._prop(
            self._p_values[left], self._p_values[right], self._values)

    def _query(self, p: int, l: int, r: int, lq: int, rq: int) -> int | float | Value:
        if self._lazy[p]:
            self._propagate_lazy(p, l, r)

        if lq <= l and r <= rq:
            return self._p_values[p]

        l1, r1 = l, (l+r)//2
        l2, r2 = (l+r)//2 + 1, r

        if l1 > rq or lq > r1:
            return self._query(self._right(p), l2, r2, lq, rq)
        if l2 > rq or lq > r2:
            return self._query(self._left(p), l1, r1, lq, rq)

        left, right = self._query(self._left(p), l1, r1, lq, rq), self._query(
            self._right(p), l2, r2, lq, rq)

        return self._prop(left, right, self._values)

    def _set_rank(self, p: int, l: int, r: int, lq: int, rq: int, value: int | float | Value) -> int | float | Value:
        if self._lazy[p]:
            self._propagate_lazy(p, l, r)

        if l > rq or lq > r:
            return

        if lq <= l and r <= rq:
            self._lazy[p] = True
            self._l_values[p] = value
            self._update_lazy(p, l, r, value)
            return

        left, right = self._left(p), self._right(p)

        self._set_rank(left, l, (l+r)//2, lq, rq, value)
        self._set_rank(right, (l+r)//2+1, r, lq, rq, value)

        self._p_values[p] = self._prop(
            self._p_values[left], self._p_values[right], self._values)
