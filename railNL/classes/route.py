from classes.station import Station
from classes.connection import Connection

from typing import List, Tuple, Any

class Route:
    """
    TODO
    Route object that tracks rail connections between stations
    """

    counter = -1

    @classmethod
    def newID(self):
        """Returns an unique integer for route ID"""
        self.counter += 1
        return self.counter

    def __init__(self, rootStation: Station):
        """Initializer function"""

        self._id = self.newID()
        self._stations: List[Station] = [rootStation]
        self._connections: List[Connection] = []

        rootStation.addRoute(self.getID())
    
    def getID(self):
        """Returns the id of the route"""
        return self._id

    def duration(self) -> float:
        """
        Returns the total duration of the route
        """
        totalDuration = 0

        for connection in self._connections:
            if connection:
                totalDuration += connection.duration()
        
        return totalDuration

    def length(self) -> int:
        """
        Returns amount of connections in the route
        """
        return len(self._connections)
    
    def listStations(self) -> List[str]:
        """
        returns a list of station names
        """
        return [station.name() for station in self._stations]

    def insertStation(self, stationIndex: int, station: Station) -> None:
        """
        Inserts a rail connection at the specified Index (0 for start, -1 end)

        Args:
            station (Station): The station node to connect to
        """
        self._stations.insert(stationIndex, station)
        station.addRoute(self.getID())

        if stationIndex < 0:
            stationIndex += self.length()

        if stationIndex == 0:
            self.insertConnection(stationIndex, stationIndex)
            return

        if stationIndex > 0:
            self.insertConnection(stationIndex, stationIndex - 1)

        if stationIndex < len(self._stations) - 1:
            self.replaceConnection(stationIndex,  stationIndex)
    
    def appendStation(self, station: Station) -> None:
        """
        Calls insertStation for the end of self._stations
        """
        self.insertStation(len(self._stations), station)
    
    def insertConnection(self, stationIndex: int, connectionIndex: int):
        """Insert connection to station on connectionIndex"""
        print(self._stations)
        if stationIndex == 0:
            connection = self.findConnection(self._stations[stationIndex], self._stations[stationIndex + 1])

        else:
            connection = self.findConnection(self._stations[stationIndex], self._stations[stationIndex - 1])


        self._connections.insert(connectionIndex, connection)

    def replaceConnection(self, stationIndex: int, connectionIndex: int):
        """replace connection object on connectiop Index with new connection"""
        connection = self.findConnection(self._stations[stationIndex], 
                                         self._stations[stationIndex + 1]
                                        )
        self._connections[connectionIndex] = connection

    def findConnection(self, station1: Station, station2: Station):
        """
        Returns the connection between station1 and station2 if it exists
        """

        if not station1.hasConnection(station2.name()):
            return None

        connection = station1.getConnection(station2.name())
        connection.addRoute(self.getID())
        
        return connection
    
    def removeStation(self, station: Station) -> None:
        """
        Removes a station from stations
        TODO
        find replacement connection
        """
        for stationIndex in range(len(self._connections)):
            if self._stations[stationIndex].name() == station.name():
                self._stations[stationIndex].removeRoute(self.getID())
                self.removeConnections(stationIndex)
        
    def removeConnections(self, stationIndex: int) -> None:
        """Removes connections around station on Index"""
        if stationIndex < len(self._stations) - 1:
            self.removeConnection(stationIndex)

        if stationIndex > 0:
            self.removeConnection(stationIndex - 1)

    def removeConnection(self, connectionIndex: int):
        """
        Removes a connection from Index.
        """

        if self._connections[connectionIndex]:
            self._connections[connectionIndex].removeRoute(self.getID())

        self._connections.pop(connectionIndex)

    def insertAfter(self, targetStation: Station, newStation: Station):
        """
        TODO

        Insert the station after the station with name stationName
        """
        pass

    def insertBefore(self, targetStation: Station, newStation: Station):
        """
        TODO

        Insert the station before the station with name stationName
        """
        pass

    def brokenConnections(self) -> List[Tuple[str,str]]:
        """Returns a list of all nonexistent rail connections"""
        missing = []

        for i in range(self.length()):
            if not self._connections[i]:
                missing.append((self._stations[i].name(), self._stations[i + 1].name()))
        
        return missing

    def connectionPoints(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        pointPairs = []
        
        for connection in self._connections:
            if connection:
                pointPairs.append(connection.connectionPoints())
        
        return pointPairs

    def empty(self) -> None:
        """
        Remove all stations and connections and remove route from them.
        """

        for station in self._stations:
            station.removeRoute(self.getID())
        
        self._stations = []

        for connection in self._connections:
            if connection:
                connection.removeRoute(self.getID())
        
        self._connections = []