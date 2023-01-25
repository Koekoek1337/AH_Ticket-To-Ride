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
        
        
    def removeLowestRoute(self):
        """
        Removes the route from the list with the lowest score.
        """
        print(self.calculateScore())
        self.workModel.delRoute(self.calculateScore())
        print(self.routes)
        # if list empty, yeet
        
    def makeNewRoute(self):
        """
        Creates a newRoute with as many stations until there is no legal move left.
        """
        newRoute = RailNetwork()
        newRoute.createRoute(random.choice(newRoute.listStations()))
        while newRoute < hasLegalMoves(tMax):
            newRoute.appendStation(random.choice(newRoute.getLegalMoves(tMax)))

        return newRoute

    def addNewRoute(self, newRoute):
        """
        Adds the newRoute the list of routes.
        """
        self.routes.append(newRoute)


    def checkSolution(self, newRoute: List[List[str]]) -> None:
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

    def run(self, iterations: int = 500, verbose=False) -> None:
        """
        run
        """        
        
        while 1: 
            print("hello, world")
            self.addNewRoute(self.generateNewRoute())