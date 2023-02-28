from typing import Union

def max_length(obj: Union[int, list]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, 1, 2, 4])
    5
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    else:
        length_list = [len(obj)]
        for sublist in obj:
            length_list.append(max_length(sublist))
        return max(length_list)
    

if __name__ == '__main__':
    print(max_length([1, 2, [1, 2, [3], 4, 5], 4]))
