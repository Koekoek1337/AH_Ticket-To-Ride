import random
from copy import deepcopy
from typing import List, Tuple, Any, Dict, Union
import datetime

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
from algorithms.random_hajo import randomSolution, exportScores

START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

class HillClimber():


    def __init__(self):
        # Takes a random solution
        model = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), 20, 180, 50)
        workModel = deepcopy(model)

        self.workModel = workModel
        self.previousModel = deepcopy(self.workModel)
        self.score = self.workModel.score()
        self.scores: List[Dict[str, Union[int, float]]] = []
        self.iteration = 0


    def mutateRoute(self) -> None:
        """
        Random choice between removing first or last station for every route taken.
        Than adds a new station to the route.
        """
        self.workModel = deepcopy(self.previousModel)

        # mutate every route in the workModel 
        for route in self.workModel.listRoutes():
            randomFloat = random.random()
            if randomFloat <= 0.33:
                route.popStation()
                self.lengthenRoute(route)
            elif randomFloat <= 0.67:
                route.popStation(0)
                self.lengthenRoute(route)
            else:
                self.lengthenRoute(route)

        return self.workModel


    # def mutateLastStation(self, route: List[str]) -> List[str]:
    #     """
    #     Input is a route (minus the last station)
    #     Output: adds a station to the route and makes it a route
    #     """
    #     # if trainroute is empty, deletes route
    #     if route.nStations() == 1:
    #         self.workModel.delRoute(route.getID())
    #         return
    #
    #     # pop last station
    #     route.popStation()
    #
    #     self.lengthenRoute(route)
    #
    #
    # def mutateFirstStation(self, route: List[str]) -> List[str]:
    #     """
    #     Input is a route (minus the first station)
    #     Output: adds a station to the route and makes it a route
    #     """
    #     # if trainroute is empty, deletes route
    #     if route.nStations() == 1:
    #         self.workModel.delRoute(route.getID())
    #         return
    #
    #     # pop first station
    #     route.popStation(0)
    #
    #     self.lengthenRoute(route)


    def lengthenRoute(self, route: List[str]) -> List[str]:
        """
        Adds a station to the route, if it is still under tMax.
        """
        if not route.hasLegalMoves(180):
            return

        options = route.getLegalMoves(180)
        index = random.choice(list(options.keys()))

        # add new station as last station
        if index > 0:
            route.appendStation(random.choice(options[index])[0])

        # add new station as first station
        elif index == 0:
            route.insertStation(0, random.choice(options[index])[0])


    def checkSolution(self, routes: List[List[str]]) -> None:
        """
        Checks and accepts better solutions than current solution.
        """
        newScore = self.workModel.score()
        oldScore = self.score

        # We are looking for the highest possible K
        if newScore >= oldScore:
            self.previousModel = self.workModel
            self.score = newScore
            self.scores.append({"iteration":self.iteration, "score":newScore})
            self.workModel.exportSolution("snakeClimber22", "snakeClimber")


    def run(self, iterations: int = 3000, verbose=False, mutate_nodes_number=1) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.iterations = iterations

        for iteration in range(iterations):

            # Accept it if it is better
            self.checkSolution(self.mutateRoute())
            self.iteration += 1

        print(f"p = {self.workModel.connectionCoverage()}")
        print(f"routes = {self.workModel.nRoute()}")
        print(f"total duration = {self.workModel.totalDuration()}")
        # exports scores
        exportScores(self.scores, "snakeClimber22", "snakeClimber", START_TIMESTAMP)
