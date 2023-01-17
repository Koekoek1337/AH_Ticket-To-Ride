# random, daadwerkelijk random
# alle stations en connections random gekozen, maar wel valide

# totaal time per route < 120 minuten
# totaal aantal routes =< 7
# for i in routes:
    # kies random beginstation (importeer random library)
        # createRoute()
    # check connections (in railNetwork.py: getConnectedStation())
    # for i in connections:
        # kies connection
        # (?wordt route.has_legal_move()?) if optie < time over (in station.py: get_connection_time())
            # append connection
            # ga naar random connection