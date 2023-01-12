import csv

class Station():

    def __init__(self):
        self.name: str = station
        self.stations: Dict[str, Tuple[str, int]] = dict()


    def load_station(self, filename: str):
        """ Load all stations. """
        with open(filename,'r') as file:
            header = file.readline()
            for line in file:
                splits = line.split(',')
                if len(splits)>2:
                    station = str(splits[0])
                    if station not in self.stations:
                        self.stations[station] = None

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
                        self.station[(station_2, distance)]
                    elif station_2 in self.stations:
                        self.station[(station_1, distance)]



if __name__ == "__main__":
    station = Station()
    station.load_station("StationsHolland.csv")
    station.load_connections("ConnectiesHolland.csv")
