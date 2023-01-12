from station import Station
from route import Route
from connection import Connection

import csv

from typing import List, Tuple, Dict

class RailNetwork:
    """
    Network of stations connected by rail connections

    Attributes:

        stations (dict[str, Station]): Dictionary with key value pairs of a station and it's name.
    """

    def __init__(self, filenameStations: str, filenameConnections: str):
        """
        Initializer funtion
        """
        self.stations: Dict[str, Station] = dict()

        self.nConnections = 0

        self.routeID = 0
        self.routes: Dict[int, Route]

        self.loadStations(filenameStations)
        self.loadConnections(filenameConnections)

    
    def loadStations(self, filename: str) -> None:
        """
        Loads station objects from file filename
        """

        with open(filename) as csvFile:
            reader = csv.DictReader(csvFile)

            # find min and max x coordinates for relative x coordninates
            coords = [float(row["x"]) for row in reader]
            minX = min(coords)
            maxDX = max(coords) - minX

            csvFile.seek(0)

            # find min and max y coordinates for relative y coordinates
            coords = [float(row["y"]) for row in reader]
            minY = min(coords)
            maxDY = max(coords) - minY

            csvFile.seek(0)

            # load station object
            for row in reader:
                station = Station(row["station"], 
                                  (float(row["x"]) - minX) / maxDX, 
                                  (float(row["y"] - minY)) / maxDY
                                )
                
                self.stations[station.name()] = station
   
    def loadConnections(self, filename: str) -> None:
        """
        Adds rail connections to station objects
        """
        with open(filename) as csvFile:
            for row in csv.DictReader(csvFile):
                if row["station1"] in self.stations and row["station2"] in self.stations:
                    self.stations[row["station1"]].addConnection(self.stations[row["station2"]], row["distance"])
                    self.stations[row["station2"]].addConnection(self.stations[row["station1"]], row["distance"])
                    
                    self.routes += 1

    def listStationObjects(self) -> List[Station]:
        """
        Returns a list of all stations
        """
        return [station for _, station in self.stations.items()]

    def listStations(self) -> List[Tuple[str, int]]:
        """Returns a list of all stations with their amount of connections"""
        return [(station.name(), station.connectionAmount()) for _, station in self.stations.items()]

    def listStationConnections(self, stationName: str) -> List[Tuple[str, int, int]]:
        """
        Returns (List[Tuple[str, int, int]]) name, duration and connections of connecting stations
        """
        return self.stations[stationName].listConnections()

    def createRoute(self):
        """
        TODO
        Creates an empty route object and adds it to routes
        """
        pass
    
    def listRoutes(self):
        """
        TODO
        Returns the list of train routes
        """
        pass

    # TODO: add route operations