def main():
    model = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv")
    # Starts a route at a random station.
    model.createRoute(random.choice(model.unVisitedStation()))

    model.nRoute() <= 7

    route = model.createRoute(random.choice(model.listStations(nUnvisited = True)))

    unvisted = currentStation.listStations(nUnvisited = True)
    unconnected = currentStation.getLegalMoves(un)

    # If a connected station is not visited, the route will forward to this station.
    if unvisted:
        currentStation = random.choice(model.listUnvisitedtation())
        currentStation = currentRoute.listStations()[-1]
        newStation = random.choice(currentStation.listUnvisitedStations())
        currentRoute.appendStation(newStation)
    # If a connected rail is not visited, the route will forward on this rail.
    elif unconnected:
        currentStation = currentRoute.listStations()[-1]
        newStation = random.choice(currentStation.listUnivistedStations())
        currentRoute.appendStation(newStation)
        currentStation = random.choice(model.getLegalMoves())
    # If there is no unvisted station or undriven rail, the route will forward to the shortest track.
    else:

    currentStation = currentRoute.listStations()[-1]
    newStation = random.choice(currentStation.listUnvisitedStations())
    currentRoute.appendStation(newStation)




    while not network.checkValidSolution(tMax) and network.hasLegalMoves(tMax, nRoutes):
        route = random.choice(network.listRoutesWithLegal(tMax))

        moves = route.getLegalMoves(tMax)

        index = random.choice(list(moves.keys()))

        if index == 0:
            route.insertStation(index, random.choice(moves[index])[0])

        else:
            route.appendStation(random.choice(moves[index])[0])

    return model
