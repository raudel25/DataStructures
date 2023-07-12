from DataStructures.disjoin_set import DisjoinSet
from DataStructures.avl import Avl,Set
from DataStructures.sorted_algorithms import selection_sort, insertion_sort, merge_sort, quick_sort

# l = [3, 0, 5, -1, 0, 11, 12]
# quick_sort(l, False)
# print(l)

a = Set()

a.insert(2)
a.insert(3)
a.insert(6)
a.insert(7)
a.insert(5)
a.remove(3)

for i in a:
    print(i)
