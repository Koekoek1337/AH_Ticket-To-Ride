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
    assert conA == [(testNetwork.getStation("BBB"), 10.0, None, None, None)]
    
    conB = testNetwork.getStation("BBB").listStations() 
    assert conB == [(testNetwork.getStation("AAA"), 10.0, None, None, None),
                    (testNetwork.getStation("CCC"), 20.0, None, None, None),
                    (testNetwork.getStation("DDD"), 30.0, None, None, None),
                   ]
    