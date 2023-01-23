from classes.railNetwork import RailNetwork
from visualize.visualize import visualizeNetwork
from algorithms import random_hajo

import json
from os import path
from sys import argv

from typing import List, Dict, Union


def main(stationsFilepath: str, connectionsFilepath: str, recordAll: bool,
         convergenceLimit: int, targetFolder: int, jobType: str, maxRoutes: int, maxTime: float):

    network = RailNetwork(stationsFilepath, connectionsFilepath)

    if jobType == "batch":
        random_hajo.main(network, maxRoutes, maxTime, targetFolder, convergenceLimit=convergenceLimit, 
                         recordAll = recordAll)
        return
    
    network.createRoute(network.getStation("Den Helder"))
    route = network.getRoute(0)
    route.appendStation(network.getStation("Alkmaar"))
    route.appendStation(network.getStation("Castricum"))

    visualizeNetwork(network.connectionPoints(), network.stationPoints(), network.routePointLists())

    network.exportSolution(targetFolder, "Nederland")


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