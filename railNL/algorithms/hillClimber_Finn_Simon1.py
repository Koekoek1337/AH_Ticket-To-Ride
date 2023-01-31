import random
from copy import deepcopy
from typing import List, Tuple, Any, Dict, Union
import datetime

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
from algorithms.random_hajo import randomSolution, exportScores, randomRoute
# from algorithms.finnHillClimber import routeHillClimber


START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tMax = 180
routeMax = 20

class HillClimber():


    def __init__(self):
        model = randomSolution(RailNetwork("data/StationsMinGroningen.csv", "data/ConnectiesMinGroningen.csv"), 20, 180, 50)
        workModel = deepcopy(model)
        self.previousModel = deepcopy(workModel)
        self.workModel = workModel
        self.routes = workModel.listRoutes()
        self.score = workModel.score()
        self.scores: List[Dict[str, Union[int, float]]] = []
        self.iteration = 0


    def ReplaceOrMutate(self):
        """
        Makes a choice between replace the lowest score route, or mutate a Route.
        """
        self.previousModel = deepcopy(self.workModel)

        if self.workModel.nRoute() < 7:
            routeID = self.getLowestScoringRoute()
            self.removeLowestRoute(routeID)
            self.makeNewRoute(routeID)

        else:
            if random.random() < 0.5:
                self.mutateRoute()
            else:
                routeID = self.getLowestScoringRoute()
                self.removeLowestRoute(routeID)
                self.makeNewRoute(routeID)


    def getLowestScoringRoute(self) -> int:
        """
        Returns route with only one station or
        lowest scoring route in railNetwork.
        """
        self.previousModel = deepcopy(self.workModel)
        lowestScore: float = 10000
        lowestRoute: Route = self.routes[0]
        for route in self.workModel.listRoutes():
            if route.nStations == 1:
                return route.getID()
            if route.routeScore(len(self.workModel._connections)) < lowestScore:
                lowestScore = route.routeScore(len(self.workModel._connections))
                lowestRoute = route
        return lowestRoute.getID()

    def removeLowestRoute(self, routeID: int) -> None:
        """
        Removes route from the railNetwork with the lowest score.
        """

        self.workModel.delRoute(routeID)

    def makeNewRoute(self, routeID: int) -> None:
        """
        Creates a new route with a legal amount of stations.
        """

        randomRoute(self.workModel, tMax)


    def mutateRoute(self) -> None:
        """
        Random choice between removing first three or last three station for every route taken.
        Than adds a new station to the route.
        """
        # self.previousModel = deepcopy(self.workModel)

        # mutate every route in the workModel
        for route in self.workModel.listRoutes():
            if route.nStations() < 2:
                self.lengthenRoute(route)
            randomFloat = random.random()
            if randomFloat < 0.33:
                for _ in range(random.randint(1,3)):
                    self.mutateLastStation(route)
            elif randomFloat > 0.67:
                for _ in range(random.randint(1,3)):
                    self.mutateFirstStation(route)
            else:
                for _ in range(random.randint(1,3)):
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
            print(self.score)
            self.scores.append({"iteration":self.iteration, "score":newScore})
            self.workModel.exportSolution("snakeRouteClimberGroningen9", "hillClimber1SimonFinn1")
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()


    def run(self, iterations: int = 30000, verbose=False, mutate_nodes_number=1) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.iterations = iterations

        for iteration in range(iterations):

            # Accept it if it is better
            self.checkSolution(self.ReplaceOrMutate())
            self.iteration += 1

        # exports scores
        exportScores(self.scores, "snakeRouteClimberGroningen9", "hillClimber1SimonFinn1", START_TIMESTAMP)
