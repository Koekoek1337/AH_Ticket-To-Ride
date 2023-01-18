from typing import TYPE_CHECKING, List, Tuple, Dict, Optional, Union

if TYPE_CHECKING:
    from connection import Connection

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
        self._connections: Dict[str, "Connection"] = dict()
        self._routes = set()

    def __str__(self):
        """"""
        return f"Station {self._name}"

    def name(self) -> str:
        """Returns the name of the station"""

        return self._name
    
    def position(self) -> Tuple[float, float]:
        """Returns the x and y coordinates of the station"""
    
        return self._position
    
    def inRoute(self, routeID: int) -> bool:
        """Returns true if the station is in route routeID, else false"""

        if routeID in self._routes:
            return True
        
        return False

    def listStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[Tuple["Station", int, Optional[int], Optional[int], Optional[int]]]:
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
            
            stationPoint = [station, self.connectionDuration(stationName), None, None, None]

            if nConnections:
                stationPoint[2] = station.connectionAmount()
            
            if nUnused:
                stationPoint[3] = station.unusedConnectionAmount()
            
            if nUnconnected:
                stationPoint[4] = station.unvistitedConnectionAmount()
        
            stationList.append(tuple(stationPoint))
        
        return stationList

    def listUnconnectedStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[Tuple["Station", int, Optional[int], Optional[int], Optional[int]]]:
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
        stationList = self.listStations(nConnections, nUnused, nUnconnected)
        
        # from all stations with data, take only those where the station is unconnected
        return [stationPoint for stationPoint in stationList if not stationPoint[0].isConnected()]
        
    def listUnusedConnections(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[Tuple["Station", int, Optional[int], Optional[int], Optional[int]]]:
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
        stationList = self.listStations(nConnections, nUnused, nUnconnected)
        
        # From all connected stations, take only the stations have a connection node connected to
        # self that is not visited by any route.
        return [stationPoint for stationPoint in stationList 
                if not stationPoint[0].getConnection(self.name()).isConnected()
               ]

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
            if not connection.getConnectedStation(name).isConnected():
                unvisitedStations += 1
        
        return unvisitedStations
    
    def unusedConnectionAmount(self) -> int:
        """
        Returns the amount of unused station connections connected to the station. A connection 
        is unused if it is not in any routes.
        """
        unusedStations = 0
        for _, connection in self._connections.items():
            if not connection.isConnected():
                unusedStations += 1
        
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
    
    def listNodeConnections(self) -> List["Connection"]:
        "returns a list of the connection nodes connected to the station"
        return [connection for _, connection in self._connections.items()]