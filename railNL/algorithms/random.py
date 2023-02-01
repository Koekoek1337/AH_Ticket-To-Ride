import random
import csv
import os
import datetime
import time

from copy import deepcopy

from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

from typing import List, Dict, Union

"""Module for generating random solutions for Train routing problem

Main runs a random algorithm on a given empty RailNetwork graph until converged after an amount of
iterations. The algorithm Attempts to fill the RailNetwork with random routes and will export any
network with a new better score to CSV, as well as a score summary file that documents the score per
every iteration if recordAll is true, or score improvements per iteration.

The module also contains the following functions which can be applied for other problems:
    - randomRoute(): Generates a random route in the RailNetwork graph, that scores more than 0 
        points in an isolated system.
    - randomSolution(): Returns the best random solution for a given amount of random iterations for
        optimization algorithms.
    - exportSCores(): Exports a score summary csv file from a list of dictionaries containing the
        iteration and score per stored iteration.
"""


START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def main(
    network: RailNetwork, 
    maxRoutes: int, 
    maxDuration: float, 
    targetFolder: str ="results", 
    runName: str = "solution", 
    convergenceLimit: int = 5000, 
    recordAll: bool = False
    ):
    """
    Random solver for Train routing problem. Intended for baselining and for generating standalone
    solutions.

    Args:
        network (RailNetwork): Empty graph consisting of station and connection nodes.
        maxRoutes (int): The maximum amount of train routes that can be utilized.
        maxDuration (float): The maximum duration a single route may have.
        targetFolder (str): The folder where solutions should be saved to
        runName (str): Human readable part of the filename
        convergenceLimit (int): The maximum amount of iterations to run the algorithm for without
            improvements.
        recordAll (bool): True if all scores should be tracked for the summary file, false if
            only score improvements should be tracked
    """
    # Guarantees that the summary file will have a lower timestamp than the first result
    time.sleep(1)

    convergence = 0
    iteration = 1
    highest = 0

    scores: List[Dict[str, Union[int, float]]] = []

    while convergence <= convergenceLimit:
        if not iteration % 1000:
            print(f"iteration: {iteration}")

        workNetwork = deepcopy(network)
        randomAlgorithm(workNetwork, maxRoutes, maxDuration)
        
        newScore = workNetwork.score()

        # When a new score is found, print to terminal, export the solution and append the score to
        # to the scorelist.
        # Convergence set back to zero.
        if highest < newScore:
            print(f"new best found: {newScore}")
            highest = newScore

            workNetwork.exportSolution(targetFolder, f"{runName}-{iteration}")
            convergence = 0

            scores.append({"iteration":iteration, "score":newScore})
        
        # If all scores are to be tracked, append iteration and score to scores
        elif recordAll:
            scores.append({"iteration":iteration, "score":newScore})

        if convergenceLimit:
            convergence += 1

        iteration += 1
    
    scores.append({"iteration":"Theoretical max", "score": network.theoreticalMaxScore(maxDuration)})
    exportScores(scores, targetFolder, runName, START_TIMESTAMP)
    
    print(f"Terminating with best score {highest}")

    return


def randomAlgorithm(
    network: RailNetwork, maxRoutes: int, maxDuration: int, minimumRoutes: int=1
) -> None:
    """
    Randomly generates a solution for a Train routing problem with up to maxRoutes trainRoutes and 
    of up to maxDuration

    Args:
        network (RailNetwork): The object containing all nodes and routes of the system.
        maxRoutes (int): The maximum amount of train routes that can be utilized.
        maxDuration (float): The maximum duration a single route may have.
        minimumRoutes (int): The minimum amount of routes the solution must have.

    Post: The network given as argument will hold a random solution for the train routing problem.
    """
    nRoutes = random.randint(minimumRoutes, maxRoutes)

    for _ in range(nRoutes):
        randomRoute(network, maxDuration)
    
    return


def randomRoute(network: RailNetwork, maxDuration: float) -> None:
    """
    Randomly adds a route to a rail network in a Train routing problem. The route will have a random
    duration between the longest connecting and maxDuration. Generated routes must have a score
    above 0 in isolation.

    Args:
        network (RailNetwork): The object containing all nodes and routes of the system.
        maxDuration (float): The maximum duration a single route may have.
    
    Post: The network given in the argument will have a new route.
    """
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
        
        # Routes fill up to tTarget or until they no longer have legal moves
        while route.hasLegalMoves(tTarget):
            moves = route.getLegalMoves(tTarget)
            
            index = random.choice(list(moves.keys()))

            if index == 0:
                route.insertStation(index, random.choice(moves[index])[0])
            
            else:
                route.appendStation(random.choice(moves[index])[0])
    return


def randomSolution(
    network: RailNetwork, 
    maxRoutes: int, 
    maxDuration: float,
    randomIterations: int = 1000
) -> RailNetwork:
    """
    Returns the best solution for a railNetwork after a given amount of iterations for optimization.

    Args:
        network (RailNetwork): Empty graph consisting of station and connection nodes.
        maxRoutes (int): The maximum amount of train routes that can be utilized.
        maxDuration (float): The maximum duration a single route may have.
        randomIterations(int): The amount of iteration to run the algorithm for.
    
    Returns (RailNetwork): A valid solution for network.
    """
    bestNetwork = network

    minimumoutes = network.minimumRoutes(maxDuration)

    iteration = 0
    highest = 0

    while iteration <= randomIterations:
        workNetwork = deepcopy(network)

        randomAlgorithm(workNetwork, maxRoutes, maxDuration, minimumoutes)

        newScore = workNetwork.score()
        if highest < newScore:
            highest = newScore
            bestNetwork = workNetwork

        iteration += 1

    return bestNetwork


def exportScores(scoreList: List[Dict[str, Union[int, float]]], targetFolder: str, runName: str, 
                timestamp: str):
    """
    Exports a list of iterations and scores to a summarizing csv file.

    Args:
        scoreList (List[Dict[str, Union[int, float]]]): The list of scores and iterations to export.
        targetFolder (str): The folder the score summary should be exported to.
        runName (str): The human readable part of the filename.
        timestamp (str): The time the algorithm started running
    """
    if not os.path.exists(f"{targetFolder}/"):
            os.mkdir(f"{targetFolder}/")
    
    with open(f"{targetFolder}/{timestamp}-summary-{runName}.csv", "w", newline='') as resultFile:
        fieldnames = scoreList[0].keys()
        
        writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for score in scoreList:
            writer.writerow(score)
    
    return