from classes.station import Station
from classes.route import Route
from classes.connection import Connection

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

        self.connections: List[Connection] = []
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

            # load station object
            for row in reader:
                station = Station(row["station"], float(row["x"]), float(row["y"]))
                
                self.stations[station.name()] = station
   
    def loadConnections(self, filename: str) -> None:
        """
        Adds rail connections to station objects
        """
        with open(filename) as csvFile:
            for row in csv.DictReader(csvFile):
                if row["station1"] in self.stations and row["station2"] in self.stations:
                    # make new connection object and add it to both stations
                    connection = Connection(len(self.connections), self.stations[row["station1"]], self.stations[row["station2"]], float(row["distance"]))
                    self.connections.append(connection)
                    
                    self.stations[row["station1"]].addConnection(row["station2"], connection)
                    self.stations[row["station2"]].addConnection(row["station1"], connection)

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
    
    def getConnectedStation(self, fromStation, toStation) -> Station:
        """
        Returns the connected station object of a station
        """
        return self.stations[fromStation].getConnectedStation(toStation)

    def connectionPoints(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Returns coordinate pairs for all rail connections
        """
        pointPairs = []
        
        for connection in self.connections:
            pointPairs.append(connection.connectionPoints())
        
        return pointPairs
    
    def stationPoints(self) -> List[Tuple[str, Tuple[float, float]]]:
        """
        Returns name coordinate pairs for all stations
        """
        points = []
        
        for station in [entry[1] for entry in self.stations.items()]:
            points.append(station.stationPoint())
        
        return points

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