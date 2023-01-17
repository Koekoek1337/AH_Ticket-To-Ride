import os
import csv
import datetime

from classes.station import Station
from classes.route import Route
from classes.connection import Connection

from typing import Optional, List, Tuple, Dict, Union

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
        """
        Initializer function

        Args:
            filepathStations (str): The path to the station data csv file
        """
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
   
    def loadConnections(self, csvFilepath: str) -> None:
        """
        Adds rail connections to station objects from csv file
        

        """
        with open(csvFilepath) as csvFile:
            for row in csv.DictReader(csvFile):
                if row["station1"] in self.stations and row["station2"] in self.stations:
                    # make new connection object and add it to both stations
                    connection = Connection(len(self.connections), self.stations[row["station1"]], self.stations[row["station2"]], float(row["distance"]))
                    self.connections.append(connection)
                    
                    self.stations[row["station1"]].addConnection(row["station2"], connection)
                    self.stations[row["station2"]].addConnection(row["station1"], connection)

    # User methods: Stations
    def listStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[List[Union["Station", Optional[int]]]]:
        """
        Returns a list of all station nodes with optional information on their connections
        
        Args:
            nConnections (bool): Whether the amount of connections of the stations should be given.
            nUnused (bool): Whether the amount of unused connections should be given. A connection
                            is unused if the corresponding station node is in a route, but the
                            connection is not.
            nUnconnected (bool): Whether the amount of unconnected connections should be given. A
                               connection is unconnected if the corresponding station node is not
                               in any route.
        
        Returns: A list of lists of The station nodes with the amounts of connections (optional), 
                 the amount of unused connectiosn (optional) and the amount of unconnected connections
                (optional) in that order
        """
        stationList = []

        for _, station in self.stations.items():
            
            stationPoint = station

            if nConnections or nUnused or nUnconnected:
                stationPoint = [stationPoint]

                if nConnections:
                    stationPoint.append(station.connectionAmount())
                
                if nUnused:
                    stationPoint.append(station.unusedConnectionAmount())
                
                if nUnconnected:
                    stationPoint.append(station.unvistitedConnectionAmount())
        
            stationList.append(stationPoint)
        
        return stationList
    
    def getStation(self, stationName: str) -> Station:
        """Returns the station node with stationName"""
        return self.stations[stationName]

    def listUnconnectedStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[List[Union["Station", Optional[int]]]]:
        """
        Returns a list of all stations not connected to any route.

        Args:
            nConnections (bool): Whether the amount of connections of the stations should be given.
            nUnused (bool): Whether the amount of unused connections should be given. A connection
                            is unused if the corresponding station node is in a route, but the
                            connection is not.
            nUnconnected (bool): Whether the amount of unconnected connections should be given. A
                               connection is unconnected if the corresponding station node is not
                               in any route.
        
        Returns: A list of lists of The station nodes with the amounts of connections (optional), 
                 the amount of unused connectiosn (optional) and the amount of unconnected connections
                (optional) in that order
        """
        stationList = []

        for _, station in self.stations.items():
            # skip if station is connected
            if station.isConnected():
                continue

            stationPoint = station

            if nConnections or nUnused or nUnconnected:
                stationPoint = [stationPoint]

                if nConnections:
                    stationPoint.append(station.connectionAmount())
                
                if nUnused:
                    stationPoint.append(station.unusedConnectionAmount())
                
                if nUnconnected:
                    stationPoint.append(station.unvistitedConnectionAmount())
        
            stationList.append(stationPoint)
        
        return stationList
    
    # User methods: Routes
    def createRoute(self, station: Station):
        """
        Creates an empty route with initial station station and adds it to routes.
        """
        newRoute = Route(station)
        self.routes[newRoute.getID()] = newRoute
    
    def nRoute(self) -> int:
        """
        Returns the amount of routes
        """
        return len(self.routes)

    def getRoute(self, routeID: int) -> Route:
        """
        returns the route with routeID  
        """
        return self.routes[routeID]

    def delRoute(self, routeID: int):
        """
        Removes a route from routes
        """
        self.routes[routeID].empty()
        self.routes.pop(routeID)

    def listRoutes(self) -> List[Route]:
        """
        Returns the list of train routes
        """
        return [route for _, route in self.routes.items()]

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
            points.append(station.name(), station.position())
        
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
    def checkValidSolution(self, tMax: float) -> bool:
        if self.checkStationCoverage(self) and self.checkLegalRoutes(self, tMax):
            return True
        
        return False

    def checkStationCoverage(self) -> bool:
        """Returns True if all stations have routes going through them, else false"""
        for _, station in self.stations.items():
            if not station.isConnected():
                return False
        
        return True
    
    def checkLegalRoutes(self, tMax: float) -> bool:
        """Returns True if all routes are legal (unbroken and duration < tMax)"""
        for _, route in self.routes.items():
            if route.brokenConnections() or route.duration() >= tMax:
                return False
        return True
    
    def connectionCoverage(self) -> float:
        """Returns the fraction of connections that have routes going over them"""
        usedConnections = 0

        for connection in self.connections:
            if connection.isConnected():
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