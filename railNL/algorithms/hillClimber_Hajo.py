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

def standardHillclimber(network: RailNetwork, maxRoutes: int, maxDuration: float, 
    targetFolder: str ="results", runName: str = "solution", convergenceLimit: int = 5000, 
    recordAll: bool = False):
    
    convergence = 0
    iteration = 1
    highest = 0

    bestNetwork = network

    scores: List[Dict[str, Union[int, float]]] = []

    while convergence <= convergenceLimit:
        print(f"iteration: {iteration}")

        workNetwork = deepcopy(bestNetwork)

        
def climbStep