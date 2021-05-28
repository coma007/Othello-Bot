"""
Implementacija strukture podataka mapa i element mape.
"""


class MapItem(object):
    """
    Klasa MapItem modeluje jedan element iz mape.
    """

    def __init__(self, key, value):
        """
        Konstruktor klase MapItem.

        :param key: Ključ.
        :param value: Vrijednost.
        """

        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __eq__(self, other):
        return self._key == other.key

    def __lt__(self, other):
        return self._key < other.key


class Map(object):

    """
    Klasa Map modeluje mapu.
    """

    def __init__(self):
        """
        Konstruktor klase Map.
        """
        self._data = []

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for item in self._data:
            yield item.key

    def __getitem__(self, key):
        for item in self._data:
            if item.key == key:
                return item.value
        else:
            raise KeyError("Key does not exist !")

    def __setitem__(self, key, value):
        new_item = MapItem(key, value)
        for item in self._data:
            if item == new_item:
                item.value = value
                return

        self._data.append(new_item)

    def __contains__(self, key):
        for item in self._data:
            if item.key == key:
                return True
        else:
            return False

    def __delitem__(self, key):
        for i in range(len(self)):
            if self._data[i].key == key:
                self._data.pop(i)
                return
        else:
            raise KeyError("Key does not exist !")

    def items(self):
        """
        Metoda za iteriranje elementima mape.

        :return: Uređen par (ključ, vrijednost).
        """

        for item in self._data:
            yield item.key, item.value

    def keys(self):
        """
        Metoda za dobijanje svih ključeva iz mape.

        :return: Lista svih ključeva.
        :rtype: list
        """

        keys = []
        for item in self._data:
            keys.append(item.key)
        return keys

    def values(self):
        """
        Metoda za dobijanje svih vrijednosti iz mape.

        :return: Lista svih vrijednosti.
        :rtype: list
        """

        values = []
        for item in self._data:
            values.append(item.value)
        return values

    def clear(self):
        """
        Metoda za brisanje svih elemenata iz mape.
        """

        self._data = []

