from DataStructures.disjoin_set import DisjoinSet
from DataStructures.avl import Avl,Set,Dictionary
from DataStructures.sorted_algorithms import selection_sort, insertion_sort, merge_sort, quick_sort

# l = [3, 0, 5, -1, 0, 11, 12]
# quick_sort(l, False)
# print(l)

a = Set()
a.remove(100)
a.insert(2)
a.insert(3)
a.insert(6)
a.insert(7)
a.insert(8)
# a.remove(3)

a= Dictionary()

a.insert(3,2)
a.insert(5,1)
a.insert(122,2)
# a[3]=4
a[12]=2


for i in a:
    print(i)

print(a.select(1))
print(a.find(1))
