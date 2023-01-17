from typing import TYPE_CHECKING, List, Tuple, Dict, Optional

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
        self._routes = set()

    def __repr__(self):
        """"""
        return f"Station({self._name}, {self._position[0]}. {self._position[1]})"

    def name(self) -> str:
        """Returns the name of the station"""

        return self._name
    
    def position(self) -> Tuple[float, float]:
        """Returns the x and y coordinates of the station"""
    
        return self._position

    def listStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[List["Station", Optional[int], Optional[int], Optional[int]]]:
        """
        Returns a list of all connected station nodes with the duration of the connection and
        optional information on the connections
        
        Args:
            nConnections (bool): Whether the amount of connections of the stations should be given.
            nUnused (bool): Whether the amount of unused connections should be given. A connection
                            is unused if the corresponding station node is in a route, but the
                            connection is not.
            nUnconnected (bool): Whether the amount of unconnected connections should be given. A
                               connection is unconnected if the corresponding station node is not
                               in any route.
        
        Returns: A list of lists of The station nodes with the duration of the connection amounts of
            connections (optional), the amount of unused connections (optional) and the amount of 
            unconnected connections (optional) in that order
        """
        stationList = []

        for stationName in self._connections.keys():
            station = self.getConnectedStation(stationName)
            
            stationPoint = [station, self.connectionDuration(stationName)]

            if nConnections:
                stationPoint.append(station.connectionAmount())
            
            if nUnused:
                stationPoint.append(station.unusedConnectionAmount())
            
            if nUnconnected:
                stationPoint.append(station.unvistitedConnectionAmount())
        
            stationList.append(stationPoint)
        
        return stationList

    def listConnectedStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[List["Station", Optional[int], Optional[int], Optional[int]]]:
        """
        Returns a list of connected station nodes that are not in any route with the duration of the
        connection and optional information on the connections
        
        Args:
            nConnections (bool): Whether the amount of connections of the stations should be given.
            nUnused (bool): Whether the amount of unused connections should be given. A connection
                            is unused if the corresponding station node is in a route, but the
                            connection is not.
            nUnconnected (bool): Whether the amount of unconnected connections should be given. A
                               connection is unconnected if the corresponding station node is not
                               in any route.
        
        Returns: A list of lists of The station nodes with the duration of the connection amounts of
            connections (optional), the amount of unused connections (optional) and the amount of 
            unconnected connections (optional) in that order
        """
        stationList = []
        
        for stationName in self._connections.keys():
            station = self.getConnectedStation(stationName)
            
            if station.isConnected():
                continue

            stationPoint = [station, self.connectionDuration(stationName)]

            if nConnections:
                stationPoint.append(station.connectionAmount())
            
            if nUnused:
                stationPoint.append(station.unusedConnectionAmount())
            
            if nUnconnected:
                stationPoint.append(station.unvistitedConnectionAmount())
        
            stationList.append(stationPoint)
        
        return stationList
        
    def listUnusedConnections(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[List["Station", Optional[int], Optional[int], Optional[int]]]:
        """
        Returns a list of connected station nodes to which the connections are not in any route
        with the duration of the connection and optional information on the connections
        
        Args:
            nConnections (bool): Whether the amount of connections of the stations should be given.
            nUnused (bool): Whether the amount of unused connections should be given. A connection
                            is unused if the corresponding station node is in a route, but the
                            connection is not.
            nUnconnected (bool): Whether the amount of unconnected connections should be given. A
                               connection is unconnected if the corresponding station node is not
                               in any route.
        
        Returns: A list of lists of The station nodes with the duration of the connection amounts of
            connections (optional), the amount of unused connections (optional) and the amount of 
            unconnected connections (optional) in that order
        """
        unusedStations = []
        
        for name, connection in self._connections.items():
            if connection.getConnectedStation(name).isConnected():
                unusedStations.append(
                    (name, connection.duration(), 
                     connection.getConnectedStation(name).unvistitedConnectionAmount())
                    )

        stationList = []
        
        for stationName, connection in self._connections.items():
            if connection.isConnected():
                continue
        
            station = self.getConnectedStation(stationName)

            stationPoint = [station, self.connectionDuration(stationName)]

            if nConnections:
                stationPoint.append(station.connectionAmount())
            
            if nUnused:
                stationPoint.append(station.unusedConnectionAmount())
            
            if nUnconnected:
                stationPoint.append(station.unvistitedConnectionAmount())
        
            stationList.append(stationPoint)
        
        return stationList

    def connectionAmount(self) -> int: 
        """Returns the amount of stations connected to the station"""

        return len(self._connections)
    
    def unvistitedConnectionAmount(self) -> int:
        """
        Returns the amount of unvisited stations connected to the station. A station is unvisited if
        it is not in any route.
        """
        unvisitedStations = 0
        for name, connection in self._connections.items():
            if connection.getConnectedStation(name).isConnected():
                unvisitedStations += 1
        
        return unvisitedStations
    
    def unusedConnectionAmount(self) -> int:
        """
        Returns the amount of unused station connections connected to the station. A connection 
        is unused if it is not in any routes.
        """
        unusedStations = 0
        for name, connection in self._connections.items():
            if connection.isConnected():
                unusedtations += 1
        
        return unusedStations

    def getConnectedStation(self, stationName: str) -> "Station":
        """returns the station object of a connected station."""
        return self._connections[stationName].getConnectedStation(stationName)

    def connectionDuration(self, stationName: str) -> int:
        """Returns the duration of the connection"""
        return self._connections[stationName].duration()

    # under the hood
    def hasConnection(self, stationName: str) -> bool:
        """
        Returns True if the station is connected to the station with stationName, else False.
        """
        return stationName in self._connections.keys()

    def addConnection(self, stationName: str,  connection: "Connection") -> None:
        """
        Adds a connection node to the station.
        
        Args:
            stationName (str): The name of the connected station.
            connection (Connection): The connnection node
        """
        self._connections[stationName] = connection

    def addRoute(self, routeID: int):
        """Adds a route to the set of routes"""
        self._routes.add(routeID)
    
    def removeRoute(self, routeID: int):
        """Removes a route from the set of routes"""
        if routeID in self._routes:
            self._routes.remove(routeID)

    def isConnected(self) -> bool:
        """
        Returns true if the station is in any route, else false
        """
        return bool(self._routes)

    def getConnection(self, stationName: str) -> "Connection":
        """returns the connection object between a connected station"""
        return self._connections[stationName]