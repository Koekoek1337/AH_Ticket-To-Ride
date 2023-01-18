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
    
    Quick Guide
    o ROUTES
    > Creating a new route:
        - To create a route, pick one station from self.listStations()
        - Then create a new route with self.createRoute()
        - The new route can is returned from createRoute() or can be taken from self.listRoutes().

    > Getting the head and Tail end stations from the Route:
        - Use route.getStation(0) to get the head end of the station.
        - Use route.getStation(-1) for the get the tail end of the station.
        - route.getStation can also get any other station in the route, and can be treated like a
          list in this regard.
    
    > Adding a station to the head and tail end:
        - Use route.appendStation(station) to add a station at the tail end of the route
        - Use route.insertStation(0, station) to add a station to the head end of the route
        - route.insertStation can also be used to add a station to the middle of the route. However,
          this will lead to broken connections which will have to be resolved before the route is
          legal.
    
    > Removing a station from the head and tail end:
        - Use route.popStation() to remove a station from the tail end of the route
        - Use route.popStation(0) to remove a station from the head end of the route
        - route.popStation can also be used to remove a station from the middle of te route. However
          this will lead to unconnected stations, which will have to be resolved before the route is
          legal.

    O STATIONS
    > Getting connecting stations
        - 

    Attributes:
        stations (dict[str, Station]): Dictionary of station nodes, keyed by their name.
        connections (List[Connection]): List of all connection nodes, indexed by their id.
        routes (List[Route]): List of all used routes.
        routeID (int): The first free unique identifier for routes
    """

    # Initialization functions

    def __init__(self, filepathStations: str, filepathConnections: str):
        """
        Initializer function

        Args:
            filepathStations (str): The path to the station data csv file.
            filepathConnections (str): The path to the connection data csv file.
        """
        self.stations: Dict[str, Station] = dict()

        self.connections: List[Connection] = []

        self.routes: Dict[int, Route] = dict()

        self.routeID = 0

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
        
        Args:
            csvFilepath (str): The path to the file containing connections between stations
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
    def getStation(self, stationName: str) -> Station:
        """
        Returns the station node with key stationName
        
        Args:
            stationName (str): the name of the station
        """
        return self.stations[stationName]

    def listStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[Union["Station", Tuple["Station", Optional[int], Optional[int], Optional[int]]]]:
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
        # if no extra data is requested, a simple list comprehension can be used
        if not (nConnections or nUnused or nUnconnected):
            return [station for _, station in self.stations.items()]

        stationList = []

        # Loop through all station nodes in the stations dictionary
        for _, station in self.stations.items():
            stationPoint = [station, None, None, None]

            # Append the amount of connections of the station if requested.
            if nConnections:
                stationPoint[1] = station.connectionAmount()
            
            # append the amount of unused connections of the station if requested.
            if nUnused:
                stationPoint[2] = station.unusedConnectionAmount()
            
            # append the amount of unconnected stations connected to the station if requested.
            if nUnconnected:
                stationPoint[3] = station.unvistitedConnectionAmount()
        
            stationList.append(tuple(stationPoint))
        
        return stationList

    def listUnconnectedStations(self, nConnections = False, nUnused = False, nUnconnected = False) \
        -> List[Union["Station", Tuple["Station", Optional[int], Optional[int], Optional[int]]]]:
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
        # get the list of all station and take only the unconnected stations
        if not (nConnections or nUnused or nUnconnected):
            return [station for station in self.listStations() if not station.isConnected()]

        # If data is requested, get list of stations with data and take only unconnected stations
        return [station for station in self.listStations(nConnections, nUnused, nUnconnected) if not
                station[0].isConnected()]
    
    # User methods: Routes
    def createRoute(self, station: Station) -> Route:
        """
        Creates a route with a root station and no connections and adds it to routes with key 
        routeID.

        Arguments:
            station (Station): The root station of the route
        
        Returns (Route): The newly created route.
        """
        newRoute = Route(station, self.routeID)
        self.routeID += 1
        
        self.routes[newRoute.getID()] = newRoute

        return newRoute

    def listRoutesWithLegal(self, tMax: float):
        """
        Returns a list of all routes that have legal moves.

        Args:
            tMax: The maximum time a route can have.
        """
        # get all routes from the list of routes and take only those with legal moves
        return [route for _, route in self.routes.items() if route.hasLegalMoves(tMax)]

    def nRoute(self) -> int:
        """
        Returns (int) the amount of currently active routes
        """
        return len(self.routes)

    def getRoute(self, routeID: int) -> Route:
        """
        returns the route with routeID

        Args:
            routeID (int): the unique identifier of the route.
        """
        return self.routes[routeID]

    def delRoute(self, routeID: int):
        """
        Removes a route from routes.

        Args:
            routeID (int): the unique identifier of the route.
        """
        # remove all routeID's from all stations and routes in route
        self.routes[routeID].empty()

        self.routes.pop(routeID)

    def listRoutes(self) -> List[Route]:
        """
        Returns a list of all route objects.
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
        
        # enforces unique filenames
        timeStamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        with open(f"results/{timeStamp}-{filename}.csv", "w") as resultFile:
            resultFile.write("train,stations\n")

            for _, route in self.routes.items():
                resultFile.write(f"{route}\n")
            
            resultFile.write(f"score,{self.score()}")


    def connectionPoints(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Returns coordinate pairs for all rail connections for visualization
        """
        pointPairs = []
        
        for connection in self.connections:
            pointPairs.append(connection.connectionPoints())
        
        return pointPairs
    
    def stationPoints(self) -> List[Tuple[str, Tuple[float, float]]]:
        """
        Returns name coordinate pairs for all stations for visualization
        """
        points = []
        
        for station in [entry[1] for entry in self.stations.items()]:
            points.append(station.name(), station.position())
        
        return points
    
    def routePointLists(self) -> List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Returns a list of coordinate pairs for connections of all rail routes for visualization
        """
        routePointLists = []
        
        for _, route in self.routes.items():
            routePointLists.append(route.connectionPoints())
        
        return routePointLists

    # Check methods
    def checkValidSolution(self, tMax: float) -> bool:
        """
        Checks if all stations are serviced and all routes are legal
        
        Args:
            tMax (float): The maximum duration of a route.
        
        Returns (bool): True if all stations have a route and all routes are shorter than tMax and 
                        are continuous.
        """
        if self.checkStationCoverage() and self.checkLegalRoutes(tMax):
            return True
        
        return False

    def hasLegalMoves(self, tMax: float, maxRoutes: int) -> bool:
        """
        Checks if any route has legal moves. A move is legal if it has a station that can make a
        connection without going over tMax.
        
        Args:
            tMax (float): The maximum duration of a route.
            maxRoutes (int): The maximum amount of routes.
        
        Returns (bool): True if the amount of routes is below maxRoutes or if any route has legal 
                        moves. Else false
        """
        if len(self.routes) < maxRoutes:
            return True
        
        for _, route in self.routes.items():
            if not route.hasLegalMoves(tMax):
                return False
        
        return True

    def checkStationCoverage(self) -> bool:
        """
        Returns True if all stations have routes going through them, else false
        """
        for _, station in self.stations.items():
            if not station.isConnected():
                return False
        
        return True
    
    def checkLegalRoutes(self, tMax: float) -> bool:
        """
        Checks if all routes are legal. A route is legal if it shorter than tMax and is continuous.

        Returns (bool): True if all routes are legal, else False
        """
        for _, route in self.routes.items():
            if route.brokenConnections() or route.duration() >= tMax:
                return False
        return True
    
    def connectionCoverage(self) -> float:
        """
        Returns (float): the fraction of connections that have routes going over them
        """
        usedConnections = 0

        for connection in self.connections:
            if connection.isConnected():
                usedConnections += 1
        
        return usedConnections / len(self.connections)

    def totalDuration(self) -> float:
        """returns (float): the total duration of the routes"""
        totalDuration = 0

        for _, route in self.routes.items():
            totalDuration += route.duration()
        
        return totalDuration

    def getConnectedStation(self, fromStation, toStation) -> Station:
        """
        Returns the connected station object of a station
        """
        return self.stations[fromStation].getConnectedStation(toStation)