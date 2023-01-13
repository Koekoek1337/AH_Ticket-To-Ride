from classes.station import Station
from classes.route import Route
from classes.connection import Connection

import csv

from typing import List, Tuple, Dict

class RailNetwork:
    """
    Network of stations connected by rail connections

    Attributes:

        stations (dict[str, Station]): Dictionary of station nodes, keyed by their name.
        connections (List[Connection]): List of all connection nodes, indexed by their id.
        routes (List[Route]: List of all used routes.
    """

    def __init__(self, filepathStations: str, filepathConnections: str):
        """Initializer funtion"""
        self.stations: Dict[str, Station] = dict()

        self.connections: List[Connection] = []

        self.routes: Dict[int, Route] = dict()

        self.loadStations(filepathStations)
        self.loadConnections(filepathConnections)

    
    def loadStations(self, csvFilepath: str) -> None:
        """
        Loads stations in memory from csv file
        
        Args:
            csvFilepath: The path of the CSV file containing the fields [station, x, y] in any order.
        
        Post:
            Station objects are created and stored in self.stations, keyed by name.
        """

        with open(csvFilepath) as csvFile:
            reader = csv.DictReader(csvFile)

            for row in reader:
                station = Station(row["station"], float(row["x"]), float(row["y"]))
                
                self.stations[station.name()] = station
   
    def loadConnections(self, filename: str) -> None:
        """
        Adds rail connections to station objects from csv file
        
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
        Returns a list of all station objects
        """
        return [station for _, station in self.stations.items()]

    def listStations(self) -> List[Tuple[str, int]]:
        """Returns a list of all station names with the amount of stations connected to them"""
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