from classes.station import Station
from classes.connection import Connection

from typing import List, Tuple, Any, Union

class Route:
    """
    Route object that tracks rail connections between stations
    """

    def __init__(self, rootStation: Station, uid: int):
        """Initializer function"""

        self._id = uid
        self._stations: List[Station] = [rootStation]
        self._connections: List[Connection] = []

        rootStation.addRoute(self.getID())
    
    def __repr__(self):
        """representation"""
        return f"{self._id},\"[{', '.join(self.listStations())}]\""

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
    
    def listStations(self) -> List[Station]:
        """
        returns a list of stations
        """
        return [station for station in self._stations]
    
    def appendStation(self, station: Station) -> None:
        """
        Append a station at the end of stations
        """
        self.insertStation(len(self._stations), station)
    
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

    def insertConnection(self, stationIndex: int, connectionIndex: int) -> int:
        """
        Insert connections to station at stationIndex on connectionIndex
        """
        
        # Only at stationIndex 0 does a connection have to be inserted that connects to the next
        # station
        if stationIndex == 0:
            connection = self.findConnection(self._stations[stationIndex], 
                                             self._stations[stationIndex + 1])

        else:
            connection = self.findConnection(self._stations[stationIndex], 
                                             self._stations[stationIndex - 1])


        self._connections.insert(connectionIndex, connection)

    def replaceConnection(self, stationIndex: int, connectionIndex: int):
        """replace connection object on connectioIndex with new connection"""
        connection = self.findConnection(self._stations[stationIndex], 
                                         self._stations[stationIndex + 1]
                                        )

        if self._connections[connectionIndex]:
            self._connections[connectionIndex].removeRoute(self.getID())

        self._connections[connectionIndex] = connection

    def findConnection(self, station1: Station, station2: Station) -> Union[Connection, None]:
        """
        Returns the connection object between station1 and station2, if it exists
        """

        if not station1.hasConnection(station2.name()):
            return None

        connection = station1.getConnection(station2.name())
        connection.addRoute(self.getID())
        
        return connection
    
    def popStation(self, stationIndex: int) -> None:
        """
        Removes a station from stations at stationIndex
        
        TODO
        find replacement connection when not at edges
        """
        
        self._stations[stationIndex].removeRoute(self.getID())
        
        self.removeConnections(stationIndex)
        
        self._stations.pop[stationIndex]
        
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
        self._connections[connectionIndex].removeRoute(self.getID())
        
        self._connections.pop(connectionIndex)

    def getStation(self, index: int) -> Station:
        """Returns the station on stationIndex"""
        return self._stations[index]

    def getOpenStations(self) -> List[Tuple[int, Station]]:
        """
        Returns a list of all stations which can make a new connection without breaking an existing
        one.
        """
        openStations = \
        [(0, self._stations[0])] + \
        [x for t in self.brokenConnections() for x in t]+ \
        [(self.length() - 1, self._stations[self.length() - 1])] # The station at the end is always open
        

        return openStations
    
    def hasLegalMoves(self, tMax: float) -> bool:
        """
        Returns wheter the connection can make any legal moves with the stations it currently
        has.
        """
        currentDuration = self.duration()

        if currentDuration >= tMax:
            return False

        for _, station in self.getOpenStations():
            for duration in [duration for _, duration in station.listStations()]:
                if currentDuration + duration < tMax:
                    return True
        
        return False

    def getLegalMoves(self, tMax: float) -> List[Tuple[Station, int]]:
        """
        Returns the station and index for stations that have legal moves.
        """
        currentDuration = self.duration()

        stations = []

        if currentDuration >= tMax:
            return stations

        for station in self.getOpenStations():
            for duration in [duration for _, duration in station.listStations()]:
                if currentDuration + duration < tMax:
                    stations.append(station)
        
        return stations

    def brokenConnections(self) -> List[Tuple[Tuple[int, Station], Tuple[int, Station]]]:
        """
        Returns a list of all nonexistent rail connections
        
        """
        missing = []

        for i in range(self.length()):
            if not self._connections[i]:
                missing.append(((i, self._stations[i]), (i+1, self._stations[i + 1])))
        
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