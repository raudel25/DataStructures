from .value import Value
from typing import Tuple, Iterable


class Bst:
    def __init__(self, k: int | float | Value, v=None):
        self.key: int | float | Value = k
        self.value = v
        self.size: int = 1
        self.h = 1
        self.left: Bst = None
        self.right: Bst = None

    def pre_orden(self) -> Iterable['Bst']:
        yield self

        if self.left is not None:
            for i in self.left.pre_orden():
                yield i

        for i in self.right.pre_orden():
            yield i

    def in_orden(self) -> Iterable['Bst']:
        if self.left is not None:
            for i in self.left.in_orden():
                yield i

        yield self

        if self.right is not None:
            for i in self.right.in_orden():
                yield i

    def post_orden(self) -> Iterable['Bst']:
        if self.left is not None:
            for i in self.left.post_orden():
                yield i

        if self.right is not None:
            for i in self.right.post_orden():
                yield i

        yield self

    def find(self, k: int | float | Value) -> 'Bst':
        if self.key == k:
            return self

        if k < self.key:
            return None if self.left is None else self.left.find(k)

        return None if self.right is None else self.right.find(k)

    def update(self, k: int | float | Value):
        if self.key == k:
            return

        if k < self.key and self.left is not None:
            self.left.update(k)

        if k > self.key and self.right is not None:
            self.right.update(k)

        self.act_h()
        self.act_size()

    def rank(self, k: int | float | Value) -> int:
        left = 0 if self.left is None else self.left.size

        if k == self.key:
            return left

        if k < self.key:
            return 0 if self.left is None else self.left.rank(k)

        return left + 1 if self.right is None else left + 1 + self.right.rank(k)

    def select(self, index: int) -> 'Bst':
        if index < 0 or index >= self.size:
            return None

        left = 0 if self.left is None else self.left.size

        if index == left:
            return self

        if index < left:
            return None if self.left is None else self.left.select(index)

        return None if self.right is None else self.right.select(index - left - 1)

    def act_h(self):
        hl: int = 0 if self.left is None else self.left.h
        hr: int = 0 if self.right is None else self.right.h

        self.h = max(hl, hr) + 1

    def act_size(self):
        sl: int = 0 if self.left is None else self.left.size
        sr: int = 0 if self.right is None else self.right.size

        self.size = sl + sr + 1


class MultiBst(Bst):
    def __init__(self, k: int | float | Value, v=None):
        super().__init__(k, v)

    def pre_orden(self) -> Iterable['MultiBst']:
        for _ in range(self.value):
            yield self

        if self.left is not None:
            for i in self.left.pre_orden():
                yield i

        for i in self.right.pre_orden():
            yield i

    def in_orden(self) -> Iterable['MultiBst']:
        if self.left is not None:
            for i in self.left.in_orden():
                yield i

        for _ in range(self.value):
            yield self

        if self.right is not None:
            for i in self.right.in_orden():
                yield i

    def post_orden(self) -> Iterable['MultiBst']:
        if self.left is not None:
            for i in self.left.post_orden():
                yield i

        if self.right is not None:
            for i in self.right.post_orden():
                yield i

        for _ in range(self.value):
            yield self

    def rank(self, k: int | float | Value) -> int:
        left = 0 if self.left is None else self.left.size

        if k == self.key:
            return left

        if k < self.key:
            return 0 if self.left is None else self.left.rank(k)

        return left + self.value if self.right is None else left + self.value + self.right.rank(k)

    def select(self, index: int) -> 'MultiBst':
        if index < 0 or index >= self.size:
            return None

        left = 0 if self.left is None else self.left.size

        if left <= index and index < left + self.value:
            return self

        if index < left:
            return None if self.left is None else self.left.select(index)

        return None if self.right is None else self.right.select(index - left - self.value)

    def act_size(self):
        sl: int = 0 if self.left is None else self.left.size
        sr: int = 0 if self.right is None else self.right.size

        self.size = sl + sr + self.value


