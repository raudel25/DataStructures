from typing import List
from .value import Value


def comp_desc(a: int | float | Value, b: int | float | Value) -> int | float | Value:
    return a > b


def comp_asc(a: int | float | Value, b: int | float | Value) -> int | float | Value:
    return a < b


def bugle_sort(l: List[int] | List[float] | List[Value], asc=True):
    comp = comp_desc if asc else comp_asc
    change = True

    while change:
        change = False

        for i in range(1, len(l)):
            if comp(l[i-1], l[i]):
                l[i-1], l[i] = l[i], l[i-1]
                change = True


def selection_sort(l: List[int] | List[float] | List[Value], asc=True):
    comp = comp_desc if asc else comp_asc

    for i in range(len(l)):
        ind = i
        for j in range(i+1, len(l)):
            if comp(l[ind], l[j]):
                ind = j
        l[i], l[ind] = l[ind], l[i]


def insertion_sort(l: List[int] | List[float] | List[Value], asc=True):
    comp = comp_desc if asc else comp_asc

    for i in range(len(l)):
        j = i
        while j != 0 and comp(l[j], l[j-1]):
            l[j-1], l[j] = l[j], l[j-1]
            j -= 1
