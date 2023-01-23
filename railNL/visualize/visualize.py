import os
import statistics
from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import re
from classes.railNetwork import RailNetwork
import matplotlib
import bestRandomHolland

stations = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").stationPoints()
connections = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").connectionPoints()
route = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv").routePointLists()

def visualizeNetwork(connections: List[Tuple[Tuple[float, float], Tuple[float, float]]],
                     stations: List[Tuple[str, Tuple[float, float]]],
                     routePointLists: List[List[Tuple[Tuple[int, int], Tuple[int, int]]]],
                     stationNames: bool = True) -> None:
    """
    Args:
        connections: List of tuples of (x, y) and (x, y)
        stations: List of tuples of station name and (x,y)
    """

    # Print an image of the Netherlands
    image = mpimg.imread("NLkaart.png")
    # plt.imshow(image)
    dpi = 120
    height, width, band = image.shape
    # Update figure size based on image size
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig, ax = plt.subplots(figsize=figsize)

    # find the extent
    longitude_top_left = 3.5
    longitude_top_right = 7.0
    latitude_bottom_left = 50.8
    latitude_top_left = 53.5
    extent = [longitude_top_left, longitude_top_right, latitude_bottom_left, latitude_top_left]

    # Draw the image
    ax.imshow(image, interpolation='nearest', extent=extent)

    # draw rail connections
    for pointPair in connections:
        plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair], marker=" ",
        color="grey", zorder=0)

    # draw routes
    for routePointPairs in routePointLists:
        # TODO routepointpairs colours red
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

    plt.savefig("rail1.png", format="PNG")
    plt.show()




def choicesFiles():
    scores = []
    iteration = []
    # iterate through all file
    # TODO
    for file in os.listdir("Ticket-to-Ride\bestRandomHolland"):
        # Check whether file is in text format or not
        if file.endswith(".csv"):
            scores.append(loadScores(file))
            iteration.append(re.split("[-.]", file)[-3])

    scores.sort()
    average = statistics.mean(scores)
    return scores, average, iteration

def loadScores(filename):
    # Select the scores of the files.
    with open(filename, 'r') as file:
        for line in file:
            splits = line.split(',')
            if splits[0] == 'score':
                return float(splits[1])

def plotHistAverage(scores, average):
    # Creates a hist with the data.
    counts, bins = np.histogram(scores, 30)
    plt.title("Baseline Holland, Random-Average")
    plt.axvline(average)
    plt.xlabel("scores")
    plt.ylabel("frequency")
    plt.xticks([average], [f'{average:.2f}'])
    plt.stairs(counts, bins)
    plt.savefig("hist.png", format="PNG")
    plt.show()

def plotAlgorithm(scocers, iterations):
    plt.title("Baseline Holland, Random")
    plt.xlabel("iteration")
    plt.ylabel("scores")
    plt.savefig("algorithm.png", format="PNG")


if __name__ == '__main__':
#     # plotHist(*choicesFiles())
    visualizeNetwork(connections, stations, route)
