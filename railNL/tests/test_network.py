import pytest
from classes.railNetwork import RailNetwork
from classes.route import Route
from copy import deepcopy

masterNetwork = RailNetwork("tests/testStation.csv", "tests/testRoute.csv")

def test_load():
    testNetwork = deepcopy(masterNetwork)

    for station in testNetwork.listStations():
        print(station)
    
    conA = testNetwork.getStation("AAA").listStations() 
    assert conA == [[testNetwork.getStation("BBB"), 10.0]]
    
    conB = testNetwork.getStation("BBB").listStations() 
    assert conB == [[testNetwork.getStation("AAA"), 10.0],
                    [testNetwork.getStation("CCC"), 20.0],
                    [testNetwork.getStation("DDD"), 30.0]
                   ]

def test_routeID():
    testNetwork = deepcopy(masterNetwork)

    stationA = testNetwork.getStation("AAA")
    stationB = testNetwork.getStation("BBB")
    stationC = testNetwork.getStation("CCC")
    stationD = testNetwork.getStation("DDD")

    testNetwork.createRoute(stationA)
    assert testNetwork.listRoutes()[0].getID() == 0

    testNetwork.createRoute(stationD)
    assert testNetwork.listRoutes()[1].getID() == 1

def test_routeAppend():
    testNetwork = deepcopy(masterNetwork)

    stationA = testNetwork.getStation("AAA")
    stationB = testNetwork.getStation("BBB")
    stationC = testNetwork.getStation("CCC")
    stationD = testNetwork.getStation("DDD")

    testRoute = testNetwork.createRoute(stationA)
    testRoute.appendStation(stationB)

    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationC)
    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationD)
    assert not testRoute.brokenConnections()

def test_routeBroken():
    testNetwork = deepcopy(masterNetwork)

    stationA = testNetwork.getStation("AAA")
    stationB = testNetwork.getStation("BBB")
    stationC = testNetwork.getStation("CCC")
    stationD = testNetwork.getStation("DDD")

    testRoute = testNetwork.createRoute(stationC)
    testRoute.appendStation(stationA)

    assert testRoute.brokenConnections() == [((0, stationC), (1, stationA))]

    testRoute.appendStation(stationD)
    assert testRoute.brokenConnections() == [((0, stationC), (1, stationA)), ((1, stationA), (2, stationD))]

def test_routeDuration():
    testNetwork = deepcopy(masterNetwork)

    stationA = testNetwork.getStation("AAA")
    stationB = testNetwork.getStation("BBB")
    stationC = testNetwork.getStation("CCC")
    stationD = testNetwork.getStation("DDD")

    testRoute = testNetwork.createRoute(stationA)
    testRoute.appendStation(stationB)

    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationC)
    assert not testRoute.brokenConnections()

    testRoute.appendStation(stationD)
    assert not testRoute.brokenConnections()
    
    assert testRoute.duration() == 70.0

def test_reroute():
    """
    TODO
    port to network
    """
    pass

    # route3 = Route(stationB, 3)

    # route3.appendStation(stationD)

    # route3.insertStation(1, stationC)

    # assert route3._connections == [connection1, connection3]

    