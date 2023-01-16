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
        self._routes = set()

    def __repr__(self):
        """"""
        return f"Station({self._name}, {self._position[0]}. {self._position[1]})"

    def __str__(self) -> str:
        """string representation"""

        return f"{self._name} station, connected to {len(self.listConnections())} other stations"

    def name(self) -> str:
        """Returns the name of the station"""

        return self._name
    
    def position(self) -> Tuple[float, float]:
        """Returns the position of the station"""
    
        return self._position

    def stationPoint(self) -> Tuple[str, Tuple[float, float]]:
        """Returns the name and position of the station"""

        return self.name(), self.position()

    def addConnection(self, stationName,  connection: "Connection") -> None:
        """Adds a connection to station with a duration"""

        self._connections[stationName] = connection

    def addRoute(self, routeID: int):
        """Adds a route to the set of routes"""
        self._routes.add(routeID)
    
    def removeRoute(self, routeID: int):
        """Removes a route from the set of routes"""
        if routeID in self._routes:
            self._routes.remove(routeID)

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
            if connection.getConnectedStation(name).isVisited():
                unvisitedStations += 1
        
        return unvisitedStations
    
    def unusedConnectionAmount(self) -> int:
        """
        Returns the amount of unused station connections connected to the station. A connection 
        is unused if it is not in any routes.
        """
        unusedStations = 0
        for name, connection in self._connections.items():
            if connection.isVisited():
                unusedtations += 1
        
        return unusedStations

    def listConnections(self) -> List[Tuple[str, float, int]]:
        """
        Returns (List[Tuple[str, float, int]]): name, duration and connections of all connecting 
            stations
        """
        return [(stationName, connection.duration(), connection.stationConnectionAmount(stationName)) 
                for stationName, connection  in self._connections.items()]
    
    def isVisited(self) -> bool:
        """
        Returns true if the station is in any route, else false
        """
        return bool(self._routes)

    def listUnvisitedConnections(self) -> List[Tuple[str, float, int]]:
        """
        Returns (List[Tuple[str, float, int]]): name, duration and unvisited connections of all 
        connecting unvisited stations
        """
        unvisitedStations = []
        
        for name, connection in self._connections.items():
            if connection.getConnectedStation(name).isVisited():
                unvisitedStations.append(
                    (name, connection.duration(), 
                     connection.getConnectedStation(name).unvistitedConnectionAmount())
                    )
        
        return unvisitedStations
        
    def listUnusedConnections(self) -> List[Tuple[str, float, int]]:
        """
        Returns (List[Tuple[str, float, int]]): name, duration and unvisited connections of all 
        stations connected via an unused connection
        """
        unusedStations = []
        
        for name, connection in self._connections.items():
            if connection.getConnectedStation(name).isVisited():
                unusedStations.append(
                    (name, connection.duration(), 
                     connection.getConnectedStation(name).unvistitedConnectionAmount())
                    )
        
        return unusedStations

    def hasConnection(self, stationName: str) -> bool:
        """Returns True if the station is connected to the station with stationName, else False."""
        return stationName in self._connections.keys()

    def getConnectedStation(self, stationName: str) -> "Station":
        """returns the station object of a connected station."""
        return self._connections[stationName].getConnectedStation(stationName)
    
    def getConnection(self, stationName: str) -> "Connection":
        """retunrs the connection object between a connected station"""
        return self._connections[stationName]

    def connectionDuration(self, stationName: str) -> int:
        """Returns the duration of the connection"""
        return self._connections[stationName].duration()