from algorithms.random_hajo import randomSolution

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Tuple, Any

import random
from copy import deepcopy

tMax = 180
routeMax = 20
iterations = 0

class HillClimber():

    def __init__(self):
        self.workModel = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), routeMax, tMax, 50)
        self.routes = self.workModel.listRoutes()
        
        self.previousModel = deepcopy(self.workModel)
        self.score = self.previousModel.score()


    def getLowestScoringRoute(self):
        """
        Returns lowest scoring route in railNetwork
        """
        lowestScore = 10000
        lowestRoute = self.routes[0].routeScore(len(self.workModel._connections))
        for route in self.routes:
            if route.routeScore(len(self.workModel._connections)) < lowestScore:
                lowestScore = route.routeScore(len(self.workModel._connections))
                lowestRoute = route
                
        return lowestRoute.getID()
        
        
    def removeLowestRoute(self, routeID):
        """
        Removes the route from the list with the lowest score.
        """
        self.workModel.delRoute(routeID)
        
    def makeNewRoute(self, routeID):
        """
        Creates a new route with a legal amount of stations.
        """
        # get id of emptied route
        # insert into emptied list while possible
        
        newRoute = Route((random.choice(self.workModel.listUnvisitedStations())), routeID)
        self.workModel._routes[newRoute.getID()] = newRoute
        options = newRoute.getLegalMoves(tMax)
        index = random.choice(list(options.keys()))
        while newRoute.hasLegalMoves(tMax) and random.random() < 0.15:
            # currentStation = newRoute.listStations()[-1]
            # newRoute.appendStation(random.choice(currentStation.listStations()))
            newRoute.appendStation(random.choice(options[index])[0])


    def checkSolution(self) -> None:
        """
        Checks and accepts better solutions than current solution.
        """

        newScore = self.workModel.score()
        oldScore = self.previousModel.score()

         # We are looking for the highest possible K
        if newScore > oldScore:
            self.score = newScore
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()

    def run(self, iterations: int = 500, verbose=False) -> None:
        """
        run
        """        
        
        while 1: 
            routeID = self.getLowestScoringRoute()
            self.removeLowestRoute(routeID)
            self.makeNewRoute(routeID)
            self.checkSolution()
