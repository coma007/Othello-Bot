from data_structures.LimitedQueue import *


class TreeNode(object):

    def __init__(self, data, parent=None, children=None):
        self._data = data
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        if children is None:
            children = []
        self._children = children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def children(self):
        return self._children

    def remove_child(self, child):
        self._children.remove(child)

    @children.setter
    def children(self, new_children):
        self._children = new_children

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    def add_child(self, node):
        self._children.append(node)
        node.parent = self

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return self._children == []

    def num_children(self):
        return len(self._children)

    def __eq__(self, other):
        return self._data == other.data

    def __str__(self):
        return str(self._data)


class Tree(object):

    def __init__(self, root=None):
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
        return self._root is None

    def replace(self, old_node, new_node):
        parent = old_node.parent
        parent.children[parent.children.index(old_node)] = new_node
        new_node.parent = parent

        children = old_node.children
        new_node.children = children
        for child in children:
            child.parent = new_node

    def depth(self, node):
        parent = node.parent
        if parent is None:
            return 1
        return 1 + self.depth(parent)

    def height(self):
        return self._height(self._root)

    def _height(self, node):
        if node.is_leaf():
            return 1
        else:
            return 1 + max(self._height(x) for x in node.children)

    def preorder(self, f):
        self._preorder(self._root, f)

    def _preorder(self, node, f):
        f(node)
        for child in node.children:
            self._preorder(child, f)

    def postorder(self, f):
        self._postorder(self._root, f)

    def _postorder(self, node, f):
        for child in node.children:
            if child is not None:
                self._postorder(child, f)
        f(node)

    def breadth(self, f):
        queue = LimitedQueue(500)
        queue.enqueue(self._root)
        while not queue.is_empty():
            node = queue.dequeue()
            f(node)
            for child in node.children:
                queue.enqueue(child)

    def euler(self):
        self._euler(self._root)

    def _euler(self, node):
        print(node.data, end=" ")
        for children in node.children:
            self._euler(children)
        else:
            if node.parent is not None:
                print(node.parent.data, end=" ")


if __name__ == '__main__':
    tree = Tree(TreeNode(0))
    for i in range(1, 5):
        node = TreeNode("child" + str(i))
        tree.current.add_child(node)

    i = 5
    for child in tree.root.children:
        tree.current = child
        tree.current.add_child(TreeNode("child's child" + str(i)))
        i += 1

    tree.preorder(print)
