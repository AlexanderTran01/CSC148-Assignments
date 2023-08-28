from typing import List

def more(m: int) -> int:
    return m + 2

def other(lst: List[int]) -> int:
    return sum(lst)

def that(lst: List[int]) -> float:
    try:
        temp1 = more(lst[0])
        temp2 = other(lst)
        return temp1 / temp2
    except ZeroDivisionError:
        print ('Ouch')
        return -1.0

def this(lst: List[int]) -> bool:
    return that(lst) > 0

if __name__ == '__main__':
    print(this([5, 10, 15, -30]))
