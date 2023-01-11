from typing import List, Tuple

class Station:
    def __init__(self, name: str, x: int, y: int):
        """
        TODO
        Initializer function
        """
        self.name = name
        self.coordinates = (x, y)
        self.connections = []
        pass

    def addConnection(self, station: "Station", duration: int):
        """
        TODO
        Adds a connection to station with a duration
        """

    def listConnections(self):
        """
        TODO
        Returns a list of all connections the station has to other stations.
        """

    def connectionTime(self, stationName) -> int:
        """
        TODO
        Returns the duration of the connection
        """
