"""
Implementation of the data structure Dynamic Array.
"""


def _prepare_locations(capacity):
    """
    Static method that prepares memory locations necessary for creating a dynamic array.

    :param capacity: Capacity of the array.
    :type capacity: int

    :return: Prepared memory locations for the array.
    :rtype: _ctypes.PyCArrayType
    """

    from ctypes import py_object
    return (capacity * py_object)()


class DynamicArray(object):
    """
    Class DynamicArray models a dynamic array.
    """

    def __init__(self, default_capacity=None):
        """
        Constructor of the DynamicArray class.

        :param default_capacity: Default capacity.
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
        Method to add a new element to the end of the array.

        :param elem: New element.
        """

        if self._nelem == self._capacity:
            self._resize(2*self._capacity)
        self._array[self._nelem] = elem
        self._nelem += 1

    def insert_at(self, index, elem):
        """
        Method to add a new element to the array at a specific position.

        :param index: Position.
        :param elem: New element.
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
        Method to add a new element to the beginning of the array.

        :param elem: New element.
        """

        if self._nelem == 0:
            self.append(elem)
        else:
            self.insert_at(0, elem)

    def pop(self):
        """
        Method to remove an element from the end of the array.
        """

        if 0 == self._nelem:
            raise Exception("Empty array !")
        last = self._array[self._nelem-1]
        self._array[self._nelem-1] = 0
        self._nelem -= 1
        return last

    def remove_at(self, index):
        """
        Method to remove an element from the array at a specific position.

        :param index: Index of the element to be removed.
        """

        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        for i in range(index+1, self._nelem-1):
            self._array[i-1] = self._array[i]

    def remove_first(self):
        """
        Method to remove the first element from the array.
        """

        if self._nelem == 0:
            raise Exception("Empty array !")
        else:
            self.remove_at(0)

    def _resize(self, new_capacity):
        """
        Private method to resize the capacity of the array.

        :param new_capacity: New capacity.
        """

        new_array = _prepare_locations(new_capacity)
        for index in range(self._nelem):
            new_array[index] = self._array[index]
        self._array = new_array
        self._capacity = new_capacity
