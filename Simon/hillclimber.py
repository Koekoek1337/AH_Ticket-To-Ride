import random

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station



class HillClimber():

    def __init__(self, station, connection):
        self.station = station
        self.connection = connection
        self.route = []
        self.score = totalRoute.score()


    # voeg alle routes toe aan een lijst.
    # Maak een kleine verandering van alle routes.
    # Bereken het nieuwe punten totaal.
    # Als het nieuwe punten totaal groter is, sla deze op


    def mutateStation():
        # random choice between removing first or last station.
        randomFloat = random.random()
        if randomFloat < 0.5:
            route.mutateLastStation()
        else:
            route.mutateFirstStation()


    def mutateLastStation():
        # pop last station
        route.popStation()
        randomFloat = random.random()
        # new last station connects to a new station
        if randomFloat < 0.5:
            route.appendStation(random.choice(route.listStations()))
        # first station connects to a new station
        else:
            route.appendStation(0, random.choice(route.listStations()))


    def mutateFirstStation():
        # pop first station
        route.popStation(0)
        randomFloat = random.random()
        # add new station to last station
        if randomFloat < 0.5:
            route.appendStation(random.choice(route.listStations()))
        # or add new station as first station
        else:
            route.appendStation(0, random.choice(route.listStations()))


    def checkSolution():
        """
        Checks and accepts better solutions than current solution.
        """
        # TODO: mag pas oordelen als alle routes zijn veranderd.

        newScore = newRoutes.score()
        oldScore = self.score

        # We are looking for the highest possible K
        if newScore >= Score:
            self.graph = new_graph
            self.score = newScore
