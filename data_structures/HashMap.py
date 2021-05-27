from data_structures.Array import *
from data_structures.Map import *
from random import randint
from constants import *


class HashMap(object):

    def __init__(self, capacity=128):
        self._table = DynamicArray(capacity)
        self._size = 0
        self._capacity = self._table.capacity
        self._init_buckets()
        self._board_values = self._init_table()

    def _init_table(self):
        table = []
        for i in range(8):
            column = []
            for j in range(8):
                numbers = []
                for k in range(2):
                    numbers.append(randint(0, 255))
                column.append(numbers)
            table.append(column)
        return table

    def _init_buckets(self):
        for i in range(self._capacity):
            self._table.append(Map())

    def _Zobrist_hashing(self, key):
        hashed = 0
        for i in range(8):
            for j in range(8):
                piece = key[i][j]
                field = self._board_values[i][j]
                if piece != 0:
                    if piece.color == WHITE:
                        color = 0
                    else:
                        color = 1
                    table_value = field[color]
                    hashed ^= table_value
        return hashed

    def _compress_key(self, key):
        hashed_key = self._Zobrist_hashing(key)
        return hashed_key % self._capacity

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        compressed_index = self._compress_key(key)
        return self._bucket_getitem(compressed_index, key)

    def __setitem__(self, key, value):
        compressed_index = self._compress_key(key)
        self._bucket_setitem(compressed_index, key, value)

    def __delitem__(self, key):
        compressed_index = self._compress_key(key)
        self._bucket_delitem(compressed_index, key)

    def __contains__(self, key):
        compressed_index = self._compress_key(key)
        bucket = self._table[compressed_index]
        if key in bucket:
            return True
        else:
            return False

    def items(self):
        pass

    def _bucket_getitem(self, index, key):
        bucket = self._table[index]
        return bucket[key]

    def _bucket_setitem(self, index, key, value):
        bucket = self._table[index]
        bucket[key] = value

    def _bucket_delitem(self, index, key):
        bucket = self._table[index]
        if len(bucket) == 0:
            raise KeyError("Key does not exist !")
        else:
            del bucket[key]

    def __iter__(self):
        for bucket in self._table:
            if len(bucket) != 0:
                for key in bucket:
                    yield key

