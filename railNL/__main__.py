from classes.railNetwork import RailNetwork
from visualize.visualize import visualize

def main():
    network = RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")
    
    network.createRoute(network.getStation("Den Helder"))
    route = network.getRoute(0)
    route.appendStation(network.getStation("Alkmaar"))
    route.appendStation(network.getStation("Castricum"))

    visualize(network.connectionPoints(), network.stationPoints(), network.routePointLists())

    network.exportSolution("Nederland")

if __name__ == "__main__":
    main()