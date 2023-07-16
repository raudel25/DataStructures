# class SparseTable
# {

# private:
#     vector<vi> lookup;

#     vi arr;

#     int operation(int a, int b)
#     {
#         if (arr[a] <= arr[b])
#             return a;

#         return b;
#     }

#     int simple_node(int i) { return i; }

#     void build_sparse_table()
#     {
#         int n = arr.size();

#         for (int i = 0; i < n; i++)
#             lookup[i][0] = simple_node(i);

#         for (int j = 1; (1 << j) <= n; j++)
#         {
#             for (int i = 0; i <= n - (1 << j); i++)
#                 lookup[i][j] = operation(lookup[i][j - 1],
#                                          lookup[i + (1 << (j - 1))][j - 1]);
#         }
#     }

# public:
#     SparseTable(vi &a)
#     {
#         int q = (int)log2(a.size());

#         arr.assign(a.size(), 0);
#         lookup.assign(a.size(), vi(q + 1));

#         for (int i = 0; i < a.size(); i++)
#             arr[i] = a[i];

#         build_sparse_table();
#     }

#     int query(int l, int r)
#     {
#         int q = (int)log2(r - l + 1);

#         return operation(lookup[l][q], lookup[r - (1 << q) + 1][q]);
#     }

#     int get(int i) { return arr[i]; }
# };

from .value import Value
from .properties import Property, PropertyRmq
from typing import List
from math import log2


class SparseTable:
    def __init__(self, l: List[int | float | Value], prop: Property = PropertyRmq()):
        q = int(log2(len(l)))

        self.__values = l.copy()
        self.__lookup = [[0]*(q+1) for _ in range(len(l))]
        self.__prop = prop
        self.__prop.assign_values(self.__values)

        self.__build_sparse_table()

    def get(self, index: int) -> int | float | Value:
        return self.__values[index]

    def query(self, l: int, r: int):
        q = int(log2(r-l+1))

        return self.__prop.prop(self.__lookup[l][q], self.__lookup[r - (1 << q) + 1][q])

    def __build_sparse_table(self):
        n = len(self.__values)

        for i in range(n):
            self.__lookup[i][0] = self.__prop.simple_node(i)

        j = 1
        while (1 << j) <= n:
            for i in range(n-(1 << j)+1):
                self.__lookup[i][j] = self.__prop.prop(
                    self.__lookup[i][j - 1], self.__lookup[i + (1 << (j - 1))][j - 1])

            j += 1
