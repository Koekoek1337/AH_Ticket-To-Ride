import random
import datetime
import time

from copy import deepcopy

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Dict, Union


import algorithms.random_hajo as randomAlgorithm

"""
"""

START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def routeHillclimber(network: RailNetwork, maxRoutes: int, maxDuration: float, 
    targetFolder: str ="results", runName: str = "soluionHill", convergenceLimit: int = 5000,
    randomIterations: int = 5000, recordAll: bool = False) -> RailNetwork:
    """
    A hillclimber that takes any network and attempts to optimize it by adding, removing or 
    replacing random routes.

    Args:
        network (RailNetwork):
        maxRoutes (int):
        maxDuration (float):
        targetFolder (str):
        runName (str):
        convergenceLimit (int):
        randomIterations (int):
        recordAll (bool):
    
    Returns: The optimized network
    """

    convergence = 0
    iteration = 1

    bestNetwork = network

    if randomIterations:
        print("generating random solution")
        bestNetwork = randomAlgorithm.randomSolution(network,
                                                     maxRoutes,
                                                     maxDuration,
                                                     randomIterations
                                                    )
        highestScore = bestNetwork.score()

    scores: List[Dict[str, Union[int, float]]] = []

    highestScore = bestNetwork.score()
    
    scores.append({"iteration":iteration, "score":highestScore})
    
    while convergence <= convergenceLimit:
        print(f"iteration: {iteration}")

        workNetwork = deepcopy(bestNetwork)
        climbStep(workNetwork, maxRoutes, maxDuration)

        newScore = workNetwork.score()
        
        # When a new highscore is found, print to terminal, export the solution and append the score
        # to the scorelist.
        # Convergence set back to zero.
        if newScore > highestScore:
            print(f"new best found: {newScore}")

            highestScore = newScore
            convergence = 0

            workNetwork.exportSolution(targetFolder, f"{runName}-{iteration}")
            scores.append({"iteration":iteration, "score":newScore})

        # If all scores are to be tracked, append iteration and score to scores
        elif recordAll:
            scores.append({"iteration":iteration, "score":newScore})

        iteration += 1
        convergence += 1

        randomAlgorithm.exportScores(scores, targetFolder, runName, START_TIMESTAMP)

    return bestNetwork


def climbStep(network: RailNetwork, maxRoutes: int, maxDuration: float) -> None:
    """
    Either adds, removes or replaces a random route.

    Args:
        network (RailNetwork):
        maxRoutes (maxRoutes):
        maxDuration (maxDuration):
    
    post: The argument network will have a route replaced, added or removed.
    """
    randomNum = random.random()

    if randomNum <= 0.25 and network.nRoute() > 1:
        removeRoute(network)
        return
    
    # add a random route if 0.25 < randomNum <=0.50 or if a route could not be removed
    if (randomNum <= 0.50 and network.nRoute() < maxRoutes) or network.nRoute() == 0:
        randomAlgorithm.randomRoute(network, maxDuration)
        return

    removeRoute(network)
    randomAlgorithm.randomRoute(network, maxDuration)
    
    return


def removeRoute(network: RailNetwork):
    randomRoute = random.choice(network.listRoutes())
    network.delRoute(randomRoute.getID())