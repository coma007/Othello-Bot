"""
Implementacija strukture podataka red.
"""


class EmptyQueueException(Exception):
    pass


class FullQueueException(Exception):
    pass


class LimitedQueue(object):
    """
    Klasa LimitedQueue modeluje red.
    """

    def __init__(self, default_capacity):
        """
        Konstruktor klase LimitedQueue.

        :param default_capacity: Podrazumijevani kapacitet
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
        Metoda za ispis svih elemenata reda.
        """

        for i in range(self._capacity):
            print((i-self._front) % self._capacity, ".", self._queue[i], end="\t")

    def is_empty(self):
        """
        Metoda koja provjerava da li je red prazan.

        :return: True ako je prazno, u suprotnom False.
        :rtype: bool
        """

        return self._size == 0

    def get_frist(self):
        """
        Metoda koja vraća prvi element reda.

        :raises EmptyQueueException: Ukoliko je red prazan.
        """

        if self.is_empty():
            raise EmptyQueueException("Empty queue !")
        return self._queue[self._front]

    def enqueue(self, elem):
        """
        Metoda koja dodaje novi element u red.

        :param elem: Novi element.
        :raises FullQueueException: Ukoliko je red pun.
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
        Metoda koja element na redu izbacuje iz reda.

        :return: Izbačen element.
        """

        tmp = self._queue[self._front]
        self._queue[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return tmp

