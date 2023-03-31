"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional, Union

WIDTH = 800
HEIGHT = 600


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.
        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.
        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.
        Set this tree as the parent for each of its subtrees.
        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        self._expanded = False

        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        if self._is_leaf():
            self.data_size = data_size
        else:
            self.data_size = 0
            for subtree in self._subtrees:
                self.data_size += subtree.data_size
                subtree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        else:
            self.rect = rect

        if not self._is_leaf():
            x, y, w, h = rect;
            max_x, max_y = w, h
            if w > h:
                a = 0
                for subtree in self._subtrees[:-1]:
                    ratio = self._check(subtree)
                    subtree.update_rectangles((x + a, y,
                                               math.floor(ratio * w), h))
                    a += subtree.rect[2]
                self._subtrees[-1].update_rectangles((x + a, y,
                                                      max_x - a, max_y))
            else:
                b = 0
                for subtree in self._subtrees[:-1]:
                    ratio = self._check(subtree)
                    subtree.update_rectangles((x, y + b,
                                               w, math.floor(ratio * h)))
                    b += subtree.rect[3]
                self._subtrees[-1].update_rectangles((x, y + b,
                                                      max_x, max_y - b))

    def _check(self, subtree: TMTree) -> float:
        """Check if self size is 0
        """
        if self.data_size == 0:
            return 0.0
        return subtree.data_size / self.data_size

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0:
            return []

        if not self._expanded:
            return [(self.rect, self._colour)]
        else:
            if self._is_leaf():
                return [(self.rect, self._colour)]

            r = []
            for subtree in self._subtrees:
                r.extend(subtree.get_rectangles())
            return r

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.
        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if pos > (WIDTH, HEIGHT) or self.is_empty() or not self._includes(pos):
            return None

        if not (self._expanded and self._subtrees):
            return self

        result = None
        for sub in self._subtrees:
            x = sub.get_tree_at_position(pos)
            if x:
                if not result or ((x.rect[0] < result.rect[0]) or
                                  (x.rect[1] < result.rect[1])):
                    result = x
        return result

    def _includes(self, pos: Tuple[int, int]) -> bool:
        return (self.rect[0] <= pos[0] <= (self.rect[0] + self.rect[2]) and
                self.rect[1] <= pos[1] <= (self.rect[1] + self.rect[3]))

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.
        If this tree is a leaf, return its size unchanged.
        """
        if self._is_leaf():
            return self.data_size

        r = 0

        for subtree in self._subtrees:
            r += subtree.update_data_sizes()

        self.data_size = r
        return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._movable(destination):
            item = self
            if self._parent_tree:
                self._parent_tree._subtrees.remove(item)

                if not self._parent_tree._subtrees:
                    self._parent_tree.data_size = 0
                self._parent_tree.update_data_sizes()

            destination._subtrees.append(item)
            item._parent_tree = destination
            destination.update_data_sizes()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._is_leaf():
            change = factor * self.data_size
            if change > 0:
                self.data_size += math.ceil(change)
            else:
                if self.data_size + math.floor(change) <= 1:
                    self.data_size = 1
                else:
                    self.data_size += math.floor(change)

            if not self._is_root():
                self._parent_tree.update_data_sizes()

    def expand(self) -> None:
        """Expand the file."""
        if not self._subtrees:
            return
        self._expanded = True
        item = self
        while item:
            item._expanded = True
            item = item._parent_tree

    def expand_all(self) -> None:
        """Expand all files."""
        if self._subtrees:
            self._expanded = True
            for sub in self._subtrees:
                sub.expand_all()

    def collapse(self) -> None:
        """Unexpanded the file.
        """
        if self._parent_tree:
            self._parent_tree._real_collapse()

    def collapse_all(self) -> None:
        """Unexpanded all files.
        """
        if self._parent_tree:
            r = self
            while r._parent_tree:
                r = r._parent_tree
            r._real_collapse()

    def _movable(self, destination: TMTree) -> bool:
        return self._is_leaf() and not destination._is_leaf()

    def _real_collapse(self) -> None:
        """Helper for collapse.
        """
        self._expanded = False
        for sub in self._subtrees:
            sub._real_collapse()

    def _is_root(self) -> bool:
        return not self._parent_tree

    def _is_leaf(self) -> bool:
        return not self._subtrees

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        subtrees = []
        name = os.path.basename(path)

        if os.path.isdir(path):
            dirs = os.listdir(path)
            for file in dirs:
                sub_path = os.path.join(path, file)
                subtree = FileSystemTree(sub_path)
                subtrees.append(subtree)

        TMTree.__init__(self, name, subtrees, os.path.getsize(path))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
    # import doctest
    #
    # doctest.testmod()