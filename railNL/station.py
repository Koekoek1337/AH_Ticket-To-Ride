from typing import List, Tuple, Dict

class Station:
    """
    Station object for a rail network

    Attributes:
        name (str): The name of the station
        position (Tuple[float, float]): The x and y coordinates of the station.
        Connections (Dict[str, Tuple[Station, int]]): Connected stations and the time the rail
            connection takes keyed by station name.
    """

    def __init__(self, name: str, x: float, y: float):
        """Initializer function"""

        self._name = name
        self._position = (x, y)
        self._connections: Dict[str, Tuple["Station", int]] = dict()

    def name(self) -> str:
        """Returns the name of the station"""

        return self._name
    
    def position(self) -> tuple(float, float):
        """Returns the position of the station"""

        return self._position

    def addConnection(self, otherStation: "Station", duration: int) -> None:
        """Adds a connection to station with a duration"""

        self._connections[otherStation.name()] = (otherStation, duration)
    
    def removeConnection(self, stationName: str) -> None:
        """Removes a station from connections"""
        
        self._connections.pop(stationName)

    def connectionAmount(self) -> int: 
        return len(self._connections)

    def listConnections(self) -> List[Tuple(str, int, int)]:
        """
        Returns (List[Tuple[str, int, int]]) name, duration and connections of connecting stations
        """
        return [(key, duration, station.connectionAmount()) for key, (station, duration)  in self._connections.items()]
    
    def hasConnection(self, stationName: str) -> bool:
        """Returns True if the station is connected to the station with stationName, else False."""
        return stationName in self.listConnections()

    def getConnectedStation(self, stationName: str):
        """returns the station object of a connected station."""
        return self._connections[stationName][0]

    def connectionDuration(self, stationName: str) -> int:
        """Returns the duration of the connection"""
        return self._connections[stationName][1]