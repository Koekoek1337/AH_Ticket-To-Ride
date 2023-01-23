from classes.railNetwork import RailNetwork
from visualize.visualize import visualizeNetwork
from algorithms import random_hajo

import json
from os import path
from sys import argv

from typing import List, Dict, Union

"""
o How to run:
> python railNL jobs/filename.json
    - See jobs/runHolland.json and jobs/runNetherlands.json

"""

def main(stationsFilepath: str, connectionsFilepath: str, jobType: str, **parameters):

    network = RailNetwork(stationsFilepath, connectionsFilepath)

    if jobType.lower() in ["batch", "b", "bat"]:
        runBatch(network, **parameters)
        return
    
    elif jobType.lower() in ["visualize", "vis", "v"]:
        runVis(network, **parameters)


def runBatch(network: RailNetwork, algorithm: str, **parameters):
    algorithm = algorithm.lower()
    
    if algorithm == "random":
        random_hajo.main(network, **parameters)


def runVis(network: RailNetwork, **parameters):
    network.createRoute(network.getStation("Den Helder"))
    route = network.getRoute(0)
    route.appendStation(network.getStation("Alkmaar"))
    route.appendStation(network.getStation("Castricum"))

    visualizeNetwork(network.connectionPoints(), network.stationPoints(), network.routePointLists())
    

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