from classes.railNetwork import RailNetwork
from algorithms.hillClimber_Finn_Simon1 import HillClimber

model = HillClimber()
# model.checkSolution(model.mutateRoute())
model.run()