class Avl:
    def __init__(self, init: callable = Bst):
        self.root: Bst = None
        self.init = init

    def pre_orden(self) -> Iterable[Bst]:
        if self.root is None:
            return []
        return self.root.pre_orden()

    def in_orden(self) -> Iterable[Bst]:
        if self.root is None:
            return []
        return self.root.in_orden()

    def post_orden(self) -> Iterable[Bst]:
        if self.root is None:
            return []
        return self.root.post_orden()

    def find(self, k: int | float | Value) -> Bst:
        if self.root is None:
            return None
        return self.root.find(k)

    def update(self, k: int | float | Value):
        if self.root is None:
            return
        self.root.update(k)

    def rank(self, k: int | float | Value) -> int:
        return self.root.rank(k)

    def select(self, index: int) -> Bst | None:
        if self.root is None:
            return None
        return self.root.select(index)

    def insert(self, k: int | float | Value, v=None):
        if self.root is None:
            self.root = Bst(k, v)
            return

        self.__insert(self.root, k, v)
        self.__valance__root()

    def remove(self, k: int | float | Value):
        if self.root is not None and self.root.key == k:
            self.root = self.__remove_node(self.root)
        else:
            self.__remove(self.root, k)

        self.__valance__root()

    def __insert(self, node: Bst, k: int | float | Value, v=None):
        if node.key == k:
            return

        if k < node.key:
            if node.left is None:
                node.left = self.init(k, v)
            else:
                self.__insert(node.left, k, v)
        else:
            if node.right is None:
                node.right = self.init(k, v)
            else:
                self.__insert(node.right, k, v)

        node.act_h()
        node.act_size()

        Avl.__valance(node)

    def __remove(self, node: Bst | None, k: int | float | Value):
        if node is None:
            return

        find = False

        if node.left is not None and node.left.key == k:
            node.left = self.__remove_node(node.left)
            find = True

        if node.right is not None and node.right.key == k:
            node.right = self.__remove_node(node.right)
            find = True

        if not find:
            if node.key < k:
                self._remove(node.left, k)
            else:
                self._remove(node.right, k)

        node.act_h()
        node.act_size()

        Avl.__valance(node)

    def __remove_node(self, node: Bst) -> Bst:
        if node.left is None and node.right is None:
            return None

        if node.left is None:

            return node.right

        if node.right is None:
            return node.left

        k = node.key
        aux = node.right.select(0)

        node.key, node.value = aux.key, aux.value
        aux.key = k

        self.__remove(node, k)

        return node

    @staticmethod
    def __f_valance(node: Bst | None) -> int:
        if node is None:
            return 0

        left = 0 if node.left is None else node.left.h
        right = 0 if node.right is None else node.right.h

        return right - left

    def __valance__root(self):
        if Avl.__f_valance(self.root) == 2:
            self.root = Avl.__valance_r(self.root)
        if Avl.__f_valance(self.root) == -2:
            self.root = Avl.__valance_l(self.root)

    @staticmethod
    def __valance(node: Bst):
        if Avl.__f_valance(node.left) == 2:
            node.left = Avl.__valance_r(node.left)
        if Avl.__f_valance(node.left) == -2:
            node.left = Avl.__valance_l(node.left)

        if Avl.__f_valance(node.right) == 2:
            node.right = Avl.__valance_r(node.right)
        if Avl.__f_valance(node.right) == -2:
            node.right = Avl.__valance_l(node.right)

    @staticmethod
    def __valance_r(node: Bst) -> Bst:
        if Avl.__f_valance(node.right) == -1:
            node.right = Avl.__valance_l_s(node.right)

        return Avl.__valance_r_s(node)

    @staticmethod
    def __valance_l(node: Bst) -> Bst:
        if Avl.__f_valance(node.left) == 1:
            node.left = Avl.__valance_r_s(node.left)

        return Avl.__valance_l_s(node)

    @staticmethod
    def __valance_r_s(node: Bst) -> Bst:
        aux = node.right

        node.right = aux.left
        aux.left = node

        aux.left.act_h()
        aux.act_h()

        aux.left.act_size()
        aux.act_size()

        return aux

    @staticmethod
    def __valance_l_s(node: Bst) -> Bst:
        aux = node.left

        node.left = aux.right
        aux.right = node

        aux.right.act_h()
        aux.act_h()

        aux.right.act_size()
        aux.act_size()

        return aux


class Set:
    def __init__(self, l: Iterable[int | float | Value] = []):
        self.__avl = Avl()

        for i in l:
            self.insert(i)

    def __iter__(self) -> Iterable[int | float | Value]:
        return map(lambda node: node.key, self.__avl.in_orden())

    def insert(self, k: int | float | Value):
        self.__avl.insert(k)

    def remove(self, k: int | float | Value):
        self.__avl.remove(k)

    def rank(self, k: int | float | Value) -> int:
        return self.__avl.rank(k)

    def select(self, index: int) -> int | float | Value:
        node = self.__avl.select(index)

        if node is None:
            raise IndexError

        return node.key

    def find(self, k: int | float | Value):
        return self.__avl.find(k) is not None

    def __getitem__(self, index: int) -> int | float | Value:
        return self.select(index)


class Dictionary:
    def __init__(self, l: Iterable[Tuple[int | float | Value, any]] = []):
        self.__avl = Avl()

        for i in l:
            self.insert(i)

    def __iter__(self) -> Iterable[int | float | Value]:
        return map(lambda node: (node.key, node.value), self.__avl.in_orden())

    def insert(self, k: int | float | Value, v: any):
        self.__avl.insert(k, v)

    def remove(self, k: int | float | Value):
        self.__avl.remove(k)

    def rank(self, k: int | float | Value) -> int:
        return self.__avl.rank(k)

    def select(self, index: int) -> Tuple[int | float | Value, any]:
        node = self.__avl.select(index)

        if node is None:
            raise IndexError

        return node.key, node.value

    def find(self, k: int | float | Value):
        return self.__avl.find(k) is not None

    def get(self, k: int | float | Value) -> any:
        node = self.__avl.find(k)

        return Bst if node is None else node.value

    def set(self, k: int | float | Value, v: any) -> any:
        node = self.__avl.find(k)

        if node is not None:
            node.value = v
        else:
            self.insert(k, v)

    def __getitem__(self, k: int | float | Value) -> any:
        return self.get(k)

    def __setitem__(self, k: int | float | Value, v: any) -> any:
        self.set(k, v)


class MultiSet:
    def __init__(self, l: Iterable[int | float | Value] = []):
        self.__avl = Avl(MultiBst)

        for i in l:
            self.insert(i)

    def __iter__(self) -> Iterable[int | float | Value]:
        return map(lambda node: node.key, self.__avl.in_orden())

    def insert(self, k: int | float | Value):
        node = self.__avl.find(k)

        if node is None:
            self.__avl.insert(k, 1)
        else:
            node.value += 1
            node.size += 1
            self.__avl.root.update(k)

    def remove(self, k: int | float | Value):
        node = self.__avl.find(k)

        if node is not None:
            node.value -= 1
            node.size -= 1

            if node.value == 0:
                self.__avl.remove(k)

            self.__avl.update(k)

    def rank(self, k: int | float | Value) -> int:
        return self.__avl.rank(k)

    def select(self, index: int) -> int | float | Value:
        node = self.__avl.select(index)

        if node is None:
            raise IndexError

        return node.key

    def find(self, k: int | float | Value):
        return self.__avl.find(k) is not None

    def __getitem__(self, index: int) -> int | float | Value:
        return self.select(index)
