from visualize.visualize import visualizeNetwork
from visualize.visualize import plotAlgorithm
from classes.railNetwork import RailNetwork
from visualize.visualize import choicesFiles



visualizeNetwork(RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv"))

plotAlgorithm(*choicesFiles())
