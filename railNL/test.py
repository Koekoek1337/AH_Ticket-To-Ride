from visualize.visualize import visualizeNetwork
from classes.railNetwork import RailNetwork

stations = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").stationPoints()
connections = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").connectionPoints()
route = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").routePointLists()

visualizeNetwork(connections, stations, route)
