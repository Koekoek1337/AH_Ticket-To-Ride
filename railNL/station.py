from typing import List, Tuple, Dict

class Station:
    """
    Station object for a rail network


    
    """

    def __init__(self, name: str, x: int, y: int):
        """
        TODO
        Initializer function
        """
        self.name = name
        self.position = (x, y)
        self.connections: Dict[str, Tuple["Station", int]] = dict()
        pass

    def addConnection(self, otherStation: "Station", duration: int):
        """
        TODO
        Adds a connection to station with a duration
        """
    

    def listConnections(self) -> List(str):
        """
        TODO
        Returns a list of all connections the station has to other stations.
        """

    def connectionTime(self, stationName: str) -> int:
        """
        TODO
        Returns the duration of the connection
        """

    def hasConnection(self, stationName: str) -> bool:
        """
        TODO
        Returns True if 
        """