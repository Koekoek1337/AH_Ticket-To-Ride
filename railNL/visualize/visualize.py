import os
import re
import statistics
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv
from natsort import natsorted
from typing import List, Tuple, Any


def visualizeNetwork(connections: List[Tuple[Tuple[float, float], Tuple[float, float]]],
                     stations: List[Tuple[str, Tuple[float, float]]],
                     routePointLists: List[List[Tuple[Tuple[int, int], Tuple[int, int]]]],
                     stationNames: bool = True) -> None:
    """
    Input: RailNetwork()
    Gives the connections, stations and routePointLists.
    """

    # Print an image of the Netherlands
    image = mpimg.imread("railNL/resources/NLkaart.png")

    # Update figure size based on image size
    dpi = 120
    height, width, band = image.shape
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig, ax = plt.subplots(figsize=figsize)

    # find the extent
    longitudeMin = 3.5
    longitudeMax = 7.0
    latitudeMin = 50.8
    latitudeMax = 53.5
    extent = [longitudeMin, longitudeMax, latitudeMin, latitudeMax]

    # Draw the image
    ax.imshow(image, interpolation='nearest', extent=extent)

    # draw rail connections
    for pointPair in connections:
        plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair], marker=" ",
        color="grey", zorder=0)


    NUM_COLORS = 20

    cm = plt.get_cmap('gist_rainbow')

    routeNumber = 0
    # draw routes
    for routePointPairs in routePointLists:
        # TODO routepointpairs colours red

        for pointPair in routePointPairs:
            plt.plot([point[0] for point in pointPair], [point[1] for point in pointPair],
            marker=" ", color = cm(1.*i/routeNumber), zorder=1)

        routeNumber += 1

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
    plt.clf()


def choicesFiles(targetFolder: str) -> Tuple[List[int], List[int], float]:
    """
    Input: ../<Foldername>
    Selects the folder with the results and scans through them.
    """
    scores = []
    iterations = []
    # iterate through all file
    for file in os.listdir(targetFolder):
        # Check whether file is in text format or not
        if file.endswith(".csv"):
            scores.append(loadScores(file))
            # gets the amount of iteration from the title in csv file.
            iterations.append(re.split("[-.]", file)[3])

    #  Orders the lists from low to high.
    iterations = natsorted(iterations, key=lambda y: str(y).lower())
    iterations = [int(it) for it in iterations]
    scores.sort()

    average = statistics.mean(scores)
    return scores, iterations, average


def loadScores (targetFolder: str, filename: str) -> float:
    """
    Select the scores of the file.
    """
    with open(f"../{targetFolder}/{filename}", newline = '') as csvFile:
        reader = csv.dictreader(csvFile)

        for row in reader:
            if row["train"] == "score":
                return float(row["stations"])

def loadSummary (targetFolder: str, filename: str) -> Tuple[List[int], List[Float], Optional[float]]:
    """
    Shows the scores with the amount of iterations needed.
    """
    with open(f"../{targetFolder}/{filename}", newline = '') as csvFile:
        reader = csv.dictreader(csvFile)

        iterations = []
        scores = []

        for row in reader:
            if row["iteration"] == "Theoretical max"
                return iterations, score, float(row["score"])

            iterations.append(int(row["iteration"]))
            scores.append(float(row["score"]))

        return iterations, score, None



def plotHistAverage (scores: List[int], _iterations: Any, average: List[int],
                    runName, algorithmName) -> None:
    """
    Input: scores, average from def choicesFiles.
    Input: scope and algorithm.
    Creates a hist with the data.
    """
    counts, bins = np.histogram(scores, 30)
    plt.title(f"{runName}, {algorithmName}")
    plt.axvline(average)
    plt.xlabel("scores")
    plt.ylabel("frequency")
    plt.xticks([average], [f'{average:.2f}'])
    plt.stairs(counts, bins)
    plt.savefig("hist.png", format="PNG")
    plt.show()
    plt.clf()


def plotAlgorithm (scores: List[int], iterations: List[int], _average: Any,
                   runName, algorithmName) -> None:
    """
    Input: scores, average from def choicesFiles.
    Input: scope and algorithm.
    Creates a graph of the applied algorithm.
    """
    plt.plot(iterations, scores)
    plt.title(f"Highest Score: {round(scores[-1], 2)}")
    plt.suptitle(f"{runName}, {algorithmName}")
    plt.xlabel("iteration")
    plt.ylabel("points")
    plt.savefig("algorithm.png", format="PNG")
    plt.show()
