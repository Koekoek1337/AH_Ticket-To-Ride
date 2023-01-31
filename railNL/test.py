from classes.railNetwork import RailNetwork
from algorithms.hillclimber_simon2 import HillClimber

model = HillClimber()
# model.checkSolution(model.mutateRoute())
model.run()
