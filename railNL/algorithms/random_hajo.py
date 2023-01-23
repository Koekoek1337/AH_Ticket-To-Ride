import random
from copy import deepcopy

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

def main(network: RailNetwork, maxRoutes: int, tMax: float, targetFolder: str ="results", 
         runName: str = "solution", convergenceLimit: int = 10000, recordAll: bool = False):
    
    convergence = 0
    attempt = 1
    highest = 0



    while convergence <= convergenceLimit:
        print(f"attempt: {attempt}")

        workNetwork = deepcopy(network)

        randomAlgorithm(workNetwork, maxRoutes, tMax)

        newScore = workNetwork.score()
        if highest < newScore:

            print(f"new best found: {newScore}")
            highest = newScore
            workNetwork.exportSolution(targetFolder, f"{runName}-{attempt}")
            convergence = 0
        
        elif recordAll:
            workNetwork.exportSolution(targetFolder, f"{runName}-{attempt}")

        if convergenceLimit:
            convergence += 1

        attempt += 1

        print("retrying")

def randomAlgorithm(network: RailNetwork, maxRoutes: int, tMax: int):
    
    nRoutes = random.randint(1, maxRoutes)

    for _ in range(nRoutes):
        randomRoute(network, tMax)
    
    return network


def randomRoute(network: RailNetwork, tMax: float):
    longestConnection = network.getLongestDuration()

    route = network.createRoute(random.choice(network.listStations()))

    while route.routeScore(network.nConnections()) <= 0:
        tTarget = random.randrange(round(longestConnection), round(tMax))

        route.empty()

        route.appendStation(random.choice(network.listStations()))

        route.appendStation(
                            random.choice(
                                        [station for station, *_ in route.listStations()[0].listStations()]
                                        )
                        )
        
        while route.hasLegalMoves(tTarget):
            moves = route.getLegalMoves(tTarget)
            
            index = random.choice(list(moves.keys()))

            if index == 0:
                route.insertStation(index, random.choice(moves[index])[0])
            
            else:
                route.appendStation(random.choice(moves[index])[0])
    
    return


def randomAlgorithmOld(network: RailNetwork, maxRoutes: int, tMax: int):
    
    nRoutes = random.randint(1, maxRoutes)

    for _ in range(nRoutes):
        route = network.createRoute(random.choice(network.listStations()))

        route.appendStation(
                            random.choice(
                                          [station for station, *_ in route.listStations()[0].listStations()]
                                        )
                          )

    while network.hasLegalMoves(tMax, nRoutes):
        route = random.choice(network.listRoutesWithLegal(tMax))

        moves = route.getLegalMoves(tMax)
        
        index = random.choice(list(moves.keys()))

        if index == 0:
            route.insertStation(index, random.choice(moves[index])[0])
        
        else:
            route.appendStation(random.choice(moves[index])[0])
    
    return network