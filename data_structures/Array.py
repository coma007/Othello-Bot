"""
Implementacija strukture podataka niz.
"""


def _prepare_locations(capacity):
    """
    Statička metoda koja priprema memorijske lokacije neophodne za obrazovanje niza.

    :param capacity: Kapacitet niza.
    :type capacity: int

    :return: Pripremljene memorijske lokacije za niz.
    :rtype: _ctypes.PyCArrayType
    """

    from ctypes import py_object
    return (capacity * py_object)()


class DynamicArray(object):
    """
    Klasa DynamicArray modeluje dinamički niz.
    """

    def __init__(self, default_capacity=None):
        """
        Konsturktor klase DynamicArray.

        :param default_capacity: Podrazumijevani kapacitet.
        :type default_capacity: int.
        """

        self._nelem = 0
        if default_capacity is None:
            self._capacity = 1
        else:
            self._capacity = default_capacity
        self._array = _prepare_locations(self._capacity)

    def __len__(self):
        return self._nelem

    def __str__(self):
        string = ''
        for index in range(self._nelem):
            string += str(self._array[index]) + ' '
        return string

    def __getitem__(self, index):
        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        return self._array[index]

    def __iter__(self):
        for i in range(self._nelem):
            yield self[i]

    @property
    def capacity(self):
        return self._capacity

    def append(self, elem):
        """
        Metoda za dodavanje novog elementa na kraj niza.

        :param elem: Novi element.
        """

        if self._nelem == self._capacity:
            self._resize(2*self._capacity)
        self._array[self._nelem] = elem
        self._nelem += 1

    def insert_at(self, index, elem):
        """
        Metoda za dodavanje novog elementa u niz na određenu poziciju.

        :param index: Pozicija.
        :param elem: Novi element.
        """

        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        if self._nelem == self._capacity:
            self._resize(2*self._capacity)
        for i in range(self._nelem-1, index-1, -1):
            self._array[i+1] = self._array[i]      # make space for elem at index
        self._array[index] = elem
        self._nelem += 1

    def insert_first(self, elem):
        """
        Metoda za dodavanje novog elementa na početak niza.

        :param elem: Novi element.
        """

        if self._nelem == 0:
            self.append(elem)
        else:
            self.insert_at(0, elem)

    def pop(self):
        """
        Metoda za uklanjanje elementa sa kraja niza.
        """

        if 0 == self._nelem:
            raise Exception("Empty array !")
        last = self._array[self._nelem-1]
        self._array[self._nelem-1] = 0
        self._nelem -= 1
        return last

    def remove_at(self, index):
        """
        Metoda za uklanjanje elementa iz niza sa određene pozicije.

        :param index: Novi element.
        """

        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        for i in range(index+1, self._nelem-1):
            self._array[i-1] = self._array[i]

    def remove_first(self):
        """
        Metoda za uklanjanje prvog elementa niza.
        """

        if self._nelem == 0:
            raise Exception("Empty array !")
        else:
            self.remove_at(0)

    def _resize(self, new_capacity):
        """
        Privatna metoda za povećanje kapaciteta niza.

        :param new_capacity: Novi kapacitet.
        """

        new_array = _prepare_locations(new_capacity)
        for index in range(self._nelem):
            new_array[index] = self._array[index]
        self._array = new_array
        self._capacity = new_capacity
