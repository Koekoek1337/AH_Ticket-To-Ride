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


    def __init__(self, model, maxRoutes: int, maxDuration: int, randomIterations: int, maxConvergence: int):
        # Takes a random solution
        model = randomSolution(model, maxRoutes, maxDuration, randomIterations)
        workModel = deepcopy(model)

        self.workModel = workModel
        self.previousModel = deepcopy(self.workModel)
        self.score = self.workModel.score()
        self.scores: List[Dict[str, Union[int, float]]] = []
        self.iteration = 0
        self.maxConvergence = 10000


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
                # removes last station
                route.popStation()
                if route.nStations() > 1:
                    route.popStation()
                    if route.nStations() > 1:
                        route.popStation()
                        self.lengthenRoute(route)
                    self.lengthenRoute(route)
                # add station
                self.lengthenRoute(route)
            elif randomFloat <= 0.67:
                # removes last station
                route.popStation(0)
                if route.nStations() > 1:
                    route.popStation(0)
                    if route.nStations() > 1:
                        route.popStation(0)
                        self.lengthenRoute(route)
                    self.lengthenRoute(route)
                # add station
                self.lengthenRoute(route)
            else:
                # add three station
                self.lengthenRoute(route)


        return self.workModel


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


    def checkSolution(self, newRoutes: List[List[str]]) -> None:
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
            self.convergence = 0


    def run(self, verbose=False, mutate_nodes_number=1) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.convergence = 0

        while self.convergence <= self.maxConvergence:

            # Accept it if it is better
            self.checkSolution(self.mutateRoute())
            self.iteration += 1
            self.convergence += 1

        # exports scores
        exportScores(self.scores, "snakeClimber2", "snakeClimber2", START_TIMESTAMP)


def main(network: RailNetwork, runName: str, targetFolder: str, maxRoutes: int, maxDuration: int, randomIterations: int, maxConvergence: int) -> RailNetwork:
    model = HillClimber(network, runName, targetFolder, maxRoutes, maxDuration, randomIterations, maxConvergence)
    model.run()
    return model.previousModel
