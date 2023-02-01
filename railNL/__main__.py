from classes.railNetwork import RailNetwork
import visualize.visualize as vis

from algorithms import random as randomAlgorithm
from algorithms import simulatedAnnealing
from algorithms import hillclimber_simon, hillclimber_simon1, hillclimber_simon2
from algorithms import hillClimber_Finn_Simon
from algorithms import finnHillClimber

import json
import datetime
import statistics
import time

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
    Runs an algorithm in batch as specified by the given job.json file.

    Args:
        stationsFilepath (str): The filepath of the CSV file containing station names and 
            coordinates.
        connectionsFilepath(str): The filepath of the CSV file containing station connections and
            durations.
        runs (int): The amount of times the algorithm should be ran.
        targetFolder (str): The folder where result files should be saved to.
        runName (str): The human readable part for the name of the result files.
    """
    ALGORITHMS: Dict[str, Callable[[RailNetwork, Any], RailNetwork]] = {
        "random": randomAlgorithm.main,
        "annealing": simulatedAnnealing.runAnnealing,
        "snakeclimber": hillclimber_simon.main,
        "snakeclimber1": hillclimber_simon1.main,
        "snakeclimber2": hillclimber_simon2.main,
        "routesnakeclimber": hillClimber_Finn_Simon.main,
        "routeclimber_finn": finnHillClimber.main,
    }

    START_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Guarantees that the summary file will have a lower timestamp than the first result
    time.sleep(1)

    network = RailNetwork(stationsFilepath, connectionsFilepath)

    # Random does not need to utilize multiple runs
    if algorithm == "random":
        ALGORITHMS[algorithm.lower()](
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

        scores.append({"iteration":run, "score":newNetwork.score()})

        currentRunName = runName + str(run + 1)

    if runs > 1:
        average = statistics.mean([score["score"] for score in scores])
        scores.append({"iteration":"average", "score": average})

        summaryName = f"{runName}-{str(runs)}runs"
        randomAlgorithm.exportScores(scores, targetFolder, summaryName, START_TIMESTAMP)

    return


def visualize(plotType: str= "algorithm", **arguments):
    """
    Selects one of three visualization modes.
    
    Args:
        plotType (str): The name of the plotType
        arguments (Dict[str, any]): Keyword arguments for the plotTypes.
    """
    if plotType in ["algorithm", "alg", "a"]:
        plotAlgConvergence(**arguments)

    elif plotType in ["network", "net", "n"]:
        plotNetwork(**arguments)

    elif plotType in ["histogram", "hist", "h"]:
        plotHist(**arguments)
    
    else:
        print(f"Unknown plotType: {plotType}")

    return


def plotHist(resultFilepath: str, title = "", binCount = 30):
    """
    plots the score data from a batch summary file as a histogram.

    Args:
        resultFilepath (str): The filepath of the batch summary file to collect data from.
        title (str): The title to be displayed on the figure.
        binCount (str): The amount of bins for the histogram
    """
    summary = vis.loadSummary(resultFilepath)
    vis.plotHistAverage(summary[1], title=title, binCount=binCount)

    return


def plotAlgConvergence(resultFilepath: str, title: str):
    """
    Plots the score of an algorithm over iterations.

    Args:
        resultFilepath (str): The filepath of the run summary file to collect data from.
        title (str): The title to be displayed on the figure.
    """
    summary = vis.loadSummary(resultFilepath)
    vis.plotAlgorithm(*summary, title)

    return


def plotNetwork(
    stationsFilepath: str,
    connectionsFilepath: str,
    resultFilepath: str,
    title:str,
    stationNames: bool = False
):
    """
    Visualizes a solution for the train routing problem.

    Args:
        stationsFilepath (str): The filepath of the CSV file containing station names and 
            coordinates.
        connectionsFilepath(str): The filepath of the CSV file containing station connections and
            durations.
        resultFilepath (str): The filepath of the solution csv file.
        title (Str): The title of the figure.
        stationNames (bool): True if station names have to be displayed next to station nodes, else
            false.
    """
    network = RailNetwork(stationsFilepath, connectionsFilepath)
    network.loadSolution(resultFilepath)

    vis.visualizeNetwork(
        network.connectionPoints(),
        network.stationPoints(),
        network.routePointLists(),
        stationNames,
        title
    )


def parseArgv(argv: List[str]) -> Dict[str, Union[str, int, bool]]:
    """
    Takes a .JSON filepath from argv and returns it as dict

    Args:
        argv (List[str]): List of user input arguments.
    """

    USAGEMESSAGE = "Usage: railNL [jobfile.json]"

    if len(argv) == 1 or len(argv) > 2:
        print(USAGEMESSAGE)
        return

    jsonPath = argv[1]

    if not path.exists(jsonPath):
        print(f"Error: File {jsonPath} not found")
        return

    with open(jsonPath) as jsonFile:
        parms = json.load(jsonFile)
        return parms


if __name__ == "__main__":
    arguments = parseArgv(argv)
    if arguments:
        main(**arguments)
