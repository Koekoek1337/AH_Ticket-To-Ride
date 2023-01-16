import os
import csv
import datetime

from classes.station import Station
from classes.route import Route
from classes.connection import Connection

from typing import List, Tuple, Dict

class RailNetwork:
    """
    Network of stations connected by rail connections

    Attributes:

        stations (dict[str, Station]): Dictionary of station nodes, keyed by their name.
        connections (List[Connection]): List of all connection nodes, indexed by their id.
        routes (List[Route]: List of all used routes.
    """

    # Initialization functions

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

    # User methods: Stations
    def listStations(self) -> List[Tuple[str, int]]:
        """Returns a list of all station names with the amount of stations connected to them"""
        return [(station.name(), station.connectionAmount()) for _, station in self.stations.items()]

    def listStationConnections(self, stationName: str) -> List[Tuple[str, int, int]]:
        """
        Returns (List[Tuple[str, int, int]]) name, duration and connections of connecting stations
        """
        return self.stations[stationName].listConnections()
    
    # User methods: Routes
    def createRoute(self, stationName: str):
        """
        Creates an empty route object and adds it to routes
        """
        newRoute = Route(self.stations[stationName])
        self.routes[newRoute.getID()] = newRoute
    
    def delRoute(self, routeID: int):
        """
        Removes a route from routes
        """
        self.routes[routeID].empty()
        self.routes.pop(routeID)

    def listRoutes(self) -> List[Tuple[int, List[str]]]:
        """
        Returns the list of train routes
        """
        return [(key, route.listStations()) for key, route in self.routes.items()]

    def routeAppendStation(self, routeID: int, stationName: str):
        """
        Append station with stationName to route with routeID
        """
        self.routes[routeID].appendStation(self.stations[stationName])

    # TODO: add more route methods

    # Output methods
    def score(self) -> float:
        """
        Returns the score of the solution for the solution with the current routes according to
        score function:
            K = p*10000 - (T*100 + Min)
        K is the quality of the service
        p is the fraction of rail connections with 
        """
        return self.connectionCoverage() * 1000 - (len(self.routes) * 100 + self.totalDuration())
    
    def exportSolution(self, filename: str) -> None:
        """
        Exports the current routes to a csv file to /results
        """
        if not os.path.exists("results/"):
            os.mkdir("results/")
        
        timeStamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        with open(f"results/{timeStamp}-{filename}.csv", "w") as resultFile:
            resultFile.write("train,stations\n")

            for id, route in self.routes.items():
                resultFile.write(f"{id},\"[{', '.join(route.listStations())}]\"\n")
            
            resultFile.write(f"score,{self.score()}")


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
    
    def routePointLists(self) -> List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Returns a list of coordinate pairs for connections of all rail routes
        """
        routePointLists = []
        
        for _, route in self.routes.items():
            routePointLists.append(route.connectionPoints())
        
        return routePointLists

    # Check methods
    def checkValidSolution(self) -> bool:
        if self.checkStationCoverage(self) and self.checkLegalRoutes(self):
            return True

    def checkStationCoverage(self) -> bool:
        """Returns True if all stations have routes going through them, else false"""
        for _, station in self.stations.items():
            if not station.isVisited():
                return False
        return True
    
    def checkLegalRoutes(self, tMax: float) -> bool:
        """Returns True if all routes are legal (unbroken and duration < tMax)"""
        for _, route in self.routes.items():
            if route.brokenConnections() or route.duration() > tMax:
                return False

    def connectionCoverage(self) -> float:
        """Returns the fraction of connections that have routes going over them"""
        usedConnections = 0

        for connection in self.connections:
            if connection.isVisited():
                usedConnections += 1
        
        return usedConnections / len(self.connections)

    def totalDuration(self) -> float:
        """returns the total duration of the routes"""
        totalDuration = 0

        for _, route in self.routes.items():
            totalDuration += route.duration()
        
        return totalDuration
    
    # operation methods
    def listStationObjects(self) -> List[Station]:
        """
        Returns a list of all station objects
        """
        return [station for _, station in self.stations.items()]

    def getConnectedStation(self, fromStation, toStation) -> Station:
        """
        Returns the connected station object of a station
        """
        return self.stations[fromStation].getConnectedStation(toStation)