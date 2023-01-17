from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station

def main():
    model = RailNetwork(filename)
    model.newRoute(random.Randomchoice(model.listStations()))

    model.nRoute() =< 7


    while not checkValidSolution() and (model.validMoves() and model.nRoutes() <=7):
        currentRoute = random.Randomchoice(model.listRoutes())
        current_station = currentRoute.listStations()[-1]
        new_station = random.Randomchoice(current_station.listConnectedStations())
        currentRoute.appendStation(new_station)

        if model.nRoute() < 7:
            if model.validMoves() == True:
                randomFloat = random.random()
                if randomFloat <= 0.2
                    model.newRoute(random.Randomchoice(model.listStatins()))
                else:
                    continue
            else:
                continue
            
    exportSolution("random")