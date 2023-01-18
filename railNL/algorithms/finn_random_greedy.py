# random, maar dan greedy
# maakt route die rekening houdt met bestaande routes

# totaal time per route < 120 minuten
# totaal aantal route =< 7
# for routes:
    # kies random beginstation (importeer random library)
    # check connections (in railNetwork.py: getConnectedStation())
    # streep bestaande connections weg (in station.py: listUnusedConnections())
    # for i in connections:
        # kies connection
        # (wordt route.has_legal_move()) if optie < time over (in station.py: get_connection_time())
            # append connection
            # ga naar "random" connection


from classes.railNetwork import RailNetwork
from classes.route import Route
from classes.station import Station
import random

model = RailNetwork("name.csv", "name1.csv")
model.createRoute(random.choice(model.listUnvisitedStations()))

model.nRoute() =< 7

def GreedyRandom(current_station):
    connection_list = []
    connection_options = listUnusedConnections()
    for i in range(len(current_station)):
        if current_station._connections in connection_options:
            connection_list.append()
    return connection_list
    


def main():
    while not checkValidSolution(module.time()) and (model.validMoves() and model.nRoutes() <=7):
        currentRoute = random.choice(model.listUnusedConnections())
        current_station = currentRoute.listStations()[-1]
        trimmed_station_options = GreedyRandom(current_station)
        if trimmed_station_options:
            new_station = random.choice(trimmed_station_options)
        else:
            new_station = random.choice(current_station.listConnectedStations())
        currentRoute.appendStation(new_station)

        if model.nRoute() < 7:
            if model.validMoves() == True:
                randomFloat = random.random()
                if randomFloat <= 0.2
                    model.newRoute(random.choice(model.listStations()))
                else:
                    continue
            else:
                continue