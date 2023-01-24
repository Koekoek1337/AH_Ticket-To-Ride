import random
from copy import deepcopy
from typing import List, Tuple, Any

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
from algorithms.random_hajo import randomSolution


class HillClimber():

    def __init__(self):
        # Check if there is a valid solution
        # if not routes.checkValidSolution():
        #     raise Exception("HillClimber requires a complete solution.")
        model = randomSolution(RailNetwork("data/StationsNationaal.csv", "data/ConnectiesNationaal.csv"), 20, 180, 50)
        workModel = deepcopy(model)
        self.previousModel = deepcopy(workModel)
        self.workModel = workModel
        self.routes = workModel.listRoutes()
        self.score = workModel.score()
        print(self.workModel)



    def mutateRoute(self) -> None:
        """
        Random choice between removing first or last station for every route taken.
        Than adds a new station to the route.
        """
        self.previousModel = deepcopy(self.workModel)
        for route in self.routes:
            randomFloat = random.random()
            if randomFloat < 0.5:
                self.mutateLastStation(route)
            else:
                self.mutateFirstStation(route)


    def mutateLastStation(self, route) -> List[str]:
        """
        Input is a route (minus the last station)
        Output: adds a station to the route and makes it a newRoute
        """
        newRoute = route
        # pop last station
        newRoute.popStation()
        randomFloat = random.random()
        # new last station connects to a new station
        if randomFloat < 0.5:
            newRoute.appendStation(random.choice(newRoute.listStations()))
        # or add new station as first station
        else:
            newRoute.insertStation(0, random.choice(newRoute.listStations()))

        #  Checks if the newRoute is still valid, if not returns old route
        # if Railnetwork().checkValidSolution(newRoute):
        #     return newRoute
        # else:
        #     return route
        return newRoute


    def mutateFirstStation(self, route) -> List[str]:
        """
        Input is a route (minus the first station)
        Output: adds a station to the route and makes it a newRoute
        """
        newRoute = route
        # pop first station
        newRoute.popStation(0)
        randomFloat = random.random()
        # add new station to last station
        if randomFloat < 0.5:
            newRoute.appendStation(random.choice(newRoute.listStations()))
        # or add new station as first station
        else:
            newRoute.insertStation(0, random.choice(newRoute.listStations()))

        # if newRoute.checkValidSolution():
        #     return newRoute
        # else:
        #     return route
        print(newRoute)
        return newRoute


    # def combine_newRoute(self, newRoute: List[str]) -> List[List[str]]:
    #     """
    #     Creates a list of all the new Routes.
    #     """
    #     newRoutes = []
    #     newRoutes.append(newRoute)
    #     print(newRoutes)
    #     return newRoutes


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
        else:
            self.workModel = self.previousModel
            self.routes = self.previousModel.listRoutes()

        print(newScore)
        print(self.workModel)


    def run(self, iterations: int = 50000, verbose=False, mutate_nodes_number=1) -> None:
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
