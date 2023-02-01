import random
import datetime

from copy import deepcopy
from math import exp, log10

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Dict, Union, Callable, Optional


import algorithms.random as randomAlgorithm

"""Module for a Simulated Annealing Hillclimber Algorithm

The algorithm can be ran via either runAnnealing to have acccess to the specified stepfunction and
cooling scheme, or via routeHillclimber to run the algorithm as a pure hillclimber with the route 
stepfunction.
"""


# Run macros
def runAnnealing(
        network: RailNetwork, 
        stepFunction: str = "route", 
        coolingScheme: str = "logarithmic", 
        **arguments
    ) -> RailNetwork:
    """
    Runs the annealing hillclimber with the selected stepfunction and cooling scheme.

    There is currently one stepfunction in this module:
        - "route": See routeClimb() for description

    There are currently three cooling schemes in this module:
        - "logarithmic": See logarithmicCooling() for description
        - "geometric": See geometricCooling() for description
        - "linear": See linearCooling() for description

    Args:
        network (RailNetwork): The railnetwork for which an optimized solution has to be found.
        stepFunction (str): The name of the stepfunction in this module to be used.
        coolingScheme (str): The name of the cooling scheme in this module to be used.
        **arguments: The keyword arguments for annealingClimber()
    """
    COOLING_SCHEMES: Dict[str, Callable[[float, float, int, float], bool]] = \
    {
        ""
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
        **arguments
    )


def routeHillclimber(
    network: RailNetwork, 
    **arguments
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
        **arguments
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
        randomIterations: int = 1000, 
        recordAll: bool = False,
        exportImprovements: bool = False
    ) -> RailNetwork:
    """
    Annealing hillclimber algorithm. Takes a stepfunction and an annealingFunction (analagous to
    cooling scheme) as arguments. Exports a score summary file, as well as the best solution 
    produced.

    Args:
        network (RailNetwork): The railnetwork for which an optimized solution has to be found.
        maxRoutes (int): The maximum amount of routes that can be used in the network
        maxDuration (float): The maximum duration of a single route.
        stepFunction (Callable): The function that makes steps through the statespace.
        annealingFunction (Callable): The function that determines whether a lower score is accepted
            as new state.
        initialTemperature (float): The initial temperature of the system. Is unused with
            logarithmic cooling.
        coolingConstant (float): A constant parameter that is defined in the annealingFunction. See
            logarithmicCooling(), geometricCooling() and linearCooling() for more information. 
        targetFolder (str): The folder where all output files are to be saved to.
        runName (str): The readable part of the filenames for the exported files and the score
            summary file.
        convergenceLimit (int): The maximum amount of iterations to run for without improvement
            before terminating the algorithm.
        randomIterations (int): For how many iterations the random algorithm should be ran for the
            best initial solution.
        recordAll (bool): Whether all scores should be recorded for the the score summary files or
            only the accepted states of the network.
        exportImprovements (bool): Whether to export every improvement
    
    Returns (RailNetwork): The optimized network
    """
    START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

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
        
        if not iteration % 1000:
            print(f"iteration: {iteration}")

        workNetwork = deepcopy(currentNetwork)
        stepFunction(workNetwork, maxRoutes, maxDuration)
        newScore = workNetwork.score()
        
        # if score > highest, update the best score
        if newScore > highestScore:
            print(f"new best found: {newScore}")

            highestScore = newScore
            bestNetwork = workNetwork

            workNetwork.exportSolution(targetFolder, f"{runName}-{iteration}") if exportImprovements\
                else None
        
        # if score > currentScore, update the currentNetwork    
        if newScore > currentScore:
            currentNetwork = workNetwork
            currentScore = newScore
            convergence = 0
            
            scores.append({"iteration":iteration, "score":newScore})
        
        # if score == currentScore or the annealingfunction returns true, update the currentNetwork
        elif newScore == currentScore \
            or annealingFunction(
                (currentScore - newScore), 
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

    # append two final datapoints
    scores.append({"iteration": iteration, "score": currentNetwork.score()})
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
    
    # add a random route if 0.125 < randomNum <=0.25 or if a route could not be removed
    if (randomNum <= 0.25 and network.nRoute() < maxRoutes) or network.nRoute() == 0:
        randomAlgorithm.randomRoute(network, maxDuration)
        return

    removeRoute(network)
    randomAlgorithm.randomRoute(network, maxDuration)
    
    return


def removeRoute(network: RailNetwork) -> None:
    """Removes a random route from the RailNetwork"""
    randomRoute = random.choice(network.listRoutes())
    network.delRoute(randomRoute.getID())


# Cooling schemes
def hillClimbCoolingScheme(*_):
    """
    Always returns false in order to use the annealing climber as a hillclimber
    """
    return False


def logarithmicCooling(scoreDiff:float, _: float, iteration: int, constant: float):
    """
    Decreases temperature logarithmically over iterations.

    Args:
        scoreDiff (float): The difference in score between two states
        _ (float): Positional placeholder
        iteration (int): The current iteration of the algorithm.
        constant (float): The constant number which determines the speed of the cooling

    Returns (bool): True if the score difference is accepted, else False.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = constant / log10(1 + iteration)

    return annealingProbability(scoreDiff, currentTemperature)


def geometricCooling(
        scoreDiff:float, 
        initialTemp: float, 
        iteration: int, 
        constantPowerBase: float
    ) -> bool:
    """
    Decreases temperature geometrically over iterations.
    
    Args:
        scoreDiff (float): Difference in score between the old state and the new state.
        initialTemp (float): the initial temperature of the annealing function
        iteration (int): The current iteration of the algorithm.
        constantPowerBase (float): The constant number that determines the base of the power
            that is multiplied with initialTemp. Must be a floating point number between 0 and 1
    
    Returns (bool): True if the score difference is accepted, else False.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = initialTemp * (constantPowerBase ** iteration)

    return annealingProbability(scoreDiff, currentTemperature)


def linearCooling(
        scoreDiff:float, 
        initialTemp: float, 
        iteration: int, 
        constantCoolingSpeed: float
    ) -> bool:
    """
    Decreases temperature linearily over iterations.

    Args:
        scoreDiff (float): Difference in score between the old state and the new state.
        initialTemp (float): the initial temperature of the annealing function
        iteration (int): The current iteration of the algorithm.
        constantCoolingSpeed (flaot): The linear speed of the cooling scheme.
    
    Returns (bool): True if the score difference is accepted, else False.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    currentTemperature = initialTemp - constantCoolingSpeed * iteration
    
    return annealingProbability(scoreDiff, currentTemperature)


def annealingProbability(scoreDiff: float, temperature: float) -> bool:
    """
    Determines whether an inferior score is accepted based on score difference and temperature.

    Args:
        scoreDiff (float): The difference of the current score and the new score.
        temperature (float): The temperature obtained from one of the cooling schemes.

    Source:
    Mahdi, W.; Medjahed, S. A.; Ouali, M. Performance Analysis of Simulated Annealing Cooling 
    Schedules in the Context of Dense Image Matching. Computación y Sistemas, 2017, 21. 
    https://doi.org/10.13053/cys-21-3-2553.
    """
    if temperature <= 0:
        return False

    probability = exp(-(scoreDiff / temperature))
    if random.random() <= probability:
        return True
    
    return False