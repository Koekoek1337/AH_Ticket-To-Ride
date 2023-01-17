# random, maar dan greedy
# maakt route die rekening houdt met bestaande routes

# totaal time per route < 120 minuten
# totaal aantal route =< 7
# for i in route:
    # kies random beginstation (importeer random library)
    # check connections (in railNetwork.py: getConnectedStation())
    # streep bestaande connections weg (in station.py: listUnusedConnections())
    # for i in connections:
        # kies connection
        # (wordt route.has_legal_move()) if optie < time over (in station.py: get_connection_time())
            # append connection
            # ga naar "random" connection