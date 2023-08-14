"""
Implementation of the data structure Tree and individual tree nodes.
"""

from data_structures.LimitedQueue import *


class TreeNode(object):
    """
    Class TreeNode models a tree node.
    """

    def __init__(self, data, parent=None, children=None):
        """
        Constructor of the TreeNode class.

        :param data: Data in the node.
        :param parent: Parent node.
        :type parent: data_structures.GameTree.TreeNode
        :param children: Children nodes.
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

    def remove_child(self, child_to_remove):
        """
        Method to remove a child node.

        :param child_to_remove: Child to be removed.
        :type child_to_remove: data_structures.GameTree.TreeNode
        """

        self._children.remove(child_to_remove)

    def add_child(self, new_child):
        """
        Method to add a child node.

        :param new_child: Child to be added.
        :type new_child: data_structures.GameTree.TreeNode
        """

        self._children.append(new_child)
        new_child.parent = self

    def is_root(self):
        """
        Method that checks if the node is the root.

        :return: True if it is the root, otherwise False.
        :rtype: bool
        """

        return self._parent is None

    def is_leaf(self):
        """
        Method that checks if the node is a leaf.

        :return: True if it is a leaf, otherwise False.
        :rtype: bool
        """

        return self._children == []

    def num_children(self):
        """
        Method that calculates the number of children of the node.

        :return: Number of children.
        :rtype: int
        """

        return len(self._children)


class Tree(object):
    """
    Class Tree models a tree.
    """

    def __init__(self, root=None):
        """
        Constructor of the Tree class.

        :param root: Root node of the tree.
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
        Method that checks if the tree is empty.

        :return: True if empty, otherwise False.
        :rtype: bool
        """

        return self._root is None

    def replace(self, old_node, new_node):
        """
        Method that replaces a specific node with a new node.

        :param old_node: Node to be replaced.
        :type old_node: data_structures.GameTree.TreeNode
        :param new_node: New node.
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
        Recursive method that calculates the depth of a specific node.

        :param node: Node whose depth is calculated.
        :type node: data_structures.GameTree.TreeNode

        :return: Depth of the node.
        :rtype: int
        """

        parent = node.parent
        if parent is None:
            return 1
        return 1 + self.depth(parent)

    def height(self):
        """
        Method that calculates the height of the tree.

        :return: Height of the tree.
        :rtype: int
        """

        return self._height(self._root)

    def _height(self, node):
        """
        Recursive private method that calculates the height of a specific node.

        :return: Height of the node.
        :rtype: int
        """

        if node.is_leaf():
            return 1
        else:
            return 1 + max(self._height(x) for x in node.children)

    def preorder(self, f):
        """
        Method for preorder traversal of the tree.

        :param f: Function applied to each visited node.
        :type f: function
        """

        self._preorder(self._root, f)

    def _preorder(self, node, f):
        """
        Private recursive method for preorder traversal of the tree.

        :param node: Node being traversed from.
        :type node: data_structures.GameTree.TreeNode
        :param f: Function applied to each visited node.
        :type f: function
        """

        f(node)
        for child in node.children:
            self._preorder(child, f)

    def postorder(self, f):
        """
        Method for postorder traversal of the tree.

        :param f: Function applied to each visited node.
        :type f: function
        """

        self._postorder(self._root, f)

    def _postorder(self, node, f):
        """
        Private recursive method for postorder traversal of the tree.

        :param node: Node being traversed from.
        :type node: data_structures.GameTree.TreeNode
        :param f: Function applied to each visited node.
        :type f: function
        """

        for child in node.children:
            if child is not None:
                self._postorder(child, f)
        f(node)

    def breadth(self, f):
        """
        Method for breadth-first traversal of the tree.

        :param f: Function applied to each visited node.
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
        Method for Eulerian traversal of the tree.

        :param f: Function applied to each visited node.
        :type f: function
        """

        self._euler(self._root, f)

    def _euler(self, node, f):
        """
        Private recursive method for Eulerian traversal of the tree.

        :param node: Node being traversed from.
        :type node: data_structures.GameTree.TreeNode
        :param f: Function applied to each visited node.
        :type f: function
        """

        f(node.data)
        for children in node.children:
            self._euler(children, f)
        else:
            if node.parent is not None:
                f(node.parent.data)
