"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Union
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


def _more_space(truck1: Truck, truck2: Truck) -> bool:
    """Return True if truck1 has more space than truck2.

    >>> t1 = Truck(1423, 2, 'Toronto')
    >>> t2 = Truck(1424, 7, 'Toronto')
    >>> _more_space(t1, t2)
    False
    >>> _more_space(t2, t1)
    True
    """
    unused_space1 = truck1.capacity
    for parcel in truck1.parcels:
        unused_space1 -= parcel.volume
    unused_space2 = truck2.capacity
    for parcel in truck2.parcels:
        unused_space2 -= parcel.volume
    return unused_space1 > unused_space2


def _less_space(truck1: Truck, truck2: Truck) -> bool:
    """Return True if truck1 has less space than truck2.

    >>> t1 = Truck(1423, 2, 'Toronto')
    >>> t2 = Truck(1424, 7, 'Toronto')
    >>> _less_space(t1, t2)
    True
    >>> _less_space(t2, t1)
    False
    """
    unused_space1 = truck1.capacity
    for parcel in truck1.parcels:
        unused_space1 -= parcel.volume
    unused_space2 = truck2.capacity
    for parcel in truck2.parcels:
        unused_space2 -= parcel.volume
    return unused_space1 < unused_space2


def _larger_parcel(parcel1: Parcel, parcel2: Parcel) -> bool:
    """Return True if parcel1's volume is larger than parcel2' volume.

    >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    >>> p2 = Parcel(12, 6, 'Toronto', 'London')
    >>> _larger_parcel(p1, p2)
    False
    >>> _larger_parcel(p2, p1)
    True
    """
    return parcel1.volume > parcel2.volume


def _smaller_parcel(parcel1: Parcel, parcel2: Parcel) -> bool:
    """Return True if parcel1's volume is lesser than parcel2' volume.

    >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    >>> p2 = Parcel(12, 6, 'Toronto', 'London')
    >>> _smaller_parcel(p1, p2)
    True
    >>> _smaller_parcel(p2, p1)
    False
    """
    return parcel1.volume < parcel2.volume


def _after_destination(parcel1: Parcel, parcel2: Parcel) -> bool:
    """Return True if parcel1's destination comes after parcel2's destination,
    alphabetically.

    >>> p1 = Parcel(27, 5, 'Hamilton', 'Toronto')
    >>> p2 = Parcel(12, 5, 'Hamilton', 'London')
    >>> _after_destination(p1, p2)
    False
    >>> _after_destination(p2, p1)
    True
    """
    return parcel1.destination < parcel2.destination


def _before_destination(parcel1: Parcel, parcel2: Parcel) -> bool:
    """Return True if parcel1's destination comes before parcel2's destination,
    alphabetically.

    >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    >>> p2 = Parcel(12, 5, 'Toronto', 'London')
    >>> _before_destination(p1, p2)
    False
    >>> _before_destination(p2, p1)
    True
    """
    return parcel1.destination > parcel2.destination


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """Goes through parcels in random order. For each parcel, it will schedule
    it onto a randomly chosen truck (from among those trucks that have capacity
    to add that parcel).
    """
    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        unscheduled = []
        for parcel in parcels:
            unscheduled.append(parcel)
        shuffle(unscheduled)
        for parcel in unscheduled:
            available_trucks = []
            for truck in trucks:
                unused_space = truck.capacity
                for p in truck.parcels:
                    unused_space -= p.volume
                if unused_space >= parcel.volume:
                    available_trucks.append(truck)
            if len(available_trucks) != 0:
                if trucks[trucks.index(choice(available_trucks))].pack(parcel):
                    unscheduled.remove(parcel)
        return unscheduled


