from typing import TYPE_CHECKING, Tuple, Set, List

if TYPE_CHECKING:
    from classes.station import Station


class Connection:
    """Connection Node for rain network graph

    Connection nodes link to two station nodes and track which routes they are incorporated in.

    Attributes:
        _id (int): inique identifier.
        _connectedStations (Dict[str, Station]): A dictionary containing the two stations connected
            by this connection node, keyed by their name.
        _duration (float): The duration of the connection associated with the node.
        _routes (Set[int]): Set of route unique identifiers for all routes registered to the
            connection.
    """

    def __init__(self, uid: int, stationA: "Station", stationB: "Station", duration: float):
        """Initializer function"""

        self._id = uid
        self._connectedStations = {stationA.name(): stationA, stationB.name(): stationB}
        self._duration = float(duration)
        self._routes: Set[int] = set()

    def __lt__(self, other: "Connection"):
        """Less than magic method"""

        return self._id < other._id

    def getID(self) -> int:
        """Returns the unique ID of the connection"""

        return self._id

    def duration(self) -> float:
        """Returns the duration of the connection"""

        return self._duration

    def addRoute(self, routeID: int) -> None:
        """
        Adds a registers a route to the connection.

        Args:
            routeID (int): The route ID to to be registered.

        Post: routeID is added to self._routes.
        """
        self._routes.add(routeID)

    def removeRoute(self, routeID: int) -> None:
        """
        Unregistes a route from the connection.

        Args:
            routeID (int): The ID of the route to be unregistered.

        post: routeID is removed from self._routes.
        """

        if routeID in self._routes:
            self._routes.remove(routeID)

    def isConnected(self) -> bool:
        """Returns True if any route is registered to the connection, else False"""

        return bool(self._routes)

    def getConnectedStation(self, stationName: str) -> "Station":
        """
        Returns the Station with name with name stationName.

        Args:
            Station(str): the name of the station
        """
        return self._connectedStations[stationName]

    def stationConnectionAmount(self, stationName: str) -> int:
        """
        Returns the amount of connections the station with name stationName has.

        Args:
            Station(str): the name of the station to get connection amounts from.
        """
        return self._connectedStations[stationName].connectionAmount()

    def connectionPoints(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Returns the positions of both connected stations for visualization"""

        return (list(self._connectedStations.items())[0][1].position(),
                list(self._connectedStations.items())[1][1].position())

    def getStationNames(self) -> List[str]:
        """Returns a list of the names of the connected stations"""

        return list(self._connectedStations.keys())
