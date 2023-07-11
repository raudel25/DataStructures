from DataStructures.disjoin_set import DisjoinSet

d= DisjoinSet(4)
d.join(0,1)
print(d.set_of(1))