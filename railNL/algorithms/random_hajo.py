import random
from copy import deepcopy

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

"""
Currently gitignored
"""

def main(network: RailNetwork, maxRoutes: int, tMax):
    attempt = 1

    while True:
        print(f"attempt: {attempt}")

        workNetwork = deepcopy(network)

        randomAlgorithm(workNetwork, maxRoutes, tMax)

        if workNetwork.checkValidSolution(tMax):
            print(f"Solution found: {workNetwork.score()}")
            workNetwork.exportSolution("results/randomNat", "solution")
        else:
            print("Invalid solution")

        attempt += 1
        print("retrying")


def randomAlgorithm(network: RailNetwork, maxRoutes: int, tMax: int):
    
    nRoutes = random.randint(1, maxRoutes)

    for _ in range(nRoutes):
        route = network.createRoute(random.choice(network.listStations()))

        route.appendStation(
                            random.choice(
                                          [station for station, *_ in route.listStations()[0].listStations()]
                                        )
                          )

    while not network.checkValidSolution(tMax) and network.hasLegalMoves(tMax, nRoutes):
        route = random.choice(network.listRoutesWithLegal(tMax))

        moves = route.getLegalMoves(tMax)
        
        index = random.choice(list(moves.keys()))

        if index == 0:
            route.insertStation(index, random.choice(moves[index])[0])
        
        else:
            route.appendStation(random.choice(moves[index])[0])
    
    return network