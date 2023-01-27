from algorithms.random_hajo import randomSolution, randomRoute, exportScores

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
import datetime

from typing import List, Tuple, Any, Dict, Union

import random
from copy import deepcopy

tMax = 180
routeMax = 20

START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

class routeHillClimber():

    def __init__(self) -> None:
        self.workModel: RailNetwork = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), routeMax, tMax, 50)
        self.routes: List[Route] = self.workModel.listRoutes()
        self.score: float = self.workModel.score()
        
        self.previousModel: RailNetwork = deepcopy(self.workModel)
        self.scoreList: List[Dict[str, Union[int, float]]] = []
        self.iteration: int = 0


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
            self.scoreList.append({"iteration":self.iteration, "score":newScore})
            self.workModel.exportSolution("finnHillClimber", "hillClimber")

        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()

    def run(self, iterations: int = 10000, verbose: bool = False) -> None:
        """
        Runs a route-based Hill Climber algorithm and exports the results.
        """        
        for _ in range(iterations): 
            routeID = self.getLowestScoringRoute()
            self.removeLowestRoute(routeID)
            self.makeNewRoute(routeID)
            self.checkSolution()
            self.iteration += 1
            
        exportScores(self.scoreList, "finnHillClimber", "hillClimber", START_TIMESTAMP)