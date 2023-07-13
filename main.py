from DataStructures.disjoin_set import DisjoinSet
from DataStructures.avl import Avl,Set,Dictionary,MultiSet
from DataStructures.sorted_algorithms import selection_sort, insertion_sort, merge_sort, quick_sort
from DataStructures.segment_tree import SegmentTreeLazy,SegmentTree

s=SegmentTreeLazy([1,2,3,4,5])
s.set(3,0)
s.set(4,0)
# s.set_rank(0,1,1)
s.set_rank(0,2,3)
# s.set(1,2)
print(s.query(1,4))