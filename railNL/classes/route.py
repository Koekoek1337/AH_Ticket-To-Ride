from typing import List, Tuple, Any
from station import Station

class Route:
    """
    TODO
    Route object that tracks rail connections between stations
    """

    def __init__(self, id: int):
        """
        Initializer function
        """
        self.id = id
        self.stations: List[Station] = []

    def addConnection(self, station: Station, position: int = -1) -> bool:
        """
        Adds a rail connection at the specified position (0 for start, -1 for end)
        """
        if position in [0, -1] and not \
            self.stations[position].hasConnection(self.stations[position].name()):
            return False
        
        if position > 0 and not self.stations[position].hasConnection(self.stations[position-1].name()):
            return False
        
        if position < 0 and not self.stations[position].hasConnection(self.stations[position+1].name()):
            return False

        self.stations.insert(position, station)


    def length(self) -> int:
        """
        Returns amount of connections in the route
        """
        return len(self.stations)

    def listStations(self) -> List[str]:
        """
        returns a list of station names
        """
        return [station.name() for station in self.stations]

    def brokenConnections(self) -> List[Tuple[str,str]]:
        """Returns a list of all nonexistent rail connections"""
        missing = []
        for index in range(len(self.stations - 1)):
            if not self.stations[index].hasConnection(self.stations[index + 1].name()):
                missing.append[(self.stations[index].name(), self.stations[index + 1].name())]
        
        return missing

    def duration(self) -> int:
        """
        Returns the total duration of the route
        """
        totalDuration = 0

        for index in range(len(self.stations - 1)):
            if self.stations[index].hasConnection(self.stations[index].name()):
                totalDuration += self.stations[index].connectionDuration(self.stations[index].name())
        
        return totalDuration