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

def main(stationsFilepath: str, connectionsFilepath: str, jobType: str, **parameters):
    network = RailNetwork(stationsFilepath, connectionsFilepath)

    if jobType.lower() in ["batch", "b", "bat"]:
        runBatch(network, **parameters)
        return
    
    elif jobType.lower() in ["visualize", "vis", "v"]:
        runVis(network, **parameters)


def runBatch(network: RailNetwork, algorithm: str, **parameters):
    """Runs an algorithm in batch as specified by the given job.json file"""
    algorithm = algorithm.lower()
    
    if algorithm == "random":
        random_hajo.main(network, **parameters)
    elif algorithm == "hillclimber_hajo":
        hillClimber_Hajo.routeHillclimber(network, **parameters)


def runVis(network: RailNetwork, resultFilepath: str, plotType: str= "algorithm", **parameters):
    """Loads a solution into the network and visualizes it"""
    if plotType == "algorithm":
        runAlgConvergence(resultFilepath, **parameters)
        
    elif plotType == "network":
        network.loadSolution(resultFilepath)
        vis.visualizeNetwork(network.connectionPoints(), network.stationPoints(), network.routePointLists(), **parameters)
    
    elif plotType == "hist":
        runHist(resultFilepath, **parameters)


def runHist(resultFilepath: str, title = "", binCount = 30, **_):
    """
    plots the score data as a histogram
    """
    summary = vis.loadSummary(resultFilepath)

    vis.plotHistAverage(summary[1], title=title, binCount=binCount)


def runAlgConvergence(resultFilepath: str, title: str, **_):
    """
    Plots the convergence of an algorithm over iterations
    """
    summary = vis.loadSummary(resultFilepath)

    vis.plotAlgorithm(*summary, title)


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