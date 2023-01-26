from classes.railNetwork import RailNetwork
import visualize.visualize as vis

from algorithms import random_hajo
from algorithms import hillClimber_Hajo

import json
from os import path
from sys import argv

from typing import List, Dict, Union

"""
o How to run:
> python railNL jobs/filename.json
    - See jobs/runHolland.json and jobs/runNetherlands.json
    - **parameters acts like [arg1=A][arg2=b][arg3=c]. In order to build your own job file 
      in order to run your program from main, you should 

"""

def main(jobType: str, **parameters):
    jobType = jobType.lower()

    if jobType in ["batch", "b", "bat"]:
        batch(**parameters)
        return
    
    elif jobType in ["visualize", "vis", "v"]:
        visualize(**parameters)
    
    return


def batch(stationsFilepath: str, connectionsFilepath: str, algorithm: str, **parameters):
    """
    Runs an algorithm in batch as specified by the given job.json file
    """
    network = RailNetwork(stationsFilepath, connectionsFilepath)
    algorithm = algorithm.lower()
    
    if algorithm == "random":
        runRandom(network, **parameters)
    elif algorithm == "hillclimber_hajo":
        runHillclimberHajo(network, **parameters)
    elif algorithm == "annealing":
        runAnnealing(network, **parameters)

    return


def runRandom(network: RailNetwork, **parameters):
    """
    Runs a random algorithm until the highest score converges.
    """
    random_hajo.main(network, **parameters)

    return


def runHillclimberHajo(network: RailNetwork, **parameters) -> None:
    """
    Runs the annealing hillclimber as a normal hillclimber
    """
    hillClimber_Hajo.routeHillclimber(network, **parameters)
    

def runAnnealing(network: RailNetwork, **parameters):
    hillClimber_Hajo.runAnnealing(network = network, **parameters)

    return


def visualize(resultFilepath: str, plotType: str= "algorithm", **parameters):
    """Loads a solution into the network and visualizes it"""
    if plotType == "algorithm":
        plotAlgConvergence(resultFilepath, **parameters)

    elif plotType == "network":
        plotNetwork(**parameters)

    elif plotType == "hist":
        plotHist(resultFilepath, **parameters)
    
    return


def plotHist(resultFilepath: str, title = "", binCount = 30, **_):
    """
    plots the score data as a histogram
    """
    summary = vis.loadSummary(resultFilepath)
    vis.plotHistAverage(summary[1], title=title, binCount=binCount)

    return


def plotAlgConvergence(resultFilepath: str, title: str, **_):
    """
    Plots the convergence of an algorithm over iterations
    """
    summary = vis.loadSummary(resultFilepath)

    vis.plotAlgorithm(*summary, title)
    
    return


def plotNetwork(stationsFilepath: str, connectionsFilepath: str, resultFilepath: str, *_):
    """
    
    """
    network = RailNetwork(stationsFilepath, connectionsFilepath)
    network.loadSolution(resultFilepath)
    pass


def parseArgv(argv: List[str]) -> Dict[str, Union[str, int, bool]]:
    
    USAGEMESSAGE = "Usage: railNL [-b] [-a] dataName [convergenceLimit] [targetFolder]"

    if len(argv) == 1 or len(argv) > 2:
        print(USAGEMESSAGE)
        return
    
    jsonPath = argv[1]

    if path.exists(jsonPath):
        with open(jsonPath) as jsonFile:
            parms = json.load(jsonFile)
            return parms


if __name__ == "__main__":
    main(**parseArgv(argv))