from classes.station import Station
from classes.connection import Connection
from classes.route import Route

from typing import Tuple

import pytest

@pytest.mark.parametrize("name, x, y", [("AAA", 0, 0), ("BBB", 0.5, 0.7)])
def test_EmptyStation(name, x, y):
    station = Station(name, x, y)

    assert station.name() == name
    assert station.position() == (x, y)
    assert station.connectionAmount() == 0
    assert station.listStations() == []
    assert station.hasConnection(name) == False

def generateConnectionNew(stationA, stationB, time) -> Connection:
    return Connection(0, stationA, stationB, time)


# initialize small rail system
stationA = Station("AAA", 0, 0)
stationB = Station("BBB", 0, 0)
stationC = Station("CCC", 0, 0)
stationD = Station("DDD", 0, 0)

connection0 = Connection(0, stationA, stationB, 10)
stationA.addConnection("BBB", connection0)
stationB.addConnection("AAA", connection0)

connection1 = Connection(1, stationB, stationC, 10)
stationB.addConnection("CCC", connection1)
stationC.addConnection("BBB", connection1)

connection2 = Connection(2, stationB, stationD, 10)
stationB.addConnection("DDD", connection2)
stationD.addConnection("BBB", connection2)

connection3 = Connection(3, stationC, stationD, 10)
stationC.addConnection("DDD", connection3)
stationD.addConnection("CCC", connection3)


def test_connectionAmount():
    assert stationA.connectionAmount() == 1
    assert stationB.connectionAmount() == 3
    assert stationC.connectionAmount() == 2
    assert stationD.connectionAmount() == 2


def test_listConnections():
    assert stationB.listStations(True, True, True) == [[stationA, 10.0, 1, 1, 1], [stationC, 10.0, 2, 2, 2], [stationD, 10.0, 2, 2, 2]]

def test_hasConnections():
    assert stationA.hasConnection("BBB") == True

def test_getConnectedStation():
    assert stationA.getConnectedStation("BBB") == stationB

def test_connectionDuration():
    assert stationA.connectionDuration("BBB") == 10

def test_addRoute():
    route0 = Route(stationA)

    assert stationA._routes == {0}

    assert stationB._routes == set()

    route0.appendStation(stationB)

    assert stationB._routes == {0}

    assert route0._stations == [stationA, stationB]    

    route0.empty()

    assert stationA._routes == set()
    assert stationB._routes == set()

def test_broken():
    route1 = Route(stationA)

    route1.appendStation(stationD)

    assert route1.brokenConnections() == [("AAA", "DDD")]
    
    route1.insertStation(1, stationB)

    assert route1.brokenConnections() == []

    route1.empty()

def test_reroute():
    route3 = Route(stationB)

    route3.appendStation(stationD)

    route3.insertStation(1, stationC)

    assert route3._connections == [connection1, connection3]