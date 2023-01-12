import station

from typing import TypeAlias

Station: TypeAlias = station.Station

class Connection:
    """
    TODO
    - Implement in railNetwork
    - Implement in station
    - Implement in route
    """
    def __init__(self, uid: int, stationA: Station, stationB: Station, duration: int):
        """Initializer function"""
        self._id = uid
        self._connectedStations = {stationA.name():stationA, stationB.name():stationB}
        self._duration = duration

    def duration(self):
        """Returns the duration of the connection"""
        return self._duration
    
    def getConnectedStation(self, name):
        """Returns the station object keyed with name"""
        return self._connectedStations(name)

    def stationConnectionAmount(self, name:str):
        """Returns the amount of connections of station keyed with name"""
        return self._connectedStations[name].connectionAmount()