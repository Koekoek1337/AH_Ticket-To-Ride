from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from station import Station

class Connection:
    """
    TODO
    - Implement in route
    """

    def __init__(self, uid: int, stationA: "Station", stationB: "Station", duration: float):
        """Initializer function"""
        self._id = uid
        self._connectedStations = {stationA.name():stationA, stationB.name():stationB}
        self._duration = duration

    def getID(self):
        """Returns the unique ID of the connection"""
        return self._id

    def duration(self):
        """Returns the duration of the connection"""
        return self._duration

    def getConnectedStation(self, name: str) -> "Station":
        """
        Returns the Station object in self._connectedStations with key name.

        Args:
            Station(str): the name of the station
        """
        return self._connectedStations[name]

    def stationConnectionAmount(self, name:str) -> int:
        """
        Returns the amount of connections he Station object in self._connectedStations with key 
        name.

        Args:
            Station(str): the name of the station
        """
        return self._connectedStations[name].connectionAmount()
    
    def connectionPoints(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Returns (Tuple())station positions for visualization.
        """

        return (list(self._connectedStations.items())[0][1].position(), 
                list(self._connectedStations.items())[1][1].position())
