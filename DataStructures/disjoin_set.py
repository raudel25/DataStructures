class DisjoinSet:
    def __init__(self, n: int):
        self._pi = [x for x in range(n)]
        self._size = [1]*n
        self._cant_sets = n

    def set_of(self, index: int) -> int:
        if self._pi[index] == index:
            return index

        set_of = self.set_of(self._pi[index])
        self._pi[index] = set_of

        return set_of

    def same_set(self, index1: int, index2: int):
        return self.set_of(index1) == self.set_of(index2)

    def join(self, index1: int, index2: int):
        if self.set_of(index1) == self.set_of(index2):
            return

        if self._size[index1] < self._size[index2]:
            index1, index2 = index2, index1

        self._size[index1] += self._size[index2]
        self._pi[index2] = index1

        self._cant_sets -= 1

    @property
    def cant_sets(self) -> int:
        return self._cant_sets
