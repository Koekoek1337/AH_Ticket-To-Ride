from algorithms.random_hajo import randomSolution, randomRoute

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Tuple, Any

import random
from copy import deepcopy

tMax = 180
routeMax = 20

class HillClimber():

    def __init__(self):
        self.workModel = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), routeMax, tMax, 50)
        self.routes = self.workModel.listRoutes()
        
        self.previousModel = deepcopy(self.workModel)
        self.score = self.workModel.score()


    def getLowestScoringRoute(self):
        """
        Returns lowest scoring route in railNetwork
        """
        self.previousModel = deepcopy(self.workModel)
        lowestScore = 10000
        lowestRoute = self.routes[0].routeScore(len(self.workModel._connections))
        for route in self.workModel.listRoutes():
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
        
        randomRoute(self.workModel, tMax)


    def checkSolution(self) -> None:
        """
        Checks and accepts better solutions than current solution.
        """

        newScore = self.workModel.score()
        oldScore = self.score

         # We are looking for the highest possible K
        if newScore > oldScore:
            self.score = newScore
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()

    def run(self, iterations: int = 100, verbose=False) -> None:
        """
        run
        """        
        for _ in range(iterations): 
            routeID = self.getLowestScoringRoute()
            self.removeLowestRoute(routeID)
            self.makeNewRoute(routeID)
            self.checkSolution()
            print(self.previousModel.score())
        print(self.routes)