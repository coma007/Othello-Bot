"""
Implementacija strukture podataka stablo i pojedinačnih čvorova stabla.
"""

from data_structures.LimitedQueue import *


class TreeNode(object):
    """
    Klasa TreeNode modeluje čvor stabla.
    """

    def __init__(self, data, parent=None, children=None):
        """
        Konstruktor klase TreeNode.

        :param data: Podaci u čvoru.
        :param parent: Roditelj čvora.
        :type parent: data_structures.GameTree.TreeNode
        :param children: Djeca čvora.
        :type children: list
        """

        self._data = data
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        if children is None:
            children = []
        self._children = children

    def __eq__(self, other):
        return self._data == other.data

    def __str__(self):
        return str(self._data)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, new_children):
        self._children = new_children

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    def remove_child(self, sad_child):
        """
        Metoda za brisanje jednog djeteta čvora.

        :param sad_child: Dijete koje se briše.
        :type sad_child: data_structures.GameTree.TreeNode
        """

        self._children.remove(sad_child)

    def add_child(self, new_child):
        """
        Metoda za dodavanje jednog djeteta čvora.

        :param new_child: Dijete koje se dodaje.
        :type new_child: data_structures.GameTree.TreeNode
        """

        self._children.append(new_child)
        new_child.parent = self

    def is_root(self):
        """
        Metoda koja provjerava da li je čvor korijenski.

        :return: True ako je korijen, u suprotnom False.
        :rtype: bool
        """

        return self._parent is None

    def is_leaf(self):
        """
        Metoda koja provjerava da li je čvor lisni.

        :return: True ako je list, u suprotnom False.
        :rtype: bool
        """

        return self._children == []

    def num_children(self):
        """
        Metoda koja računa broj djece čvora.

        :return: Broj djece.
        :rtype: int
        """

        return len(self._children)


class Tree(object):
    """
    Klasa Tree modeluje stablo.
    """

    def __init__(self, root=None):
        """
        Konstruktor klase Tree.

        :param root: Roditelj stabla.
        :type root: data_structures.GameTree.TreeNode
        """

        self._root = root
        self._current = root

    @property
    def root(self):
        return self._root

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, new_current):
        self._current = new_current

    @root.setter
    def root(self, node):
        self._root = node

    def is_empty(self):
        """
        Metoda koja provjerava da li je stablo prazno.

        :return: True ako je prazno, u suprotnom False.
        :rtype: bool
        """

        return self._root is None

    def replace(self, old_node, new_node):
        """
        Metoda koja zamjenjuje određeni čvor novim čvorom.

        :param old_node: Čvor koji se zamjenjuje.
        :type old_node: data_structures.GameTree.TreeNode
        :param new_node: Novi čvor.
        :type new_node: data_structures.GameTree.TreeNode
        """

        parent = old_node.parent
        parent.children[parent.children.index(old_node)] = new_node
        new_node.parent = parent

        children = old_node.children
        new_node.children = children
        for child in children:
            child.parent = new_node

    def depth(self, node):
        """
        Rekurzivna metoda koja računa dubinu određenog čvora.

        :param node: Čvor čija se dubina računa.
        :type node: data_structures.GameTree.TreeNode

        :return: Dubina čvora.
        :rtype: int
        """

        parent = node.parent
        if parent is None:
            return 1
        return 1 + self.depth(parent)

    def height(self):
        """
        Metoda koja računa visinu stabla.

        :return: Visina stabla.
        :rtype: int
        """

        return self._height(self._root)

    def _height(self, node):
        """
        Rekurzivna privatna metoda koja računa visinu određenog čvora.

        :return: Visina čvora.
        :rtype: int
        """

        if node.is_leaf():
            return 1
        else:
            return 1 + max(self._height(x) for x in node.children)

    def preorder(self, f):
        """
        Metoda za preorder obilazak stabla.

        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        self._preorder(self._root, f)

    def _preorder(self, node, f):
        """
        Privatna rekurzivna metoda za preorder obilazak stabla.

        :param node: Čvor od koga se obilazi.
        :type node: data_structures.GameTree.TreeNode
        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        f(node)
        for child in node.children:
            self._preorder(child, f)

    def postorder(self, f):
        """
        Metoda za postorder obilazak stabla.

        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        self._postorder(self._root, f)

    def _postorder(self, node, f):
        """
        Privatna rekurzivna metoda za postorder obilazak stabla.

        :param node: Čvor od koga se obilazi.
        :type node: data_structures.GameTree.TreeNode
        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        for child in node.children:
            if child is not None:
                self._postorder(child, f)
        f(node)

    def breadth(self, f):
        """
        Metoda za breadth-first obilazak stabla.

        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        tree_queue = LimitedQueue(500)
        tree_queue.enqueue(self._root)
        while not tree_queue.is_empty():
            node = tree_queue.dequeue()
            f(node)
            for child in node.children:
                tree_queue.enqueue(child)

    def euler(self, f):
        """
        Metoda za Ojlerov obilazak stabla.

        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        self._euler(self._root, f)

    def _euler(self, node, f):
        """
        Privatna rekurzivna metoda za postorder obilazak stabla.

        :param node: Čvor od koga se obilazi.
        :type node: data_structures.GameTree.TreeNode
        :param f: Funkcija koja se primjenjuje nad obiđenim čvorom.
        :type f: function
        """

        f(node.data)
        for children in node.children:
            self._euler(children, f)
        else:
            if node.parent is not None:
                f(node.parent.data)
