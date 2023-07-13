from .value import Value
from typing import Tuple, Iterable


class Node:
    def __init__(self, k: int | float | Value, v=None):
        self.key: int | float | Value = k
        self.value = v
        self.size: int = 1
        self.h = 1
        self.left: Node = None
        self.right: Node = None

    def pre_orden(self) -> Iterable['Node']:
        yield self

        if self.left is not None:
            for i in self.left.pre_orden():
                yield i

        for i in self.right.pre_orden():
            yield i

    def in_orden(self) -> Iterable['Node']:
        if self.left is not None:
            for i in self.left.in_orden():
                yield i

        yield self

        if self.right is not None:
            for i in self.right.in_orden():
                yield i

    def post_orden(self) -> Iterable['Node']:
        if self.left is not None:
            for i in self.left.post_orden():
                yield i

        if self.right is not None:
            for i in self.right.post_orden():
                yield i

        yield self

    def find(self, k: int | float | Value) -> 'Node':
        if self.key == k:
            return self

        if k < self.key:
            return None if self.left is None else self.left.find(k)

        return None if self.right is None else self.right.find(k)

    def rank(self, k: int | float | Value) -> int:
        left = 0 if self.left is None else self.left.size

        if k == self.key:
            return left

        if k < self.key:
            return 0 if self.left is None else self.left.rank(k)

        return left + 1 if self.right is None else left + 1 + self.right.rank(k)

    def select(self, index: int) -> 'Node':
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


class Avl:
    def __init__(self):
        self.root: Node = None

    def pre_orden(self) -> Iterable[Node]:
        if self.root is None:
            return []
        return self.root.pre_orden()

    def in_orden(self) -> Iterable[Node]:
        if self.root is None:
            return []
        return self.root.in_orden()

    def post_orden(self) -> Iterable[Node]:
        if self.root is None:
            return []
        return self.root.post_orden()

    def find(self, k: int | float | Value) -> Node:
        if self.root is None:
            return None
        return self.root.find(k)

    def rank(self, k: int | float | Value) -> int:
        return self.root.rank(k)

    def select(self, index: int) -> Node | None:
        if self.root is None:
            return None
        return self.root.select(index)

    def insert(self, k: int | float | Value, v=None):
        if self.root is None:
            self.root = Node(k, v)
            return

        Avl.__insert(self.root, k, v)
        self.__valance__root()

    def remove(self, k: int | float | Value):
        if self.root is not None and self.root.key == k:
            self.root = Avl.__remove_node(self.root)
        else:
            Avl.__remove(self.root, k)

        self.__valance__root()

    @staticmethod
    def __insert(node: Node, k: int | float | Value, v=None):
        if node.key == k:
            return

        if k < node.key:
            if node.left is None:
                node.left = Node(k, v)
            else:
                Avl.__insert(node.left, k, v)
        else:
            if node.right is None:
                node.right = Node(k, v)
            else:
                Avl.__insert(node.right, k, v)

        node.act_h()
        node.act_size()

        Avl.__valance(node)

    @staticmethod
    def __remove(node: Node | None, k: int | float | Value):
        if node is None:
            return

        find = False

        if node.left is not None and node.left.key == k:
            node.left = Avl.__remove_node(node.left)
            find = True

        if node.right is not None and node.right.key == k:
            node.right = Avl.__remove_node(node.right)
            find = True

        if not find:
            if node.key < k:
                Avl.__remove(node.left, k)
            else:
                Avl.__remove(node.right, k)

        node.act_h()
        node.act_size()

        Avl.__valance(node)

    @staticmethod
    def __remove_node(node: Node) -> Node:
        if node.left is None and node.right is None:
            return None

        if node.left is None:

            return node.right

        if node.right is None:
            return node.left

        k = node.key
        aux = Avl.__select(node.right, 0)

        node.key, node.value = aux.key, aux.value
        aux.key = k

        Avl.__remove(node, k)

        return node

    @staticmethod
    def __f_valance(node: Node | None) -> int:
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
    def __valance(node: Node):
        if Avl.__f_valance(node.left) == 2:
            node.left = Avl.__valance_r(node.left)
        if Avl.__f_valance(node.left) == -2:
            node.left = Avl.__valance_l(node.left)

        if Avl.__f_valance(node.right) == 2:
            node.right = Avl.__valance_r(node.right)
        if Avl.__f_valance(node.right) == -2:
            node.right = Avl.__valance_l(node.right)

    @staticmethod
    def __valance_r(node: Node) -> Node:
        if Avl.__f_valance(node.right) == -1:
            node.right = Avl.__valance_l_s(node.right)

        return Avl.__valance_r_s(node)

    @staticmethod
    def __valance_l(node: Node) -> Node:
        if Avl.__f_valance(node.left) == 1:
            node.left = Avl.__valance_r_s(node.left)

        return Avl.__valance_l_s(node)

    @staticmethod
    def __valance_r_s(node: Node) -> Node:
        aux = node.right

        node.right = aux.left
        aux.left = node

        aux.left.act_h()
        aux.act_h()

        aux.left.act_size()
        aux.act_size()

        return aux

    @staticmethod
    def __valance_l_s(node: Node) -> Node:
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

        return Node if node is None else node.value

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


class MultiSet(Avl):
    def __init__(self, l: Iterable[int | float | Value] = []):
        self.__avl = Avl()

        for i in l:
            self.insert(i)

    def __iter__(self) -> Iterable[int | float | Value]:
        for node in self.__avl.in_orden():
            for i in range(node.value):
                yield node.key

    def insert(self, k: int | float | Value):
        node = self.__avl.find(k)

        if node is None:
            self.__avl.insert(k, 1)
        else:
            node.value += 1
            node.size += 1
            self.__avl.update(k)

    def remove(self, k: int | float | Value):
        node = self.__avl.find(k)

        if node is not None:
            print(node.size)
            node.value -= 1
            node.size -= 1

            if node.value == 0:
                self.__avl.remove(k)

            self.__avl.update(k)

    def rank(self, k: int | float | Value) -> int:
        return MultiSet.__rank(self.__avl, k)

    def select(self, index: int) -> int | float | Value:
        node = MultiSet.__select(self.__avl.root, index)

        if node is None:
            raise IndexError

        return node.key

    def find(self, k: int | float | Value):
        return self.__avl.find(k) is not None

    def __rank(node: Node | None, k: int | float | Value) -> int:
        if node is None:
            return 0

        left = 0 if node.left is None else node.left.size

        if k == node.key:
            return left

        if k < node.key:
            return MultiSet._rank(node.left, k)

        return left + node.value + MultiSet.__rank(node.right, k)

    def __select(node: Node | None, index: int) -> Node | None:
        if node is None:
            return None

        if index < 0 or index >= node.size:
            print(node.size)
            return None

        left = 0 if node.left is None else node.left.size

        if left <= index and index < left + node.value:
            return node

        if index < left:
            return MultiSet.__select(node.left, index)

        return MultiSet.__select(node.right, index - left - node.value)

    def __getitem__(self, index: int) -> int | float | Value:
        return self.select(index)
