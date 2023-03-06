"""CSC148 Prep 7: Recursion

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu and Diane Horton

=== Module description ===
This module contains sample tests for Prep 7.

Complete the TODO in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from prep7 import num_positives, nested_max, max_length



# Below are provided sample test cases for your use. You are encouraged
# to add additional test cases (in addition to the ones required above.)
# WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
# Add your own to practice writing tests and to be confident your code is
# correct.

# num_positives
def test_num_positives_doctest_example() -> None:
    """Test num_positive on one of the given doctest examples."""
    assert num_positives([1, -2, [-10, 2, [3], 4, -5], 4]) == 5

def test_num_positives_with_an_int()-> None:
    """Test num_positive on an int."""
    assert num_positives(1) == 1

def test_num_positives_with_an_empty_list()-> None:
    """Test num_positive on an emtpy list."""
    assert num_positives([]) == 0

def test_num_positives_with_a_nested_list_with_only_integers()-> None:
    """Test num_positive on a nested list with only integers."""
    assert num_positives([1, 2, 3, 4, 5]) == 5

def test_num_positives_with_only_empty_lists()-> None:
    """Test num_positive with only empty lists."""
    assert num_positives([[], [[]], [], []]) == 0

def test_num_positives_with_only_negative_int()-> None:
    """Test num_positive with only negative integers."""
    assert num_positives([-1, [-2, -3], [-10, [-9]], [-5], [-100]]) == 0

def test_num_positives_complex() -> None:
    """Test num_positives on a complex example."""
    assert num_positives([1, [2, 3], [9, 2 ,0, [1, 2, 3, 4, 5]]]) == 10

# nested_max
def test_nested_max_doctest_example() -> None:
    """Test nested_max on one of the given doctest examples."""
    assert nested_max([1, 2, [1, 2, [3], 4, 5], 4]) == 5

def test_nested_max_with_an_int() -> None:
    """Test nested_max with an integer."""
    assert nested_max(1) == 1

def test_nested_max_with_an_empty_list() -> None:
    """Test nested_max with an empty list."""
    assert nested_max([]) == 0

def test_nested_max_with_a_nested_list_with_only_int() -> None:
    """Test nested_max with a nested list with only integers."""
    assert nested_max([-1, 3, 11, 99, -5]) == 99

def test_nested_max_with_only_empty_lists()-> None:
    """Test nested_max with only empty lists."""
    assert nested_max([[], [[]], [], []]) == 0

def test_nested_max_complex() -> None:
    """Test nested_max on a complex example."""
    assert nested_max([1, [2, 3], [9, 2 ,0, [1, 2, 3, 4, 5]]]) == 9

# max_length
def test_max_length_doctest_example() -> None:
    """Test max_length on one of the given doctest examples."""
    assert max_length([1, 2, [1, 2], 4]) == 4

def test_max_length_on_an_int() -> None:
    """Test max_length with an integer."""
    assert max_length([1]) == 1

def test_max_length_on_an_empty_list() -> None:
    """Test max_length on an empty list."""
    assert max_length([]) == 0

def test_max_length_on_a_nested_list_containing_only_integers() -> None:
    """Test max_length on a nested list with only integers."""
    assert max_length([1, 2, 3, 4, 5]) == 5

def test_max_length_on_only_empty_lists()-> None:
    """Test max_length with only empty lists."""
    assert nested_max([[], [[]], [], []]) == 0

def test_max_length_complex() -> None:
    """Test max_length on a complex example."""
    assert max_length([1, [2, 3], [9, 2 ,0, [1, 2, 3, 4, 5]]]) == 5


if __name__ == '__main__':
    import pytest
    pytest.main(['prep7_starter_tests.py'])
