from typing import TYPE_CHECKING, List, Tuple, Dict

if TYPE_CHECKING:
    from connection import Connection

class Station:
    """
    TODO
    - Use connection object for connections

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
        self._connections: Dict[str, "Connection"] = dict()

    def __str__(self) -> str:
        return f"{self._name} station, connected to {len(self.listConnections())} other stations"

    def name(self) -> str:
        """Returns the name of the station"""

        return self._name
    
    def position(self) -> Tuple[float, float]:
        """Returns the position of the station"""
    
        return self._position

    def stationPoint(self) -> Tuple[str, Tuple[float, float]]:
        """Returns the name and position of the station"""

        return self._name, self._position

    def addConnection(self, stationName,  connection: "Connection") -> None:
        """Adds a connection to station with a duration"""

        self._connections[stationName] = connection
    
    def removeConnection(self, stationName: str) -> None:
        """Removes a station from connections"""
        
        self._connections.pop(stationName)

    def connectionAmount(self) -> int: 
        return len(self._connections)

    def listConnections(self) -> List[Tuple[str, float, int]]:
        """
        Returns (List[Tuple[str, float, int]]) name, duration and connections of connecting stations
        """
        return [(stationName, connection.duration(), connection.stationConnectionAmount(stationName)) 
                for stationName, connection  in self._connections.items()]
    
    def hasConnection(self, stationName: str) -> bool:
        """Returns True if the station is connected to the station with stationName, else False."""
        return stationName in self._connections.keys()

    def getConnectedStation(self, stationName: str):
        """returns the station object of a connected station."""
        return self._connections[stationName].getConnectedStation(stationName)

    def connectionDuration(self, stationName: str) -> int:
        """Returns the duration of the connection"""
        return self._connections[stationName].duration()