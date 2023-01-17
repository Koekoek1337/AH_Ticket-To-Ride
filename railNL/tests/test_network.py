import pytest
from classes.railNetwork import RailNetwork

def test_load():
    testNetwork = RailNetwork("tests/testStation.csv", "tests/testRoute.csv")

    for station in testNetwork.listStations():
        print(station)
    
    conA = testNetwork.getStation("AAA").listStations() 
    assert conA == [[testNetwork.getStation("BBB"), 10.0]]
    
    conB = testNetwork.getStation("BBB").listStations() 
    assert conB == [[testNetwork.getStation("AAA"), 10.0],
                    [testNetwork.getStation("CCC"), 10.0],
                    [testNetwork.getStation("DDD"), 10.0]
                   ]