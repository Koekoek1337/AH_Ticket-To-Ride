import pytest
from classes.railNetwork import RailNetwork

def test_load():
    testNetwork = RailNetwork("tests/testStation.csv", "tests/testRoute.csv")

    for station in testNetwork.listStationObjects():
        print(station)
    
    assert testNetwork.listStationConnections("AAA") == [("BBB", 10, 3)]
    
    assert testNetwork.listStationConnections("BBB") == [("AAA", 10, 1),
                                                         ("CCC", 10, 2),
                                                         ("DDD", 10, 2)
                                                    ]