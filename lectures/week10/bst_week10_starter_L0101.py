"""
Extra practice with BSTs.
"""
from __future__ import annotations

import math
from typing import Any, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every item, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return whether this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        else:
            return max(self._left.height(), self._right.height()) + 1

    # -------------------------------------------------------------------------
    # Standard Container methods (search, insert, delete [copy from last week])
    # -------------------------------------------------------------------------
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left  # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    def insert(self, item: Any) -> None:
        """Insert <item> into this tree.

        Do not change positions of any other values.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf.
            # Note that self._left and self._right cannot be None when the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = type(self)(None)
            self._right = type(self)(None)
        elif item <= self._root:  # this version always inserts equals in left.
            self._left.insert(item)
        else:
            self._right.insert(item)

    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    #######################
    # TODO: implement copy according to its docstring
    def copy(self, new_root: BinarySearchTree) -> None:
        """
        Recursively copy self into <new_root>.

        Precondition:
        new_root is an empty BinarySearchTree

        # a small example
        >>> bst = BinarySearchTree(7)
        >>> copy_bst = BinarySearchTree(None)
        >>> bst.copy(copy_bst)
        >>> copy_bst._root == 7
        True
        >>> copy_bst is bst
        False

        # a slightly larger example
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> copy_bst = BinarySearchTree(None)
        >>> bst.copy(copy_bst)


        # ensure that copy_bst contains all the values
        >>> copy_bst._left._root == 3
        True
        >>> copy_bst._left._left._root == 2
        True
        >>> copy_bst._root == 7
        True
        >>> copy_bst._right.is_empty()
        True
        >>> copy_bst._left._right._root == 5
        True
        """
        # TODO: implement me!
        if self.is_empty():
            return
        new_root._root = self._root
        new_root._left = BinarySearchTree(None)
        new_root._right = BinarySearchTree(None)

        self._left.copy(new_root._left)
        # below is the last bit of code we didn't
        # get to in lecture
        self._right.copy(new_root._right)

    # TODO: specify the preconditions so that the update method is correct.
    # We'll take this up on Thursday
    def update(self, items: list[Any]) -> None:
        """
        Update the BST so that it contains EVERY item in <items>
        by replacing the existing values in <self>.

        <items> is mutated by this method.

        Preconditions:

        items should be sorted from largest to smallest.

        len(items) == len(self)


        TODO: specify the preconditions so that this method is correct.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> print(bst)
        7
          3
            2
            5
        <BLANKLINE>
        >>> bst.update([10, 9, 8, 7])
        >>> print(bst)
        10
          8
            7
            9
        <BLANKLINE>
        """
        self._update(items)

    def _update(self, items: list[Any]) -> None:
        """See the docstring for the update method."""
        if self.is_empty():
            return
        self._left._update(items)
        self._root = items.pop()  # in order, so what do we know about items?
        self._right._update(items)

    # NEW: posted code for rotate_left from lab, which
    #      we sketched out on the slides during lecture
    def rotate_left(self) -> None:
        """
        See lab for the complete docstring. Note,
        in class we were just assuming the general structure shown,
        so you _may_ need other checks if you can't assume certain
        things about the tree structure in the original code provided.
        """
        # the approach we take is to first construct a new
        # left BST from scratch, then update self's attributes.
        left = BinarySearchTree(None)
        left._root = self._root
        left._left = self._left
        left._right = self._right._left

        self._left = left
        self._root = self._right._root
        self._right = self._right._right


####################

def check_height(values: list) -> bool:
    """
    Return whether the BST constructed by inserting all of <values> into an
    originally empty BST has the minimum possible height.
    """
    n = len(values)
    min_height = math.ceil(math.log2(n + 1))
    height = make_bst(values).height()
    return height == min_height


def make_bst(values: list) -> BinarySearchTree:
    """
    Return a BST constructed by inserting the items from <values> into an
    empty BST in the order they occur in <values>
    """
    bst = BinarySearchTree(None)
    for v in values:
        bst.insert(v)
    return bst


def balanced_bst_order(n: int) -> list[int]:
    """Return a list of <n> integers, such that inserting them in that order
    will create a balanced BST.

    >>> balanced_bst_order(0)
    []
    >>> balanced_bst_order(1)
    [1]
    >>> balanced_bst_order(2)
    [2, 1]
    >>> balanced_bst_order(3)
    [2, 1, 3]
    >>> balanced_bst_order(7)
    [4, 2, 1, 3, 6, 5, 7]
    """
    # TODO complete me!

    if n == 0:
        return []
    if n == 1:
        return [1]

    # n > 1
    # find the middle
    # for each half, recursively create the list
    num_left = n // 2

    num_right = n - n // 2 - 1

    root = num_left + 1

    # after class sanity check for n=2 and n=3
    # n = 2:
    # num_left = 1
    # num_right = 2 - 1 - 1 = 0
    # root = 2
    # so we will end up with [2] + [1] + []

    # n = 3:
    # num_left = 1
    # num_right = 3 - 1 - 1 = 1
    # root = 2
    # so we will end up with [2] + [1] + [3]

    left = balanced_bst_order(num_left)

    # as we noted in class, we need to "+ root"
    # to the result of the below recursive call, in order
    # to get the values in the range that we want!
    right = balanced_bst_order(num_right)
    fixed_right = []
    for item in right:
        fixed_right.append(item + root)

    return [root] + left + fixed_right
    # note, we could do [root] + fixed_right + left, but
    # that would fail our provided docstring examples. The resulting
    # BST would be correct otherwise though.
    # side note during lecture: ensure makes sense for odd n


if __name__ == '__main__':

    # confirm that balanced_bst_order works for a range of values of n
    for i in range(32):
        order = balanced_bst_order(i)
        assert len(order) == i
        assert check_height(order)

    import doctest

    doctest.testmod()
