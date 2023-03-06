from typing import Union, Optional

def buyable(n: int) -> bool:
    """Return whether one can buy exactly <n> McNuggets.
    McNuggets come in packs of 4, 6, or 25.  It is
    considered possible to buy exactly 0 McNuggets.
    Precondition: n >= 0
    >>> buyable(0)
    True
    >>> buyable(4)
    True
    >>> buyable(6)
    True
    >>> buyable(25)
    True
    >>> buyable(35) # 25 + 6 + 4
    True
    >>> buyable(66) # 25 + 25 + 6 + 6 + 4
    True
    >>> buyable(5)
    False
    >>> buyable(13)
    False
    """
    if n == 0:
        return True
    for num in (25, 6, 4):
        if n >= num and buyable(n - num):
            return True
    return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()