from classes.railNetwork import RailNetwork
from algorithms.hillclimber_simon import HillClimber

model = HillClimber()
# model.checkSolution(model.mutateRoute())
model.run()
