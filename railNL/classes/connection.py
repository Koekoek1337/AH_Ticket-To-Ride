from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from station import Station

class Connection:
    """
    TODO
    - Implement in railNetwork
    - Implement in station
    - Implement in route
    """

    def __init__(self, uid: int, stationA: "Station", stationB: "Station", duration: float):
        """Initializer function"""
        self._id = uid
        self._connectedStations = {stationA.name():stationA, stationB.name():stationB}
        self._duration = duration

    def getID(self):
        return self._id

    def duration(self):
        """Returns the duration of the connection"""
        return self._duration

    def getConnectedStation(self, name: str) -> "Station":
        """Returns the station object keyed with name"""
        return self._connectedStations[name]

    def stationConnectionAmount(self, name:str):
        """Returns the amount of connections of station keyed with name"""
        return self._connectedStations[name].connectionAmount()
    
    def connectionPoints(self):
        return list(self._connectedStations.items())[0][1].position(), list(self._connectedStations.items())[1][1].position()
