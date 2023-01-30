from classes.railNetwork import RailNetwork
import visualize.visualize as vis

from algorithms import random_hajo
from algorithms import hillClimber_Hajo

import json
import datetime
import statistics

from os import path
from sys import argv
from copy import deepcopy

from typing import List, Dict, Union, Any, Callable

"""
o How to run:
> python railNL jobs/filename.json
    - See jobs/runHolland.json and jobs/runNetherlands.json
    - **arguments acts like [arg1=A][arg2=b][arg3=c]. In order to build your own job file 
      in order to run your program from main, you should 

"""

def main(jobType: str, **arguments):
    jobType = jobType.lower()

    if jobType in ["batch", "b", "bat"]:
        batch(**arguments)
        return
    
    elif jobType in ["visualize", "vis", "v"]:
        visualize(**arguments)
    
    return


def batch(
    stationsFilepath: str, 
    connectionsFilepath: str, 
    algorithm: str, 
    runs: int = 1, 
    targetFolder: str = "results",
    runName: str = "solution",
    **arguments
) -> None:
    """
    Runs an algorithm in batch as specified by the given job.json file
    """
    ALGORITHMS: Dict[str, Callable[[RailNetwork, Any], RailNetwork]] = {
        "random": random_hajo.main,
        "hillclimber_hajo": hillClimber_Hajo.routeHillclimber,
        "annealing": hillClimber_Hajo.runAnnealing,
    }

    START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    network = RailNetwork(stationsFilepath, connectionsFilepath)
    algorithm = algorithm.lower()

    # Random does not need to utilize multiple runs
    if algorithm == "random":
        ALGORITHMS[algorithm](
            deepcopy(network), 
            targetFolder=targetFolder, 
            runName=runName, 
            **arguments
        )
    
        return
    
    currentRunName = runName
    
    scores: List[Dict[str, float]] = []

    # if multiple runs are utilized
    if runs > 1:
        currentRunName = runName + str(0)
    
    for run in range(runs):
        newNetwork: RailNetwork = ALGORITHMS[algorithm](
            deepcopy(network), 
            targetFolder=targetFolder, 
            runName=currentRunName, 
            **arguments
        )

        scores.append({"run":run, "score":newNetwork.score()})

        currentRunName = runName + str(run + 1)

    if runs > 1:
        average = statistics.mean([score["score"] for score in scores])
        scores.append({"run":"average", "score": average})

        summaryName = f"{runName}-{str(runs)}runs"
        random_hajo.exportScores(scores, targetFolder, summaryName, START_TIMESTAMP)

    return


def visualize(resultFilepath: str, plotType: str= "algorithm", **arguments):
    """Loads a solution into the network and visualizes it"""
    if plotType == "algorithm":
        plotAlgConvergence(resultFilepath, **arguments)

    elif plotType == "network":
        plotNetwork(**arguments)

    elif plotType == "hist":
        plotHist(resultFilepath, **arguments)
    
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