class GreedyScheduler(Scheduler):
    """Processes parcels one at a time, picking a truck for each, choosing
    parcels and trucks according to the configured orders.

    The greedy algorithm has two configurable features: the order in which
    parcels are considered, and how a truck is chosen for each parcel. These are
    described below.

    Parcel order
    There are four possible orders that the algorithm could use to process the
    parcels:

    In order by parcel volume, either smallest to largest (non-decreasing) or
    largest to smallest (non-increasing).
    In order by parcel destination, either smallest to largest (non-decreasing)
    or largest to smallest (non-increasing). Since destinations are strings,
    larger and smaller is determined by comparing strings (city names)
    alphabetically.
    Ties are broken using the order in which the parcels are read.

    Truck choice:
    It only considers trucks that have enough unused volume to add the parcel.
    Among these trucks, if there are any that already have the parcel’s
    destination at the end of their route, only those trucks are considered.
    Otherwise, all trucks that have enough unused volume are considered.
    Given the eligible trucks, the algorithm can be configured one of two ways
    to make a choice:
    choose the eligible truck with the most available space, or
    choose the eligible truck with the least available space
    Ties are broken using the order in which the trucks are read. If there are
    no eligible trucks, then the parcel is not scheduled onto any truck.

    === Private Attributes ===
    _parcel_priority:
        The configured priority in which parcels are chosen.
    _parcel_order:
        The configured order in which parcels are chosen.
    _truck_order:
        The configured order in which trucks are chosen.

    === Representation invariants ===
    - _parcel_priority == 'volume' or _parcel_priority == 'destination'
    - _parcel_order == 'non-decreasing' or _parcel_order == 'non-increasing'
    - _truck_order == 'non-decreasing' or _truck_order == 'non-increasing'
    """
    _parcel_priority: str
    _parcel_order: str
    _truck_order: str

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:
        """Initialize this GreedyScheduler with the given configuration.
        >>> configuration = {'parcel_priority': 'volume',\
                             'parcel_order': 'non-decreasing',\
                             'truck_order': 'non-decreasing'}
        >>> gs1 = GreedyScheduler(configuration)
        >>> gs1._parcel_priority == 'volume'
        True
        >>> gs1._parcel_order == 'non-decreasing'
        True
        >>> gs1._truck_order == 'non-decreasing'
        True
        """
        self._parcel_priority = config['parcel_priority']
        self._parcel_order = config['parcel_order']
        self._truck_order = config['truck_order']

    def _choose_truck(self, available_trucks: List[Truck],
                      available_trucks_v2: List[Truck]) -> Truck:
        """Chooses a truck among the lists of trucks according to the given
        truck order configuration

        Precondition: available_trucks contains at least one truck.

        >>> # Define a GreedyScheduler with priority on trucks with more space
        >>> configuration = {'parcel_priority': 'volume',\
                             'parcel_order': 'non-decreasing',\
                             'truck_order': 'non-decreasing'}
        >>> gs = GreedyScheduler(configuration)
        >>> t1 = Truck(1423, 2, 'Toronto')
        >>> t2 = Truck(1424, 7, 'Toronto')
        >>> t3 = Truck(1425, 5, 'Toronto')
        >>> t4 = Truck(1426, 1, 'Toronto')
        >>> at = (t1, t2, t3, t4)
        >>> at2 = (t1, t2, t3, t4)
        >>> chosen_truck = gs._choose_truck(at, at2)
        >>> chosen_truck.id == 1426
        True
        """
        if self._truck_order == 'non-decreasing':
            pq = PriorityQueue(_less_space)
            for truck in available_trucks_v2:
                pq.add(truck)
            if not pq.is_empty():
                return pq.remove()
            for truck in available_trucks:
                pq.add(truck)
            if not pq.is_empty():
                return pq.remove()
        if self._truck_order == 'non-increasing':
            pq = PriorityQueue(_more_space)
            for truck in available_trucks_v2:
                pq.add(truck)
            if not pq.is_empty():
                return pq.remove()
            for truck in available_trucks:
                pq.add(truck)
            if not pq.is_empty():
                return pq.remove()
        return None

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedules parcels onto trucks according to the given configuration.
        >>> p1 = Parcel(1, 150, 'Woodstock', 'Mississauga')
        >>> p2 = Parcel(2, 100, 'Kingston', 'Hamilton')
        >>> p3 = Parcel(3, 50, 'Oakville', 'London')
        >>> t1 = Truck(1, 50, 'York')
        >>> t2 = Truck(2, 150, 'York')
        >>> t3 = Truck(3, 100, 'York')
        >>> from domain import Fleet
        >>> f = Fleet()
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> config = {'depot_location': 'Toronto',\
                      'parcel_file': '',\
                      'truck_file': '',\
                      'map_file': '',\
                      'algorithm': 'greedy',\
                      'parcel_priority': 'volume',\
                      'parcel_order': 'non-decreasing',\
                      'truck_order': 'non-increasing',\
                      'verbose': 'false'}
        >>> scheduler = GreedyScheduler(config)
        >>> unscheduled_parcels = scheduler.schedule([p1, p2, p3],[t1, t2, t3])
        >>> unscheduled_parcels == [p1]
        True
        >>> truck_parcels = f.parcel_allocations()
        >>> truck_parcels[2] == [3, 2]
        True
        """
        unscheduled = []
        pq = []
        if self._parcel_priority == 'volume' and\
           self._parcel_order == 'non-decreasing':
            pq = PriorityQueue(_smaller_parcel)
        if self._parcel_priority == 'volume' and \
           self._parcel_order == 'non-increasing':
            pq = PriorityQueue(_larger_parcel)
        if self._parcel_priority == 'destination' and \
           self._parcel_order == 'non-decreasing':
            pq = PriorityQueue(_after_destination)
        if self._parcel_priority == 'destination' and \
           self._parcel_order == 'non-increasing':
            pq = PriorityQueue(_before_destination)
        for parcel in parcels:
            unscheduled.append(parcel)
            pq.add(parcel)
        while not pq.is_empty():
            p = pq.remove()
            available_trucks = []
            for truck in trucks:
                unused_space = truck.capacity
                for parcel in truck.parcels:
                    unused_space -= parcel.volume
                if unused_space >= p.volume:
                    available_trucks.append(truck)
            available_trucks_v2 = []
            for truck in available_trucks:
                if truck.route[-1] == p.destination:
                    available_trucks_v2.append(truck)
            if len(available_trucks) != 0:
                if trucks[trucks.index(self._choose_truck
                                       (available_trucks,
                                        available_trucks_v2))].pack(p):
                    unscheduled.remove(p)
        return unscheduled


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
