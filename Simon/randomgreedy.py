def main():
    model = RailNetwork("StationsNationaal.csv", "ConnectiesNationaal.csv")
    # Starts a route at a random station.
    model.createRoute(random.choice(model.unVisitedStation()))

    model.nRoute() <= 7
