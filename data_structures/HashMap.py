"""
Implementacija strukture podataka heš mapa.
"""

from data_structures.Array import *
from data_structures.Map import *
from random import randint, randrange
from constants import *


class HashMap(object):
    """
    Klasa HashMap modeluje heš mapu.
    """

    def __init__(self, capacity=128):
        """
        Konstruktor klase HashMap.

        :param capacity: Kapacitet heš mape.
        :type capacity: int
        """

        self._table = DynamicArray(capacity)
        self._size = 0
        self._capacity = self._table.capacity
        self._init_buckets()
        self._board_values = self._init_table()

        self.prime = 109345121
        self._a = 1 + randrange(self.prime-1)
        self._b = randrange(self.prime)

    def __len__(self):
        return self._size

    def __iter__(self):
        for bucket in self._table:
            if len(bucket) != 0:
                for key in bucket:
                    yield key

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

    def _init_buckets(self):
        """
        Privatna metoda za iniciranje bucket-a u heš mapi.
        """

        for i in range(self._capacity):
            self._table.append(Map())

    def _init_table(self):
        """
        Privatna metoda za iniciranje vrijednosti polja na tabli.

        :return: Tabla sa vrijednostima svakog polja.
        :rtype: list
        """

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

    def _Zobrist_hashing(self, key):
        """
        Zobrist heširanje ključa (prvo heširanje).

        :param key: Ključ.

        :return: Heširan ključ.
        :rtype: int
        """

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
        """
        Privatna metoda za drugo heširanje i kompresovanje ključa.

        :param key: Ključ.

        :return: Kompresovan ključ.
        :rtype: int
        """

        Zobrist_key = self._Zobrist_hashing(key)
        hashed_key = (Zobrist_key*self._a + self._b) % self.prime
        return hashed_key % self._capacity

    def _bucket_getitem(self, index, key):
        """
        Privatna metoda za dobijanje elementa iz bucket-a na osnovu ključa.

        :param index: Indeks ključa u bucket-u.
        :type index: int
        :param key: Ključ.

        :return: Vrijednost pod ključem.
        """

        bucket = self._table[index]
        return bucket[key]

    def _bucket_setitem(self, index, key, value):
        """
        Privatna metoda za postavljanje elementa u bucket na osnovu ključa.

        :param index: Indeks ključa u bucket-u.
        :type index: int
        :param key: Ključ.
        :param value: Vrijednost.
        """

        bucket = self._table[index]
        bucket[key] = value

    def _bucket_delitem(self, index, key):
        """
        Privatna metoda za brisanje elementa iz bucket-a na osnovu ključa.

        :param index: Indeks ključa u bucket-u.
        :type index: int
        :param key: Ključ.
        """

        bucket = self._table[index]
        if len(bucket) == 0:
            raise KeyError("Key does not exist !")
        else:
            del bucket[key]
