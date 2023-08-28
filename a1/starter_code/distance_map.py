"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple


class DistanceMap:
    """Stores the distance between any two cities

    === Private Attributes ===
    _distance_dict:
      A dictionary mapping a pair of cities to the distance from the first to
      the second
    """
    _distance_dict: Dict[Tuple[str, str], int]

    def __init__(self) -> None:
        """Initialize this DistanceMap with an empty _distance_dict

        >>> dm = DistanceMap()
        >>> dm._distance_dict == {}
        True
        """
        self._distance_dict = {}

    def distance(self, city1: str, city2: str) -> int:
        """Returns the distance from city1 to city2, or -1 if the distance is
        not stored in the distance map

        >>> d = DistanceMap()
        >>> d._distance_dict = {('Toronto', 'London'):154}
        >>> distance = d.distance('Toronto', 'London')
        >>> distance == 154
        True
        """
        if (city1, city2) in self._distance_dict:
            return self._distance_dict[(city1, city2)]
        return -1

    def add_distance(self, city1: str, city2: str, distance1: int, distance2:
                     int = 'Not Specified') -> None:
        """Adds a new entry to _distance_dict mapping (city1, city2) to
        distance1 and (city2, city1) to distance2
        >>> d = DistanceMap()
        >>> d._distance_dict == {}
        True
        >>> d.add_distance('Toronto', 'Hamilton', 9)
        >>> d._distance_dict[('Toronto', 'Hamilton')] == 9
        True
        >>> d._distance_dict[('Hamilton', 'Toronto')] == 9
        True
        """
        self._distance_dict[(city1, city2)] = distance1
        if distance2 == 'Not Specified':
            self._distance_dict[(city2, city1)] = distance1
        else:
            self._distance_dict[(city2, city1)] = distance2


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
