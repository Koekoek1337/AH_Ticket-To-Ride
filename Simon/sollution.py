import os
import matplotlib.pyplot as plt
import numpy as np
import statistics



def choicesFiles():
    scores = []
    # iterate through all file
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".csv"):
            scores.append(loadScores(file))
    scores.sort()
    average = statistics.mean(scores)
    return scores, average

def loadScores(filename):
    with open(filename, 'r') as file:
        for line in file:
            splits = line.split(',')
            if splits[0] == 'score':
                return float(splits[1])

def plotHist(scores, average):
    counts, bins = np.histogram(scores, 30)
    plt.title("Baseline Holland, Random")
    plt.axvline(average)
    plt.xlabel("scores")
    plt.ylabel("frequency")
    plt.xticks([average], [f'{average:.2f}'])
    plt.stairs(counts, bins)
    plt.savefig("hist.png", format="PNG")
    plt.show()


if __name__ == '__main__':
    plotHist(*choicesFiles())
