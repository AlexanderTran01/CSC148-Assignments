"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """A parcel object

    === Public Attributes ===
    id:
    A parcel ID that is unique to a single parcel.
    volume:
    The volume of the parcel, measured in units of cubic centimetres.
    source:
    The name of the city where the parcel came from
    destination:
    The name of the city where the parcel must be delivered to

    === Representation Invariants ===
    - self._volume > 0
    """
    id: int
    volume: int
    source: str
    destination: str

    def __init__(self, _id: int, volume: int, source: str, destination: str) ->\
            None:
        """Initialize this Parcel

        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> p1.id == 1
        True
        >>> p1.volume == 5
        True
        >>> p1.source == 'Buffalo'
        True
        >>> p1.destination == 'Hamilton'
        True
        """
        self.id = _id
        self.volume = volume
        self.source = source
        self.destination = destination


class Truck:
    """Creates a truck object

    === Public Attributes ===
    id:
    A truck ID that is unique to a single truck.
    capacity:
    The volume capacity of the truck, measured in units of cubic centimetres.
    parcels:
    A list of parcels that are packed onto this truck.
    route:
    An ordered list of cities that this truck is scheduled to travel through.
    """
    id: int
    capacity: int
    parcels: List[Parcel]
    route: List[str]

    def __init__(self, _id: int, capacity: int, depot: str) -> None:
        """Initialize this Parcel.

        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.id == 1423
        True
        >>> t1.capacity == 10
        True
        >>> t1.fullness()
        0.0
        >>> len(t1.parcels) == 0
        True
        >>> t1.route == ['Toronto']
        True
        """

        self.id = _id
        self.capacity = capacity
        self.parcels = []
        self.route = [depot]

    def pack(self, parcel: Parcel) -> bool:
        """Packs a parcel onto this truck

        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.fullness()
        50.0
        >>> len(t1.parcels) == 1
        True
        >>> t1.route == ['Toronto', 'Hamilton']
        True
        """
        unused_space = self.capacity
        for p in self.parcels:
            unused_space -= p.volume
        if unused_space >= parcel.volume:
            self.parcels.append(parcel)
            if self.route[-1] != parcel.destination:
                self.route.append(parcel.destination)
            return True
        return False

    def fullness(self) -> float:
        """Returns the percentage of the truck's capacity that is occupied by
        parcels.

        Precondition: The sum of the volumes of the parcels packed onto this
        truck is not greater than this truck's capacity.
        """
        total_parcel_volume = 0.0
        for parcel in self.parcels:
            total_parcel_volume += parcel.volume
        return float(total_parcel_volume * 100.0 / self.capacity)


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add truck to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        to_return = ''
        template = 'ID: {id}, Capacity: {capacity}, Fullness: {fullness}, \
                   Route: {route}'
        for truck in self.trucks:
            route = ''
            for city in truck.route:
                if city != truck.route[-1]:
                    route += str(city) + ' '
                else:
                    route += str(city)
            if truck != self.trucks[-1]:
                to_return += template.format(truck.id, truck.capacity,
                                             truck.fullness(), route) + '\n'
            else:
                to_return += template.format(truck.id, truck.capacity,
                                             truck.fullness(), route)
        return to_return

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        counter = 0
        for truck in self.trucks:
            if truck.fullness() > 0.0:
                counter += 1
        return counter

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        parcel_allocations = {}
        for truck in self.trucks:
            for parcel in truck.parcels:
                if truck.id in parcel_allocations:
                    parcel_allocations[truck.id].append(parcel.id)
                else:
                    parcel_allocations[truck.id] = [parcel.id]
        return parcel_allocations

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        total_unused_space = 0
        for truck in self.trucks:
            if truck.fullness() > 0.0:
                unused_space = truck.capacity
                for parcel in truck.parcels:
                    unused_space -= parcel.volume
                total_unused_space += unused_space
        return total_unused_space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.0

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        total_fullness = 0.0
        for truck in self.trucks:
            if truck.fullness() > 0.0:
                total_fullness += truck.fullness()
        return float(total_fullness)

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        if self.num_nonempty_trucks() == 0:
            return 0.0
        return float(self._total_fullness() / self.num_nonempty_trucks())

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        total_distance_travelled = 0
        for truck in self.trucks:
            for i in range(len(truck.route)):
                if i != len(truck.route) - 1:
                    distance_travelled = dmap.distance(truck.route[i],
                                                       truck.route[i + 1])
                    total_distance_travelled += distance_travelled
            if truck.route[-1] != truck.route[0]:
                distance_travelled = dmap.distance(truck.route[-1],
                                                   truck.route[0])
                total_distance_travelled += distance_travelled
        return int(total_distance_travelled)

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        travelled_trucks = 0
        for truck in self.trucks:
            if len(truck.route) > 1:
                travelled_trucks += 1
        if travelled_trucks == 0:
            return 0.0
        return float(self.total_distance_travelled(dmap) / travelled_trucks)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
