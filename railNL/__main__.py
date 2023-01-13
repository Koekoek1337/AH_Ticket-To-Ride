from classes.railNetwork import RailNetwork
from visualize.visualize import visualize

def main():
    network = RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv")

    visualize(network.connectionPoints(), network.stationPoints())

if __name__ == "__main__":
    main()