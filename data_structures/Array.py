
def _prepare_locations(capacity):
    from ctypes import py_object
    return (capacity * py_object)()      # create number = capacity of memory locations


class DynamicArray(object):

    def __init__(self, default_capacity=None):
        self._nelem = 0
        if default_capacity is None:
            self._capacity = 1
        else:
            self._capacity = default_capacity
        self._array = _prepare_locations(self._capacity)

    def __len__(self):
        return self._nelem

    @property
    def capacity(self):
        return self._capacity

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

    def append(self, elem):
        if self._nelem == self._capacity:
            self._resize(2*self._capacity)
        self._array[self._nelem] = elem
        self._nelem += 1

    def insert_at(self, index, elem):

        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        if self._nelem == self._capacity:
            self._resize(2*self._capacity)
        for i in range(self._nelem-1, index-1, -1):
            self._array[i+1] = self._array[i]      # make space for elem at index

        self._array[index] = elem
        self._nelem += 1

    def insert_first(self, elem):
        if self._nelem == 0:
            self.append(elem)
        else:
            self.insert_at(0, elem)

    def pop(self):
        if 0 == self._nelem:
            raise Exception("Empty array !")
        last = self._array[self._nelem-1]
        self._array[self._nelem-1] = 0
        self._nelem -= 1
        return last

    def remove_at(self, index):
        if not 0 <= index < self._nelem:
            raise IndexError('Invalid index !')
        for i in range(index+1, self._nelem-1):
            self._array[i-1] = self._array[i]

    def remove_first(self):
        if self._nelem == 0:
            raise Exception("Empty array !")
        else:
            self.remove_at(0)

    def _resize(self, new_capacity):
        new_array = _prepare_locations(new_capacity)
        for index in range(self._nelem):
            new_array[index] = self._array[index]
        self._array = new_array
        self._capacity = new_capacity


if __name__ == '__main__':

    array1 = DynamicArray()
    for i in range(20):
        array1.append(i)
    print("Array: ", end="")
    print(array1)
    print("Length of array: ", len(array1))
    print("Capacity of array: ", array1.capacity)
    array1.insert_at(5, 100)
    print("Array after insertion: ", end="")
    print(array1)
    print(array1[5])
    array1.remove_at(10)
    array1.remove_first()
    print("Array after removing: ", end="")
    print(array1)
