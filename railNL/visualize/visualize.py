from typing import List, Tuple
import matplotlib.pyplot as plt

def visualizeNetwork(connections: List[Tuple[Tuple[float, float], Tuple[float, float]]], 
                     stations: List[Tuple[str, Tuple[float, float]]], 
                     routePointLists: List[List[Tuple[Tuple[int, int], Tuple[int, int]]]],
                     stationNames: bool = True) -> None:
    """
    Args:
        connections: List of tuples of (x, y) and (x, y)
        stations: List of tuples of station name and (x,y)
    """
    # draw rail connections
    for pointPair in connections:
        plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair], marker=" ", 
        color="black", zorder=0)
    
    # draw routes
    for routePointPairs in routePointLists:
        for pointPair in routePointPairs:
            plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair], 
            marker=" ", color="red", zorder=1)
    
    # draw stations
    for station in stations:
        x = station[1][0]
        y = station[1][1]

        plt.scatter(x, y, zorder=5)

        if stationNames:
            name = station[0]
            plt.annotate(name, (x, y))

    plt.show()