from DataStructures.disjoin_set import DisjoinSet
from DataStructures.avl import Avl,Set,Dictionary,MultiSet
from DataStructures.sorted_algorithms import selection_sort, insertion_sort, merge_sort, quick_sort
from DataStructures.segment_tree import SegmentTree

s=SegmentTree([1,2,3,4,5])

print(s.query(2,4))