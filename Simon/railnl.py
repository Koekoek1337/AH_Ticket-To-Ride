import csv

class Network():

    def __init__(self):
        self.stations = {}

    def load_station(self, filename: str):
        """ Load all stations. """
        with open(filename,'r') as file:
            header = file.readline()
            for line in file:
                splits = line.split(',')
                if len(splits)>2:
                    station_name = str(splits[0])
                    y = float(splits[1])
                    x = float(splits[2])
                    if station_name not in self.stations:
                        self.stations[station_name] = Station(station_name)
        print(self.stations)

    def load_connections(self, filename: str):
        """ Loads and add all the possible connections with duration to each station. """
        with open(filename, 'r') as file:
            header = file.readline()
            for line in file:
                splits = line.split(',')
                if len(splits)>2:
                    station_1 = str(splits[0])
                    station_2 = str(splits[1])
                    distance = int(splits[2])
                    if station_1 in self.stations:
                        self.stations[station_1].add_connection(station_2, distance)
                    elif station_2 in self.stations:
                        self.stations[station_2].add_connection(station_1, distance)

class Station():

    def __init__(self, station_name):
        self.station_name: str = station_name
        self.connections = []


    def add_connection(self, destination, distance):
        self.connections.append((destination, distance))
        print(self.connections)





if __name__ == "__main__":
    network = Network()
    network.load_station("StationsHolland.csv")
    network.load_connections("ConnectiesHolland.csv")
