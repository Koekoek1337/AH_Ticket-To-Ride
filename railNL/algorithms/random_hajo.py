import random
from copy import deepcopy

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

def main(network: RailNetwork, maxRoutes: int, maxDuration: float, targetFolder: str ="results", 
         runName: str = "solution", convergenceLimit: int = 10000, recordAll: bool = False, 
         **_):
    
    convergence = 0
    attempt = 1
    highest = 0

    while convergence <= convergenceLimit:
        print(f"attempt: {attempt}")

        workNetwork = deepcopy(network)

        randomAlgorithm(workNetwork, maxRoutes, maxDuration)

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

def randomAlgorithm(network: RailNetwork, maxRoutes: int, maxDuration: int):
    
    nRoutes = random.randint(1, maxRoutes)

    for _ in range(nRoutes):
        randomRoute(network, maxDuration)
    
    return network


def randomRoute(network: RailNetwork, maxDuration: float):
    longestConnection = network.getLongestDuration()

    route = network.createRoute(random.choice(network.listStations()))

    while route.routeScore(network.nConnections()) <= 0:
        tTarget = random.randrange(round(longestConnection), round(maxDuration))

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


def randomSolution(network: RailNetwork, maxRoutes: int, maxDuration: float,
    convergenceLimit: int = 50000) -> RailNetwork:
    """
    Returns a randomly solved railNetwork for optimization
    """
    bestNetwork = network

    convergence = 0
    attempt = 1
    highest = 0

    while convergence <= convergenceLimit:
        workNetwork = deepcopy(network)

        randomAlgorithm(workNetwork, maxRoutes, maxDuration)

        newScore = workNetwork.score()
        if highest < newScore:
            highest = newScore
            bestNetwork = workNetwork
            convergence = 0

        convergence += 1

    return bestNetwork