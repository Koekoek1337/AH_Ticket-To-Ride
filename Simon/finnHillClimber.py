import random
from copy import deepcopy
from typing import List, Tuple, Any

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
from algorithms.random_hajo import randomSolution


class HillClimber():

    def __init__(self):
        model = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), 20, 180, 50)
        workModel = deepcopy(model)
        self.previousModel = deepcopy(workModel)
        self.workModel = workModel
        self.routes = workModel.listRoutes()


    def calculateScore(self):
        """
        Calcutes the score of every route.
        """
        for route in self.routes:
            return route.score()

    def removeLowestRoute(self):
        """
        Removes the route from the list with the lowest score.
        """
        self.routes.delroute()

    def makeNewRoute(self):
        """
        Creates a newRoute with as many stations until there is no legal move left.
        """
        newRoute = RailNetwork()
        newRoute.createRoute(random.choice(newRoute.listStations()))
        while newRoute < hasLegalMoves(tMax):
            newRoute.appendStation(random.choice(newRoute.getLegalMoves(tmax)))

        return newRoute

    def addNewRoute(self, newRoute):
        """
        Adds the newRoute the list of routes.
        """
        self.routes.append(newRoute)


    def checkSolution(self, newRoutes: List[List[str]]) -> None:
        """
        Checks and accepts better solutions than current solution.
        """

        newScore = self.workModel.score()
        oldScore = self.score

         # We are looking for the highest possible K
        if newScore >= oldScore:
            self.score = newScore
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()
