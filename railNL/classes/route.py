from classes.station import Station
from classes.connection import Connection

from typing import List, Tuple, Dict, Union, Optional

import numpy as np

class Route:
    """
    Route node that tracks rail connections between stations
    
    properties:
        _id (int): The unique identifier of the Route
        _stations (List[Station]): The stations in the route in order
        _connections (List[Connection]): The connections between the stations in order
    """

    def __init__(self, rootStation: Station, uid: int):
        """Initializer function"""

        self._id = uid
        self._stations: List[Station] = [rootStation]
        self._connections: List[Connection] = []

        rootStation.addRoute(self.getID())
    
    def __repr__(self):
        """representation"""
        return f"{self._id},\"[{', '.join([station.name() for station in self.listStations()])}]\""

    # getters
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
    
    def nStations(self) -> int:
        """
        returns the amount of stations in the route
        """
        return len(self._stations)

    # Stations
    def listStations(self) -> List[Station]:
        """
        returns a list of stations
        """
        return [station for station in self._stations]
    
    def appendStation(self, station: Station) -> None:
        """
        Append a station at the end of stations
        """
        self.insertStation(self.nStations(), station)
    
    def insertStation(self, stationIndex: int, station: Station) -> None:
        """
        Inserts a rail connection at the specified Index (0 for start, -1 end)

        Args:
            station (Station): The station node to connect to
        """
        self._stations.insert(stationIndex, station)

        station.addRoute(self.getID())

        if len(self._stations) == 1:
            return

        if stationIndex < 0:
            stationIndex += self.nStations()

        if stationIndex == 0:
            connectionIndex = 0
        else:
            connectionIndex = stationIndex - 1

        self._insertConnection(stationIndex, connectionIndex)

        if stationIndex < self.nStations() - 1 and stationIndex != 0:
            connectionIndex = stationIndex

            self._replaceConnection(stationIndex, connectionIndex)
    
    def popStation(self, stationIndex: int = -1) -> None:
        """
        Removes the station at stationIndex from the route.
        """
        
        station = self._stations.pop(stationIndex)
        
        # Do not remove the routeID from station if it still occurs in the route
        if station not in self._stations:
            station.removeRoute(self.getID())


        self.removeConnections(stationIndex)

        # Insert a new connection if possible if the removed station was not at the head or tail end
        if stationIndex not in [0, self.nStations()]:
            self._insertConnection(stationIndex, stationIndex - 1)
        
    def removeConnections(self, stationIndex: int) -> None:
        """Removes connections around station on Index"""
        if stationIndex < self.nStations() - 1:
            self.removeConnection(stationIndex)

        if stationIndex > 0:
            self.removeConnection(stationIndex - 1)

    def removeConnection(self, connectionIndex: int):
        """
        Removes the connection on connectionIndex.
        """
        connection = self._connections.pop(connectionIndex)

        # Do not remove routeID from connection if it is still in the route
        if connection and connection not in self._connections:
            connection.removeRoute(self.getID())

    def getStation(self, index: int) -> Station:
        """Returns the station on stationIndex"""
        return self._stations[index]

    def getOpenStations(self) -> List[Tuple[Station, int]]:
        """
        Returns (List[Tuple[Station, int]]): A list of tuples of stations and their indexes.
            a station can occur multiple times if it has a broken connection.

        """
        openStations = [(self._stations[0], 0)]

        openStations += [(self._stations[self.nStations() - 1], self.nStations() - 1)]

        return openStations
    
    def hasLegalMoves(self, tMax: float) -> bool:
        """
        Returns wheter the connection can make any legal moves with the stations it currently
        has.
        """
        currentDuration = self.duration()

        if currentDuration >= tMax:
            return False

        for station, _ in self.getOpenStations():
            for _, duration, *_ in station.listStations():
                if currentDuration + duration < tMax:
                    return True
        
        return False

    def getLegalMoves(self, tMax: float, 
            nConnections = False, nUnused = False, nUnvisited = False, unusedOnly = False,
            unvisitedOnly = False) \
            -> Dict[int, List[Tuple[Station, int, Optional[int], Optional[int], Optional[int]]]]:
        """
        Returns a dict keyed with the station indexes with all stations witha connection that can
        legally be added to the route.

        Args:
            tMax (float): The maximum duration for the route
        """
        currentDuration = self.duration()

        legalMoves = dict()

        for station, index in self.getOpenStations():
            if index in legalMoves:
                continue
            
            connectionList = []

            if unvisitedOnly:
                connectionList = station.listUnvisitedStations(nConnections, nUnused, nUnvisited)
            elif unusedOnly:
                connectionList = station.listUnusedConnections(nConnections, nUnused, nUnvisited)
            else:
                connectionList = station.listStations(nConnections, nUnused, nUnvisited)

            legalStations = []

            for newStation in connectionList:
                duration = newStation[1]
                if currentDuration + duration < tMax:
                    legalStations.append(newStation)
            
            if legalStations:
                legalMoves[index] = legalStations
    
        return legalMoves

    def brokenConnections(self) -> List[Tuple[Tuple[Station, int], Tuple[Station, int]]]:
        """
        Returns a list of all nonexistent rail connections.

        Returns (List[Tuple[Tuple[Station, int], Tuple[Station, int]]])
        """
        missing = []

        for i in range(self.length()):
            if not self._connections[i]:
                missing.append(((self._stations[i], i), (self._stations[i + 1], i + 1)))
        
        return missing

    def connectionPoints(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Returns a list of point pairs of x and y coordinates for all connections in the route for
        visualization.
        """

        pointPairs = []
        
        for connection in self._connections:
            if connection:
                pointPairs.append(connection.connectionPoints())
        
        return pointPairs
    
    def isValid(self, tMax: float = 0.0) -> bool:
        """
        Returns True if the route is legal else False. A route is legal if it has at least one
        connection, is unbroken and is shorter than tMax
        """
        # A route must have 1 connection
        if self.length() == 0:
            return False

        # None in connections meanse a missing connection
        if None in self._connections:
            return False
        
        # tMax is optional
        if tMax == 0:
            return True
        
        # If a tMax is given, duration must be less than tMax
        return self.duration() < tMax

    def empty(self) -> None:
        """
        Remove all stations and connections from the route and remove routeID from them.
        """
        for station in self._stations:
            station.removeRoute(self.getID())
        
        self._stations = []

        for connection in self._connections:
            if connection:
                connection.removeRoute(self.getID())
        
        self._connections = []
    
    def uniqueStations(self) -> int:
        """
        Returns the amount of stations in route that are unique.
        """
        return len(np.unique(self._stations))
    
    def uniqueConnections(self) -> int:
        """
        Returns the amount of connections in the route that are unique.
        """
        return len(np.unique(self._connections))
    
    def routeScore(self, totalConnections: int) -> float:
        """
        Returns the score of the route in an empty system
        """
        score = self.uniqueConnections() / totalConnections * 10000 - (100 + self.duration())

        return score

    # Connections
    def _insertConnection(self, stationIndex: int, connectionIndex: int) -> int:
        """
        Insert connections to station at stationIndex on connectionIndex
        """
        
        # Only at stationIndex 0 does a connection have to be inserted that connects to the next
        # station

        stationA = self._stations[stationIndex]
        stationB = None
        
        if stationIndex == 0:
            stationB = self._stations[stationIndex + 1]
        else:
            stationB = self._stations[stationIndex - 1]

        connection = self._findConnection(stationA, stationB)
        
        if connection:
            connection.addRoute(self.getID())

        self._connections.insert(connectionIndex, connection)

    def _replaceConnection(self, stationIndex: int, connectionIndex: int):
        """replace connection node on connectioIndex with new connection"""
        oldConnection = self._connections[connectionIndex]
        newConnection = self._findConnection(self._stations[stationIndex], 
                                         self._stations[stationIndex + 1]
                                        )
       
        self._connections[connectionIndex] = newConnection

        # Only attempt to remove routeID if oldConnection not None
        # Do not remove routeID from connection if it is still in the route
        if oldConnection and oldConnection not in self._connections:
            self._connections[connectionIndex].removeRoute(self.getID())

    def _findConnection(self, station1: Station, station2: Station) -> Union[Connection, None]:
        """
        Returns the connection node between station1 and station2, if it exists
        """

        if not station1.hasConnection(station2.name()):
            return None

        connection = station1.getConnection(station2.name())
        
        return connection