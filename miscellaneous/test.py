from __future__ import annotations
from typing import Optional, Any
from objprint import op



class Tree:
    """A recursive tree data structure.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: list[Tree]
    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    # This setting of attributes represents an empty tree.
    #
    # Note: self._subtrees may be empty when self._root is not None.
    # This setting of attributes represents a tree consisting of just one
    # node.


    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.
        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def leaves(self) -> list:
        """Return a list of all of the leaf items in the tree.
        """
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [self._root]
        else:
            output = []
            for subtree in self._subtrees:
                output.extend(subtree.leaves())
            return output

    def average(self) -> float:
        """Return the average of all the values in this tree.
        Return 0.0 if this tree is empty.
        
        Precondition: this is a tree of numbers.
        """
        if self.is_empty():
            return 0.0
        total, count = self._average_helper()

        return total / count

    def _average_helper(self) -> Tuple[int, int]:
        """
        Precondition: This tree is not empty.

        >>> tree = Tree(1, [Tree(2, []), Tree(3, [])])
        """
        tree_total = self._root     
        tree_count = 1
        for subtree in self._subtrees:
            subtree_total, subtree_count = subtree._average_helper()            
            tree_total += subtree_total
            tree_count += subtree_count
        return tree_total, tree_count

    def delete_item(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Return True if <item> was deleted, and False otherwise.
        Do not modify this tree if it does not contain <item>.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t.delete_item(4)
        True
        >>> print(t)
        2
          5
        <BLANKLINE>
        >>> t.delete_item(5)
        True
        >>> print(t)
        2
        <BLANKLINE>
        >>> t.delete_item(2)
        True
        >>> t.is_empty()
        True
        """
        if self.is_empty():
            return False  # item isn’t in the tree
        elif self._root == item:
            self._delete_root()
            return True  # item was deleted
        else:
            for subtree in self._subtrees:
                if subtree.delete_item(item):
                    if subtree.is_empty():
                        self._subtrees.remove(subtree)
                    return True

            return False

    def _delete_root(self) -> None:
        """Remove the root of this tree.
        Precondition: this tree is not empty.
        """
        # Base case: if it's a leaf
        if self._subtrees == []:
            self._root = None
        else:
            # Strategy 1: Promote a subtree
            # subtree_to_promote = self._subtrees[-1]
            # self._root = subtree_to_promote._root
            # self._subtrees.extend(subtree_to_promote._subtrees)
            # self._subtrees.remove(subtree_to_promote)

            # self = subtree_to_promote # This won't work! self is just a variable name

            # Strategy 2: Swap with a leaf.
            leaf = self._extract_leaf()
            self._root = leaf


    def _extract_leaf(self) -> Any:
        """Remove and return the leftmost leaf in a tree.

        Precondition: this tree is non-empty.
        Tree(2, [Tree(4, [Tree(6, [])]), Tree(5, [])])
        """
        if self._subtrees[0]._subtrees == []:
            leaf_value = self._subtrees[0]._root
            self._subtrees.pop(0)
            return leaf_value
        else:
            subtree_to_extract_from = self._subtrees[0]
            return subtree_to_extract_from._extract_leaf()

    def to_nested_list(self) -> list[Any]:
        if self.is_empty():
            return []
        else:
            output = [self._root]
            for subtree in self._subtrees:
                output.append(subtree.to_nested_list())
            return output

    def __eq__(self, other: Tree) -> bool:
        """Return whether <self> and <other> are equal.
        """
        if self.is_empty() and other.is_empty():
            return True
        elif self.is_empty() or other.is_empty():
            return False
        else:
            if self._root != other._root:
                return False

            if len(self._subtrees) != len(other._subtrees):
                return False

            return self._subtrees == other._subtrees


def to_tree(obj) -> Tree:
    """
    >>> [10, [2], [3, [4], [5]]]
    """
    if isinstance(obj, int):
        return None
    else:
        if len(obj) == 0:
            return Tree(None, [])
        root = obj[0]
        if isinstance(root, list):
            return None

        subtrees = []
        for sublist in obj[1:]:
            subtree = to_tree(sublist)
            if subtree is None:
                return None
            subtrees.append(subtree)
        return Tree(root, subtrees)



if __name__ == '__main__':
    # obj = Tree(10, [Tree(2, []), Tree(3, [Tree(4, []), Tree(5, [])])])
    # print(obj.to_nested_list())
    lst = [10, [2], [3, [4], [5]]]
    op(to_tree(lst))

