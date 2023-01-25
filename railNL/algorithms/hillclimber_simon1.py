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

        print(self.workModel)



    def mutateRoute(self) -> None:
        """
        Random choice between removing first or last station for every route taken.
        Than adds a new station to the route.
        """
        self.previousModel = deepcopy(self.workModel)
        for route in self.routes:
            randomFloat = random.random()
            if randomFloat < 0.33:
                self.mutateLastStation(route)
            elif randomFloat > 0.67:
                self.mutateFirstStation(route)
            else:
                self.lengthenRoute(route)



    def mutateLastStation(self, route) -> List[str]:
        """
        Input is a route (minus the last station)
        Output: adds a station to the route and makes it a newRoute
        """
        newRoute = route
        # pop last two station
        newRoute.popStation()
        newRoute.popStation()


        if newRoute.nStations() == 0:
            self.workModel.delRoute(newRoute.getID())

        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))
        randomFloat = random.random()
        # new two last station connects to a new station

        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])
            newRoute.appendStation(random.choice(options[index])[0])


        # or add two new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])
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
        # pop first two station
        newRoute.popStation(0)
        newRoute.popStation(0)

        if newRoute.nStations() == 0:
            self.workModel.delRoute(newRoute.getID())

        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))

        # add two new station to last station
        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])
            newRoute.appendStation(random.choice(options[index])[0])


        # or add two new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])
            newRoute.insertStation(0, random.choice(options[index])[0])


        else:
            return

        print(newRoute)
        return newRoute

    def lengthenRoute(self, route):
        """
        Adds a station to the route, if it is still under tMax.
        """
        newRoute = route
        if not newRoute.hasLegalMoves(180):
            return

        options = newRoute.getLegalMoves(180)
        index = random.choice(list(options.keys()))

        if index > 0:
            newRoute.appendStation(random.choice(options[index])[0])

        # or add new station as first station
        elif index == 0:
            newRoute.insertStation(0, random.choice(options[index])[0])

        else:
            return

        return newRoute


    def checkSolution(self, newRoutes: List[List[str]]) -> None:
        """
        Checks and accepts better solutions than current solution.
        """
        print (self.routes)
        newScore = self.workModel.score()
        oldScore = self.score
        print (oldScore)
        print (newScore)

        # We are looking for the highest possible K
        if newScore >= oldScore:
            self.score = newScore
            self.scores.append({"iteration":self.iteration, "score":newScore})
            self.workModel.exportSolution("hillClimberSimon1", "snake2Climber")
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()

        print(newScore)
        print(self.workModel)


    def run(self, iterations: int = 500000, verbose=False, mutate_nodes_number=1) -> None:
        """
        Runs the hillclimber algorithm for a specific amount of iterations.
        """
        self.iterations = iterations

        for iteration in range(iterations):
            # Nice trick to only print if variable is set to True
            print(f'Iteration {iteration}/{iterations}, current value: {self.score}') if verbose else None

            # self.mutateRoute()

            # Accept it if it is better
            self.checkSolution(self.mutateRoute())
            self.iteration += 1

        exportScores(self.scores, "hillClimberSimon1", "snake2Climber", START_TIMESTAMP)
