from test import moves_to_nested_dict


def test_1():
    lst = [["a", "b", "c"], ["a", "b"], ["d", "e"], ["d", "e"]]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 0): {('b', 1): {('c', 1): {}}}, ('d', 0): {('e', 2): {}}}

def test_2():
    lst = [["a", "b", "c"], ["a", "b"], ["d", "e", "a"], ["d", "e"]]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 0): {('b', 1): {('c', 1): {}}}, ('d', 0): {('e', 1): {('a', 1): {}}}}

def test_3():
    lst = [["a", "b", "c", 'e'], ["a", "b"], ["d", "e"], ["d", "e"], ['a', 'b', 'd', 'c']]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 0): {('b', 1): {('c', 0): {('e', 1): {}},('d', 0): {('c', 1): {}}}},('d', 0): {('e', 2): {}}}

def test_4():
    lst = [["a", "b", "c"], ["a", "d", "c"]]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 0): {('b', 0): {('c', 1): {}}, ('d', 0): {('c', 1): {}}}}

def test_5():
    lst = [['a', 'b', 'd'], ['b', 'e'], ['c', 'f', 'e', 'b'], ['e', 'd'], ['f', 'a']]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 0): {('b', 0): {('d', 1): {}}},('b', 0): {('e', 1): {}},('c', 0): {('f', 0): {('e', 0): {('b', 1): {}}}},('e', 0): {('d', 1): {}},('f', 0): {('a', 1): {}}}

def test_6():
    lst = [['a'], ['b'], ['c']]
    result = moves_to_nested_dict(lst)
    assert result == {('a', 1): {}, ('b', 1): {}, ('c', 1): {}}

# def test_7():
#     lst = [["a", "b", "c"], ["a", "b"], ["d", "e"], ["d", "e"]]
#     result = moves_to_nested_dict(lst)
#     assert result == {('a', 0): {('b', 0): {('c', 1): {}}}}


if __name__ == '__main__':
    import pytest
    pytest.main(['test2.py'])

