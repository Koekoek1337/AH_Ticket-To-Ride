from classes.railNetwork import RailNetwork
from algorithms.hillClimber_Finn_Simon import HillClimber

model = HillClimber()
# model.checkSolution(model.mutateRoute())
model.run()
