import random
import datetime
import time

from copy import deepcopy
from math import exp, log10

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Dict, Union, Callable


import algorithms.random_hajo as randomAlgorithm

"""
"""

START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def routeHillclimber(
    network: RailNetwork, 
    **parameters
) -> RailNetwork:
    """
    Runs the annealing climber as a standard hillclimber
    """
    return annealingClimber(
        network, 
        stepFunction = routeClimb,
        annealingFunction = hillClimbCoolingScheme, 
        initialTemperature = 0,
        coolingConstant = 0,
        **parameters
    )


def runAnnealing(network: RailNetwork, stepFunction: str, coolingScheme: str, **parameters
) -> RailNetwork:
    """
    Runs the annealing hillclimber with the selected stepfunction and cooling scheme
    """
    COOLING_SCHEMES: Dict[str, Callable[[float, float, int, float], bool]] = \
    {
        "logarithmic": logarithmicCooling,
        "geometric": geometricCooling,
        "linear": linearCooling,
    }

    STEP_FUNCTIONS: Dict[str, Callable[[RailNetwork, int, float]]] = \
    {
        "route": routeClimb
    }
    
    return annealingClimber(
        network, 
        stepFunction = STEP_FUNCTIONS[stepFunction], 
        annealingFunction = COOLING_SCHEMES[coolingScheme], 
        **parameters
    )


def annealingClimber(
    network: RailNetwork, 
    maxRoutes: int, 
    maxDuration: float,
    stepFunction: Callable[[RailNetwork, int, float], None],
    annealingFunction: Callable[[float, float, int, float], bool],
    initialTemperature: float = 0,
    coolingConstant: float = 0,
    targetFolder: str ="results", 
    runName: str = "soluionHill", 
    convergenceLimit: int = 5000,
    randomIterations: int = 5000, 
    recordAll: bool = False,
    exportImprovements: bool = True
) -> RailNetwork:
    """
    A hillclimber that takes any network and attempts to optimize it by adding, removing or 
    replacing random routes. Base for a simulated annealing algorithm

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
    iteration = 0

    bestNetwork = network
    scores: List[Dict[str, Union[int, float]]] = []
    
    if randomIterations:
        print("generating random solution")
        bestNetwork = randomAlgorithm.randomSolution(
            network,
            maxRoutes,
            maxDuration,
            randomIterations
        )

    currentNetwork = bestNetwork
    highestScore = bestNetwork.score()
    currentScore = highestScore

    scores.append({"iteration":iteration, "score":highestScore})
    
    iteration = 1

    while convergence <= convergenceLimit:
        print(f"iteration: {iteration}")

        workNetwork = deepcopy(currentNetwork)
        stepFunction(workNetwork, maxRoutes, maxDuration)
        newScore = workNetwork.score()
        
        # score >= highest or annealingFunction returns True
        if newScore > highestScore:
            print(f"new best found: {newScore}")

            highestScore = newScore
            bestNetwork = workNetwork

            workNetwork.exportSolution(targetFolder, f"{runName}-{iteration}") if exportImprovements\
                else None
            
        if newScore >= currentScore:
            currentNetwork = workNetwork
            currentScore = newScore
            convergence = 0
            
            scores.append({"iteration":iteration, "score":newScore})
        
        elif annealingFunction(
                (highestScore - newScore), 
                initialTemperature,
                iteration,
                coolingConstant,
            ):
            currentNetwork = workNetwork
            scores.append({"iteration":iteration, "score":newScore})

        # If all scores are to be tracked, append iteration and score to scores
        elif recordAll:
            scores.append({"iteration":iteration, "score":newScore})

        convergence += 1
        iteration += 1

    bestNetwork.exportSolution(targetFolder, runName + "_best", START_TIMESTAMP)

    scores.append({"iteration":"Best", "score":highestScore})
    scores.append({"iteration":"Theoretical max", "score": network.theoreticalMaxScore(maxDuration)})
    randomAlgorithm.exportScores(scores, targetFolder, runName, START_TIMESTAMP)

    print(f"Terminating with highest score {highestScore}")
    return bestNetwork

# Stepfunction
def routeClimb(network: RailNetwork, maxRoutes: int, maxDuration: float) -> None:
    """
    Either adds, removes or replaces a random route.

    Args:
        network (RailNetwork):
        maxRoutes (maxRoutes):
        maxDuration (maxDuration):
    
    post: The argument network will have a route replaced, added or removed.
    """
    randomNum = random.random()

    if randomNum <= 0.125 and network.nRoute() > 1:
        removeRoute(network)
        return
    
    # add a random route if 0.25 < randomNum <=0.50 or if a route could not be removed
    if (randomNum <= 0.25 and network.nRoute() < maxRoutes) or network.nRoute() == 0:
        randomAlgorithm.randomRoute(network, maxDuration)
        return

    removeRoute(network)
    randomAlgorithm.randomRoute(network, maxDuration)
    
    return


def removeRoute(network: RailNetwork):
    randomRoute = random.choice(network.listRoutes())
    network.delRoute(randomRoute.getID())


def hillClimbCoolingScheme(*_):
    """Always returns false, as a true hillclimber does not accept worse results"""
    return False


def annealingProbability(scoreDiff: float, temperature: float):
    """
    Determines whether an inferior score is accepted based on score difference and temperature.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """

    probability = exp(-(scoreDiff / temperature))
    if random.random() <= probability:
        return True
    
    return False


def logarithmicCooling(scoreDiff:float, _: float, iteration: int, constant: float):
    """
    Decreases temperature logarithmically over iterations.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = constant / log10(1 + iteration)

    return annealingProbability(scoreDiff, currentTemperature)


def geometricCooling(scoreDiff:float, initialTemp: float, iteration: int, powerBase: float) -> bool:
    """
    Decreases temperature geometrically over iterations.
    
    Args:
        scoreDiff (float): Difference in score between the old state and the new state.
        initialTemp (float): the initial temperature of the annealing function
        

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = initialTemp * (powerBase ** iteration)

    return annealingProbability(scoreDiff, currentTemperature)


def linearCooling(scoreDiff:float, initialTemp: float, iteration: int, coolingSpeed: float) -> bool:
    """
    Decreases temperature linearily over iterations.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = initialTemp - coolingSpeed * iteration

    if currentTemperature <= 0:
        return False
    
    return annealingProbability(scoreDiff, currentTemperature)