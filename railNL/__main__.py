from classes.railNetwork import RailNetwork
from visualize.visualize import visualize

def main():
    network = RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")
    
    network.createRoute("Den Helder")
    network.routeAppendStation(0, "Alkmaar")
    network.routeAppendStation(0, "Castricum")

    visualize(network.connectionPoints(), network.stationPoints(), network.routePointLists())

    network.exportSolution("Nederland")

if __name__ == "__main__":
    main()