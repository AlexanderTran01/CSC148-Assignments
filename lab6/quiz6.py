"""
Below is an implementation of the recursive function count_odd which operates
on a nested list. This implementation has a bug which you'll fix in Task 3.

Your tasks are listed below.
    1.  Identify the three recursive calls that are made when we call
        count_odd([1, [2, 6, 5], [9, [8, 7]]])

        In the doctest of count_odd, replace the ...s with the recursive
        calls that are made, along with what we expect this to return.

    2.  In the doctest of count_odd, fill in the expected result of the call
        count_odd([1, [2, 6, 5], [9, [8, 7]]])

    3.  Currently, count_odd has a bug in it. Find the bug and fix it.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
from typing import Union, List


def count_odd(obj: Union[int, List]) -> int:
    """Return the number of odd numbers in <obj>.

          e.g. if the first recursive call was made to the value 15, then
               you would replace the ... to have
               call_1 = 15

    >>> call_1 = 1
    >>> actual_1 = count_odd(call_1)
    >>> expected_1 = 1
    >>> expected_1 == actual_1
    True
    >>> call_2 = [2, 6, 5]
    >>> actual_2 = count_odd(call_2)
    >>> expected_2 = 1
    >>> expected_2 == actual_2
    True
    >>> call_3 = [9, [8, 7]]
    >>> actual_3 = count_odd(call_3)
    >>> expected_3 = 2
    >>> expected_3 == actual_3
    True
    >>> actual = count_odd([1, [2, 6, 5], [9, [8, 7]]])
    >>> expected = 4
    >>> actual == expected
    True
    """
    total = 0
    if isinstance(obj, int):
        if obj % 2 == 0:
            return 0
        else:
            return 1
    else:
        for sublist in obj:
            total += count_odd(sublist)
    return total


if __name__ == '__main__':
    import doctest
    doctest.testmod()
