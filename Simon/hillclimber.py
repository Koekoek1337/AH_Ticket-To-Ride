import random

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station


# voeg alle routes toe aan een lijst.
# Maak een kleine verandering van alle routes.
# Bereken het nieuwe punten totaal.
# Als het nieuwe punten totaal groter is, sla deze op

class HillClimber():

    def __init__(self, route):
        model = RailNetwork()
        self.routes = model.listRoutes()
        self.score = model.routes.score()


    def mutateStation(self):
        """
        Random choice between removing first or last station for every route taken.
        Than adds a new station to the route.
        """

        for route in self.routes:
            randomFloat = random.random()
            if randomFloat < 0.5:
                route.mutateLastStation()
            else:
                route.mutateFirstStation()


    def mutateLastStation(self):
        """
        Input is a route (minus the last station)
        Output: adds a station to the route and makes it a newRoute
        """

        # pop last station
        route.popStation()
        randomFloat = random.random()
        # new last station connects to a new station
        if randomFloat < 0.5:
            route.appendStation(random.choice(route.listStations()))
        # first station connects to a new station
        else:
            route.appendStation(0, random.choice(route.listStations()))

        route = newRoute

        return newRoute


    def mutateFirstStation(self):
        """
        Input is a route (minus the first station)
        Output: adds a station to the route and makes it a newRoute
        """
        # pop first station
        route.popStation(0)
        randomFloat = random.random()
        # add new station to last station
        if randomFloat < 0.5:
            route.appendStation(random.choice(route.listStations()))
        # or add new station as first station
        else:
            route.appendStation(0, random.choice(route.listStations()))

        route = newRoute

        return newRoute


    def combine_newRoute(self, newRoute):
        """
        Creates a list of all the new Routes.
        """
        newRoutes = []
        newRoutes.append(newRoute)

        return newRoutes


    def checkSolution(self, newRoutes):
        """
        Checks and accepts better solutions than current solution.
        """
        # TODO: mag pas oordelen als alle routes zijn veranderd.

        newScore = newRoutes.score()
        oldScore = self.score

        # We are looking for the highest possible K
        if newScore >= Score:
            self.routes = newRoutes
            self.score = newScore
