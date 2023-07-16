from DataStructures.disjoin_set import DisjoinSet
from DataStructures.avl import Avl, Set, Dictionary, MultiSet
from DataStructures.sorted_algorithms import selection_sort, insertion_sort, merge_sort, quick_sort
from DataStructures.segment_tree import SegmentTreeLazy, SegmentTree
from DataStructures.sparse_table import SparseTable


s=SparseTable([1,-2,3,4])

# s.set_rank(0,1,4)

print(s.query(2,3))

