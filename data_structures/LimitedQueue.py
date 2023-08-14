"""
Implementation of the data structure Queue.
"""

class EmptyQueueException(Exception):
    pass


class FullQueueException(Exception):
    pass


class LimitedQueue(object):
    """
    Class LimitedQueue models a queue.
    """

    def __init__(self, default_capacity):
        """
        Constructor of the LimitedQueue class.

        :param default_capacity: Default capacity.
        :type default_capacity: int
        """

        self._front = 0
        self._rear = 0
        self._size = 0
        self._capacity = default_capacity
        self._queue = [None] * default_capacity

    def __len__(self):
        return self._size

    def __str__(self):
        string = ''
        if self._rear > self._front:
            for index in range(self._front, self._rear):
                string += str(self._queue[index]) + ' '
            return string
        elif self._rear <= self._front:
            for index in range(self._front, self._capacity):
                string += str(self._queue[index]) + ' '
            for index in range(self._rear):
                string += str(self._queue[index]) + ' '
            return string
        if self._size == 0:
            raise EmptyQueueException("Empty queue.")

    def show_queue(self):
        """
        Method to display all elements in the queue.
        """

        for i in range(self._capacity):
            print((i-self._front) % self._capacity, ".", self._queue[i], end="\t")

    def is_empty(self):
        """
        Method to check if the queue is empty.

        :return: True if empty, False otherwise.
        :rtype: bool
        """

        return self._size == 0

    def get_first(self):
        """
        Method that returns the first element in the queue.

        :raises EmptyQueueException: If the queue is empty.
        """

        if self.is_empty():
            raise EmptyQueueException("Empty queue !")
        return self._queue[self._front]

    def enqueue(self, elem):
        """
        Method to add a new element to the queue.

        :param elem: New element.
        :raises FullQueueException: If the queue is full.
        """

        if self._rear == self._capacity:
            for index in range(self._front):
                if self._queue[index] is None:
                    self._rear = index + 1
                    self._queue[index] = elem
                    self._size += 1
        elif (self._rear != self._front and self._rear < self._capacity) or self.is_empty():
            self._queue[self._rear] = elem
            self._rear += 1
            self._size += 1
        elif self._front == self._rear and self._size != 0:
            raise FullQueueException("Full queue !")

    def dequeue(self):
        """
        Method that removes and returns the element at the front of the queue.

        :return: Removed element.
        """

        tmp = self._queue[self._front]
        self._queue[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return tmp
