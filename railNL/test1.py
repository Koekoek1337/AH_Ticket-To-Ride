from classes.railNetwork import RailNetwork
from algorithms.hillclimber_simon1 import HillClimber

model = HillClimber()
# model.checkSolution(model.mutateRoute())
model.run()
