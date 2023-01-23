import pytest
from classes.railNetwork import RailNetwork
from classes.route import Route
from copy import deepcopy

masterNetwork = RailNetwork("tests/testStation.csv", "tests/testRoute.csv")

def initializeNetwork():
    testNetwork = deepcopy(masterNetwork)

    stationA = testNetwork.getStation("AAA")
    stationB = testNetwork.getStation("BBB")
    stationC = testNetwork.getStation("CCC")
    stationD = testNetwork.getStation("DDD")

    return testNetwork, stationA, stationB, stationC, stationD

def test_routeID():
    """Asserts if routeID's are correctly assigned"""
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    testNetwork.createRoute(stationA)
    assert testNetwork.listRoutes()[0].getID() == 0

    testNetwork.createRoute(stationD)
    assert testNetwork.listRoutes()[1].getID() == 1

def test_routeDuration():
    """Test if the duration of the route is correctly returned"""
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    route = testNetwork.createRoute(stationA)
    assert route.duration() == 0
   
    route.appendStation(stationB)
    assert route.duration() == 10
    
    route.appendStation(stationC)
    assert route.duration() == 30

def test_routeLength():
    """Test if the amount of connections in the route is correctly returned"""
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()
    route = testNetwork.createRoute(stationA)

    route.appendStation(stationB)
    assert route.length() == 1
    route.appendStation(stationC)
    assert route.length() == 2

def test_nStations():
    """Test if the amount of stations in the route is correctly returned"""
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    route = testNetwork.createRoute(stationA)

    route.appendStation(stationB)
    assert route.nStations() == 2
    route.appendStation(stationC)
    assert route.nStations() == 3

def test_listStations():
    """Tests if all stations in the route are returned as expected"""

    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    route = testNetwork.createRoute(stationA)

    route.appendStation(stationB)
    route.appendStation(stationC)
    assert route.listStations() == [stationA, stationB, stationC]

def test_appendStation():
    """Test if a station can be appended to the back of the route"""

    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    testRoute = testNetwork.createRoute(stationA)
    testRoute.appendStation(stationB)

    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationC)
    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationD)
    assert not testRoute.brokenConnections()

def test_insertStationFront():
    """Tests if a station can be inserted to the front of the route"""

    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    testRoute = testNetwork.createRoute(stationD)
    testRoute.insertStation(0, stationB)

    assert testRoute.length() == 1
    assert testRoute.duration() == 30
    assert not testRoute.brokenConnections()

    testRoute.insertStation(0, stationA)
    
    assert testRoute.length() == 2
    assert testRoute.duration() == 40
    assert not testRoute.brokenConnections()


def test_insertStationBetween():
    """Test if a connecting station can be sucesfully inserted between two connecting stations"""
    
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    testRoute = testNetwork.createRoute(stationC)
    testRoute.appendStation(stationD)

    testRoute.insertStation(1, stationB)

    assert not testRoute.brokenConnections()
    assert testRoute.duration() == 50

def test_insertOnBroken():
    """
    Test if a connecting station can be sucesfully inserted between two non-connecting stations
    """
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()

    testRoute = testNetwork.createRoute(stationA)
    testRoute.appendStation(stationD)

    assert testRoute.brokenConnections()
    assert testRoute.duration() == 0

    testRoute.insertStation(1, stationB)

    assert not testRoute.brokenConnections()
    assert testRoute.duration() == 40

def test_routeBroken():
    testNetwork, stationA, stationB, stationC, stationD = initializeNetwork()
    
    testRoute = testNetwork.createRoute(stationC)
    testRoute.appendStation(stationA)

    assert testRoute.brokenConnections() == [((stationC, 0), (stationA, 1))]

    testRoute.appendStation(stationD)
    assert testRoute.brokenConnections() == [((stationC, 0), (stationA, 1)), ((stationA, 1), (stationD, 2))]
