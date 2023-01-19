from classes.railNetwork import RailNetwork
from visualize.visualize import visualizeNetwork
from os import path

BATCH = False

if path.exists("railNL/algorithms/random_hajo.py"):
    from algorithms import random_hajo

    BATCH = True

def main():
    network = RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")
    
    if BATCH:
        random_hajo.main(network, 20, 180)
        return
    
    network.createRoute(network.getStation("Den Helder"))
    route = network.getRoute(0)
    route.appendStation(network.getStation("Alkmaar"))
    route.appendStation(network.getStation("Castricum"))

    visualizeNetwork(network.connectionPoints(), network.stationPoints(), network.routePointLists())

    network.exportSolution("results", "Nederland")

if __name__ == "__main__":
    main()