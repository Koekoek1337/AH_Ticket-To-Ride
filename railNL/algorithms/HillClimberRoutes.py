import algorithms.random_hajo
from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

import random
from copy import deepcopy

tMax = 180
routeMax = 20

class HillClimberRoutes():
    
    def __init__(self):
        if not routes.checkValidSolution():
            raise Exception("HillClimber requires a complete solution.")

            model = randomSolution(RailNetwork("data/.csv", "data/.csv"), routeMax, tMax, 50)
            workModel = deepcopy(model)
            self.previousModel = deepcopy(workModel)
            self.workModel = workModel
            self.routes = workModel.listRoutes()
            self.score = workModel.score()
    
    def nRoutesReasonable(self):
        """
        Rebuilds a random railNetwork if initial railNetwork has
        less than (.70 * routeMax) routes.
        """
        while len(self.routes) < (int(0.70 * routeMax)):
        if not routes.checkValidSolution():
            raise Exception("HillClimber requires a complete solution.")
            model = randomSolution(RailNetwork("data/.csv", "data/.csv"), routeMax, tMax, 50)
            workModel = deepcopy(model)
            self.previousModel = deepcopy(workModel)
            self.workModel = workModel
            self.routes = workModel.listRoutes()
            self.score = workModel.score()
    
    def changeRoutesNetwork(self):
        """
        Creates a new railNetwork by removing the poorest scoring route
        and replacing it by the same amount of routes
        """
        pass
        
    
    def fairNetworkComparison(self):
        """
        NOT IN USE
        Calculates new network score if it had the same
        amount of routes as the old route:
        (newScore * (oldNRoutes / newNRoutes))
        Used when nRoutes changes
        
        """
        pass


    def generateScores(self):
        """
        Generates scores of routes in railNetwork
        """
        pass
    
     
    def findLowestScore(self):
        """
        Finds lowest score in railNetwork
        """
        pass
    
    def compareLowestToNewRoute(self):
        """
        Generate a new route and compare it to
        the route with the lowest score
        """
        pass
        
    def replaceLowestScore(self):
        """
        Replace lowest scoring route in railNetwork
        with newly generated route
        
        """
        pass
        
    def run(self):
        nRoutesReasonable()
        print("hello, world")