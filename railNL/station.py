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
        self.name = name
        self.position = (x, y)
        self.connections: Dict[str, Tuple["Station", int]] = dict()

    def getName(self):
        """Returns the name of the station"""
        return self.name

    def addConnection(self, otherStation: "Station", duration: int):
        """
        Adds a connection to station with a duration
        """
        self.connections[otherStation.getName()] = (otherStation, duration)
    
    def removeConnection(self, stationName: str):
        """
        Removes a station from connections
        """
        self.connections.pop(stationName)

    def listConnections(self) -> List[Tuple(str, int)]:
        """
        Returns a list of tuples of station name and duration for a connection.
        """
        return [(key, duration) for key, (_, duration)  in self.connections.items()]
    
    def getConnectedStation(self, stationName: str):
        """
        returns the station object of a connected station.
        """
        return self.connections[stationName][0]

    def connectionDuration(self, stationName: str) -> int:
        """
        Returns the duration of the connection
        """
        return self.connections[stationName][1]

    def hasConnection(self, stationName: str) -> bool:
        """
        Returns True if the station is connected to the station with stationName, else False.
        """
        return stationName in self.listConnections()