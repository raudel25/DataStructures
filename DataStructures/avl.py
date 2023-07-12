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


class Avl:
    def __init__(self):
        self.__root: Node = None

    def pre_orden(self) -> Iterable[Node]:
        return Avl.__pre_orden(self.__root)

    def in_orden(self) -> Iterable[Node]:
        return Avl.__in_orden(self.__root)

    def post_orden(self) -> Iterable[Node]:
        return Avl.__post_orden(self.__root)

    def find(self, k: int | float | Value) -> Node:
        return Avl.__find(self.__root, k)

    def rank(self, k: int | float | Value) -> int:
        return Avl.__rank(self.__root, k)

    def select(self, index: int) -> Node | None:
        if self.__root is None:
            return None
        return Avl.__select(self.__root, index)

    def insert(self, k: int | float | Value, v=None):
        if self.__root is None:
            self.__root = Node(k, v)
            return

        Avl.__insert(self.__root, k, v)
        self.__valance__root()

    def remove(self, k: int | float | Value):
        if self.__root.key == k and self.__root.size == 1:
            self.__root = None
            return

        Avl.__remove(self.__root, k)
        self.__valance__root()

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

        Avl.__act_h(node)
        Avl.__act_size(node)

        Avl.__valance(node)

    def __remove(node: Node | None, k: int | float | Value):
        if node is None:
            return

        if node.key == k:
            if node.left is None and node.right is None:
                return

            hl = 0 if node.left is None else node.left.h
            hr = 0 if node.right is None else node.right.h

            if hl < hr:
                node.key, node.value = node.right.key, node.right.value
                node.right.key = k
                Avl.__remove(node.right, k)
            else:
                node.key, node.value = node.left.key, node.left.value
                node.left.key = k
                Avl.__remove(node.left, k)
        else:
            if node.key < k:
                Avl.__remove(node.left, k)
            else:
                Avl.__remove(node.right, k)

        if node.left is not None and node.left.key == k:
            node.left = None

        if node.right is not None and node.right.key == k:
            node.right = None

        Avl.__act_h(node)
        Avl.__act_size(node)

        Avl.__valance(node)

    def __pre_orden(node: Node | None) -> Iterable[Node]:
        if node is None:
            return []

        yield node

        for i in Avl.__pre_orden(node.left):
            yield i

        for i in Avl.__pre_orden(node.right):
            yield i

    def __in_orden(node: Node | None) -> Iterable[Node]:
        if node is None:
            return []

        for i in Avl.__in_orden(node.left):
            yield i

        yield node

        for i in Avl.__in_orden(node.right):
            yield i

    def __post_orden(node: Node | None) -> Iterable[Node]:
        if node is None:
            return []

        for i in Avl.__post_orden(node.left):
            yield i

        for i in Avl.__post_orden(node.right):
            yield i

        yield node

    def __find(node: Node | Node, k: int | float | Value) -> Node:
        if node.key == k:
            return node

        if k < node.key:
            return None if node.left is None else Avl.__find(node.left, k)

        return None if node.right is None else Avl.__find(node.right, k)

    def __rank(node: Node | None, k: int | float | Value) -> int:
        if node is None:
            return 0

        left = 0 if node.left is None else node.left.size

        if k == node.key:
            return left

        if k < node.key:
            return Avl.__rank(node.left, k)

        return left + 1 + Avl.__rank(node.right, k)

    def __select(node: Node | None, index: int) -> Node | None:
        if node is None:
            return None

        if index < 0 or index >= node.size:
            return None

        left = 0 if node.left is None else node.left.size

        if index == left:
            return node

        if index < left:
            return Avl.__select(node.left, index)

        return Avl.__select(node.right, index - left - 1)

    def __f_valance(node: Node | None) -> int:
        if node is None:
            return 0

        left = 0 if node.left is None else node.left.h
        right = 0 if node.right is None else node.right.h

        return right - left

    def __valance__root(self):
        if Avl.__f_valance(self.__root) == 2:
            self.__root = Avl.__valance_r(self.__root)
        if Avl.__f_valance(self.__root) == -2:
            self.__root = Avl.__valance_l(self.__root)

    def __valance(node: Node):
        if Avl.__f_valance(node.left) == 2:
            node.left = Avl.__valance_r(node.left)
        if Avl.__f_valance(node.left) == -2:
            node.left = Avl.__valance_l(node.left)

        if Avl.__f_valance(node.right) == 2:
            node.right = Avl.__valance_r(node.right)
        if Avl.__f_valance(node.right) == -2:
            node.right = Avl.__valance_l(node.right)

    def __valance_r(node: Node) -> Node:
        if Avl.__f_valance(node.right) == -1:
            node.right = Avl.__valance_l_s(node.right)

        return Avl.__valance_r_s(node)

    def __valance_l(node: Node) -> Node:
        if Avl.__f_valance(node.left) == 1:
            node.left = Avl.__valance_r_s(node.left)

        return Avl.__valance_l_s(node)

    def __valance_r_s(node: Node) -> Node:
        aux = node.right

        node.right = aux.left
        aux.left = node

        Avl.__act_h(aux.left)
        Avl.__act_h(aux)

        Avl.__act_size(aux.left)
        Avl.__act_size(aux)

        return aux

    def __valance_l_s(node: Node) -> Node:
        aux = node.left

        node.left = aux.right
        aux.right = node

        Avl.__act_h(aux.right)
        Avl.__act_h(aux)

        Avl.__act_size(aux.right)
        Avl.__act_size(aux)

        return aux

    def __act_h(node: Node):
        hl: int = 0 if node.left is None else node.left.h
        hr: int = 0 if node.right is None else node.right.h

        node.h = max(hl, hr) + 1

    def __act_size(node: Node):
        sl: int = 0 if node.left is None else node.left.size
        sr: int = 0 if node.right is None else node.right.size

        node.size = sl + sr + 1


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
        return self.__avl.select(index).key

    def find(self, k: int | float | Value):
        return self.__avl.find(k) is not None

    def __getitem__(self, index: int) -> int | float | Value:
        return self.select(index)
