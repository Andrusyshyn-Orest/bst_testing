"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, value):
        """
        Adds value to the tree.
        """

        if self.isEmpty():
            self._root = BSTNode(value)
            self._size += 1
            return

        curr_node = self._root
        while True:
            if value < curr_node.data:
                if curr_node.left is None:
                    curr_node.left = BSTNode(value)
                    self._size += 1
                    break
                else:
                    curr_node = curr_node.left

            else:
                if curr_node.right is None:
                    curr_node.right = BSTNode(value)
                    self._size += 1
                    break
                else:
                    curr_node = curr_node.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(top):
                return 0
            else:
                return 1 + max(height1(child) for child in self.children(top))

        if self.isEmpty():
            return 0

        return height1(self._root)

    def is_leaf(self, node):
        """
        Checks if node is leaf.
        """
        return (node.left is None) and (node.right is None)

    def children(self, node):
        """
        """
        children = []
        if node.left is not None:
            children.append(node.left)
        if node.right is not None:
            children.append(node.right)

        return iter(children)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < (2*log(len(self) + 1, 2) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        elements = set()
        for element in self:
            if low <= element <= high:
                elements.add(element)
        return list(elements)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        elements = []
        for element in self.inorder():
            elements.append(element)
        self.clear()
        self._make_balanced_tree(elements)

    def _make_balanced_tree(self, elements):
        """
        Make balanced trees from elements.
        """
        if len(elements) == 1:
            return elements[0]

        if len(elements) == 0:
            return None

        middle = len(elements)//2

        element = elements[middle]
        self.add(element)
        elements_first_half = elements[:middle]
        elements_second_half = elements[middle + 1:]
        item1 = self._make_balanced_tree(elements_first_half)
        if item1 is not None:
            self.add(item1)

        item2 = self._make_balanced_tree(elements_second_half)
        if item2 is not None:
            self.add(item2)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        if self.isEmpty():
            return None

        curr_node = self._root
        curr_min = None

        while True:
            if curr_node.data <= item:
                if curr_node.right is None:
                    break
                else:
                    curr_node = curr_node.right
            else:
                curr_min = curr_node.data
                if curr_node.left is None:
                    break
                else:
                    curr_node = curr_node.left

        return curr_min

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        if item not in self:
            return None

        if self.isEmpty():
            return None

        curr_node = self._root
        curr_max = None

        while True:
            if curr_node.data < item:
                curr_max = curr_node.data
                if curr_node.right is None:
                    break
                else:
                    curr_node = curr_node.right

            else:
                if curr_node.left is None:
                    break
                else:
                    curr_node = curr_node.left

        return curr_max

    @staticmethod
    def _read_from_dictionary(path):
        """
        Return list of words from dictionary.
        """

        words = []
        with open(path, mode='r', encoding="UTF-8") as dictionary_file:
            for word in dictionary_file:
                words.append(word.strip())

        return words

    @staticmethod
    def _choose_random_words(words_list, num):
        """
        Return list of num randow words from words_list.
        """
        return random.sample(words_list, num)

    @staticmethod
    def _list_search(words_list, search_words):
        """
        """

        for word in search_words:
            try:
                words_list.index(word)
            except ValueError:
                pass

    def _make_bst_consistent(self, words_list):
        """
        """

        self.clear()
        for word in words_list:
            self.add(word)

    def _make_bst_random(self, words_list):
        """
        """

        self.clear()
        random_order_words = random.sample(words_list, len(words_list))
        for word in random_order_words:
            self.add(word)

    def _bst_search(self, search_words):
        """
        """

        for word in search_words:
            self.find(word)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_list = self._read_from_dictionary(path)
        search_words = self._choose_random_words(words_list, 10000)
        start = time.time()
        self._list_search(words_list[:900], search_words)
        time1 = time.time() - start

        self._make_bst_consistent(words_list[:900])
        start = time.time()
        self._bst_search(search_words)
        time2 = time.time() - start

        self._make_bst_random(words_list[:900])
        start = time.time()
        self._bst_search(search_words)
        time3 = time.time() - start

        self.rebalance()
        start = time.time()
        self._bst_search(search_words)
        time4 = time.time() - start

        print(f"""
List search: {time1}
Consistent BST search: {time2}
Random BST search: {time3}
Balanced BST search: {time4}""")


if __name__ == "__main__":
    tree = LinkedBST()
    tree.demo_bst("words.txt")
