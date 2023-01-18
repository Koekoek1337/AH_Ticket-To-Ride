from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

import random


def main():
    model = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv")
    # Starts a route at a random station.
    model.createRoute(random.choice(model.listStations()))

    model.nRoute() <= 7

    # Continue the routes until it satisfies the solution or exceed the timelimit.
    while not model.checkValidSolution(model.duration()) and (model.nRoute() <=7):
        # The route connects to a random station to who it is connected.
        currentRoute = random.choice(model.listRoutes())
        current_station = currentRoute.listStations()[-1]
        new_station = random.choice(current_station.listStations())
        currentRoute.appendStation(new_station)

        #  If there are not 7 trajects, there is a random chance, that the route conitinues or a new traject is made.
        if model.nRoute() < 7:
            if model.validMoves() == True:
                randomFloat = random.random()
                if randomFloat <= 0.2:
                    model.createRoute(random.choice(model.listStations()))
                else:
                    continue
            else:
                continue


    print(model)

    exportSolution("random")
