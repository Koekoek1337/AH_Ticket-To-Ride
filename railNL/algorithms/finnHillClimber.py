from algorithms.random_hajo import randomSolution, randomRoute, exportScores

from classes.railNetwork import RailNetwork
from classes.route import Route
import datetime

from typing import List, Dict, Union

from copy import deepcopy


class routeHillClimber():

    def __init__(self, network: RailNetwork, maxDuration, maxRoutes, runName, targetFolder, randomIterations) -> None:
        self.workModel: RailNetwork = randomSolution(network, maxRoutes, maxDuration, randomIterations)
        self.routes: List[Route] = self.workModel.listRoutes()
        self.score: float = self.workModel.score()
        self.previousModel: RailNetwork = deepcopy(self.workModel)
        self.iteration: int = 0
        self.attempts: int = 0
        self.scoreList: List[Dict[str, Union[int, float]]] = []
        self.tMax = maxDuration
        self.routeMax = maxRoutes
        self.runName = runName
        self.targetFolder = targetFolder
        self.START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

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

        randomRoute(self.workModel, self.tMax)

    def checkSolution(self) -> None:
        """
        Checks current railNetwork against the previous best railNetwork.
        Replaces previous best railNetwork if the current is better.
        """

        newScore = self.workModel.score()
        oldScore = self.score

        # Goal: highest K value
        if newScore > oldScore:
            print(f"New High Score: {newScore}")
            self.score = newScore
            self.scoreList.append({"iteration": self.iteration, "score": newScore})
            self.attempts = 0

        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()
            self.attempts += 1

    def run(self, verbose: bool = False) -> None:
        """
        Runs a route-based Hill Climber algorithm and exports the results.
        """
        print("New attempt")
        while self.attempts < 15000:
            routeID = self.getLowestScoringRoute()
            self.removeLowestRoute(routeID)
            self.makeNewRoute(routeID)
            self.checkSolution()
            self.iteration += 1

        print(f"Final Score: {self.workModel.score()}")
        self.workModel.exportSolution(self.targetFolder, self.runName)
        exportScores(self.scoreList, self.targetFolder, self.runName,
                     self.START_TIMESTAMP)

def main(network, runName, targetFolder, maxRoutes, maxDuration, randomIterations=50) -> RailNetwork:
    model = routeHillClimber(network, maxDuration, maxRoutes, runName, targetFolder, randomIterations)
    model.run()
    return model.workModel
