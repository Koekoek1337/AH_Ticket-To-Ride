from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

import random

tMax = 120
routeMax = 7    

def Random():
    iterations = 0
    model = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv")
    # Starts a route at a random station.
    model.createRoute(random.choice(model.listStations()))

    model.nRoute() <= 7

    # Continue the routes until it satisfies the solution or exceed the timelimit.
    while not model.checkValidSolution(tMax) and (model.hasLegalMoves(tMax, routeMax) and model.nRoute() <= routeMax):
        iterations += 1
        # The route connects to a random station to who it is connected.
        currentRoute = random.choice(model.listRoutes())
        current_station = currentRoute.listStations()[-1]
        new_station = random.choice(current_station.listStations())
        currentRoute.appendStation(new_station[0])

        #  If there are not 7 trajects, there is a random chance, that the route conitinues or a new traject is made.
        if model.nRoute() < routeMax:
            if model.hasLegalMoves(tMax, routeMax) == True:
                randomFloat = random.random()
                if randomFloat <= 0.2:
                    model.createRoute(random.choice(model.listStations()))
                else:
                    continue
            else:
                continue


    #print(f"total iterations: {iterations}")
    print(model.routes)

    #not working currently, keeping it for reference:
    #exportSolution("random")