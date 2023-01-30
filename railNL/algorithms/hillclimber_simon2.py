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
        model = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), 20, 180, 50)
        workModel = deepcopy(model)
        self.previousModel = deepcopy(workModel)
        self.workModel = workModel
        self.routes = workModel.listRoutes()
        self.score = workModel.score()
        self.scores: List[Dict[str, Union[int, float]]] = []
        self.iteration = 0


    def mutateRoute(self) -> None:
        """
        Random choice between removing first three or last three station for every route taken.
        Than adds a new station to the route.
        """
        self.previousModel = deepcopy(self.workModel)

        # mutate every route in the workModel
        for route in self.workModel.listRoutes():
            randomFloat = random.random()
            if route.nStations() < 2:
                self.lengthenRoute(route)
            if randomFloat < 0.33:
                self.mutateLastStation(route)
                self.mutateLastStation(route)
                self.mutateLastStation(route)
            elif randomFloat > 0.67:
                self.mutateFirstStation(route)
                self.mutateFirstStation(route)
                self.mutateFirstStation(route)
            else:
                self.lengthenRoute(route)
                self.lengthenRoute(route)
                self.lengthenRoute(route)



    def mutateLastStation(self, route) -> List[str]:
        """
        Input is a route (minus the last station)
        Output: adds a station to the route and makes it a newRoute
        """
        newRoute = route

        # if trainroute is empty, deletes route
        if newRoute.nStations() == 0:
            return

        # pop last station
        newRoute.popStation()

        # if trainroute is empty, deletes route
        if newRoute.nStations() == 0:
            return

        # if there are no legal moves possible, skips this function
        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))
        randomFloat = random.random()

        # add new station as last station
        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])

        # add new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])
        else:
            return

        return newRoute


    def mutateFirstStation(self, route) -> List[str]:
        """
        Input is a route (minus the first station)
        Output: adds a station to the route and makes it a newRoute
        """
        newRoute = route

        # if trainroute is empty, deletes route
        if newRoute.nStations() == 0:
            return

        # pop first station
        newRoute.popStation(0)

        # if trainroute is empty, deletes route
        if newRoute.nStations() == 0:
            return

        # if there are no legal moves possible, skips this function
        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))

        # add new station to last station
        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])

        # add new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])

        else:
            return

        return newRoute


    def lengthenRoute(self, route):
        """
        Adds a station to the route, if it is still under tMax.
        """
        newRoute = route
        if newRoute.nStations() == 0:
            return

        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))

        # add new station as last station
        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])

        # add new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])

        else:
            return

        return newRoute


    def checkSolution(self, newRoutes: List[List[str]]) -> None:
        """
        Checks and accepts better solutions than current solution.
        """
        newScore = self.workModel.score()
        oldScore = self.score

        # We are looking for the highest possible K
        if newScore >= oldScore:
            self.score = newScore
            self.scores.append({"iteration":self.iteration, "score":newScore})
            self.workModel.exportSolution("hillClimber2Simon2", "snake2Climber1")
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()


    def run(self, iterations: int = 500000, verbose=False, mutate_nodes_number=1) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.iterations = iterations

        for iteration in range(iterations):

            # Accept it if it is better
            self.checkSolution(self.mutateRoute())
            self.iteration += 1

        # exports scores
        exportScores(self.scores, "hillClimber2Simon2", "snake2Climber1", START_TIMESTAMP)
