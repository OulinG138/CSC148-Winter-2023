"""CSC148 Lab 1

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search


def test_search() -> None:
    """Simple test for binary_search."""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 5) == 1

"""
- have a double check that the conditions (no duplicates) are met
- test empty list
- test list of length 1
- test if the first element is the target
- test if the last element is the target
- test if the middle element is the target
- test that 01 is returned if the element isn't there
"""

if __name__ == '__main__':
    import pytest
    pytest.main(['test_search.py'])
