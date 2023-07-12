from typing import List
from .value import Value
import random


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
        while j != 0 and comp(l[j-1], l[j]):
            l[j-1], l[j] = l[j], l[j-1]
            j -= 1


def merge_sort(l: List[int] | List[float] | List[Value], asc=True):
    comp = comp_desc if asc else comp_asc
    sort(l, comp, 0, len(l)-1)


def sort(l: List[int] | List[float] | List[Value], comp, l1, r1):
    if l1 == r1:
        return

    sort(l, comp, l1, (l1+r1)//2)
    sort(l, comp, (l1+r1)//2+1, r1)
    merge(l, comp, l1, (l1+r1)//2, (l1+r1)//2+1, r1)


def merge(l: List[int] | List[float] | List[Value], comp, l1, r1, l2, r2):
    aux = l.copy()
    i, j = l1, l2
    x = min(l1, l2)

    while i <= r1 and j <= r2:
        if not comp(aux[i], aux[j]):
            l[x] = aux[i]
            i += 1
        else:
            l[x] = aux[j]
            j += 1

        x += 1

    while i <= r1:
        l[x] = aux[i]
        i += 1
        x += 1

    while j <= r2:
        l[x] = aux[j]
        j += 1
        x += 1


def quick_sort(l: List[int] | List[float] | List[Value], asc=True):
    comp = comp_desc if asc else comp_asc
    sort(l, comp, 0, len(l)-1)


def quick(l: List[int] | List[float] | List[Value], comp, l1, r1):
    if l1 > r1:
        return

    q = random.randint(l1, r1)
    aux = l.copy()

    i, j = l1, l1

    while i <= r1:
        if not comp(aux[i], aux[q]) and i != q:
            l[j] = aux[i]
            j += 1
        i += 1

    l[j] = aux[q]
    j += 1

    i = l1
    while i <= r1:
        if comp(aux[i], aux[q]) and i != q:
            l[j] = aux[i]
            j += 1
        i += 1

    quick(l, comp, l1, q-1)
    quick(l, comp, q+1, r1)
