from typing import List, Tuple
import matplotlib.pyplot as plt

def visualize(connections: List[Tuple[Tuple[float, float], Tuple[float, float]]], stations: List[Tuple[str, Tuple[float, float]]], stationNames: bool = True) -> None:
    """
    Args:
        connections: List of tuples of (x, y) and (x, y)
        stations: List of tuples of station name and (x,y)
    """

    for pointPair in connections:
        plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair], marker=" ", color="black", zorder=0)
    
    for station in stations:
        x = station[1][0]
        y = station[1][1]

        plt.scatter(x, y, zorder=1)

        if stationNames:
            name = station[0]
            plt.annotate(name, (x, y))

    plt.show()